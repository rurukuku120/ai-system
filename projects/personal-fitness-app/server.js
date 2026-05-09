const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");

// .env 파일 자동 로드 (외부 패키지 없이)
try {
  const envFile = fs.readFileSync(path.join(__dirname, ".env"), "utf8");
  for (const line of envFile.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const [key, ...rest] = trimmed.split("=");
    if (key && rest.length) process.env[key.trim()] ??= rest.join("=").trim();
  }
} catch {}

const port = Number(process.env.PORT || 4173);
const root = __dirname;

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
};

function readBody(request) {
  return new Promise((resolve, reject) => {
    let body = "";
    request.on("data", (chunk) => {
      body += chunk;
      if (body.length > 15_000_000) {
        request.destroy();
        reject(new Error("요청이 너무 크다."));
      }
    });
    request.on("end", () => resolve(body));
    request.on("error", reject);
  });
}

function sendJson(response, status, payload) {
  response.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  response.end(JSON.stringify(payload));
}

function extractResponseText(payload) {
  if (payload.output_text) return payload.output_text;
  const chunks = [];
  for (const item of payload.output || []) {
    for (const content of item.content || []) {
      if (content.text) chunks.push(content.text);
      if (content.type === "output_text" && content.text) chunks.push(content.text);
    }
  }
  return chunks.join("\n");
}

async function notionRequest(path, method = "GET", body = null) {
  const res = await fetch(`https://api.notion.com/v1${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${process.env.NOTION_TOKEN}`,
      "Content-Type": "application/json",
      "Notion-Version": "2022-06-28",
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || `Notion ${res.status}`);
  return data;
}

function buildNotionProperties(record) {
  const titles = {
    meal: `${record.mealType || "식사"} 식단`,
    strength: `${record.split || ""} · ${record.name || "운동"}`,
    run: `러닝 ${record.km || 0}km`,
  };
  return {
    이름: { title: [{ text: { content: titles[record.type] || record.type } }] },
    종류: { select: { name: record.typeLabel || record.type } },
    날짜: { date: { start: record.date.slice(0, 10) } },
    점수: { number: record.score ?? null },
    RecordID: { rich_text: [{ text: { content: String(record.id) } }] },
    JSON: { rich_text: [{ text: { content: JSON.stringify(record).slice(0, 2000) } }] },
  };
}

async function handleNotionSave(request, response) {
  if (!process.env.NOTION_TOKEN || !process.env.NOTION_DATABASE_ID) {
    sendJson(response, 503, { error: "Notion 미설정" });
    return;
  }
  const { record } = JSON.parse(await readBody(request));
  const existing = await notionRequest(`/databases/${process.env.NOTION_DATABASE_ID}/query`, "POST", {
    filter: { property: "RecordID", rich_text: { equals: String(record.id) } },
    page_size: 1,
  });
  const properties = buildNotionProperties(record);
  if (existing.results?.length > 0) {
    await notionRequest(`/pages/${existing.results[0].id}`, "PATCH", { properties });
  } else {
    await notionRequest("/pages", "POST", {
      parent: { database_id: process.env.NOTION_DATABASE_ID },
      properties,
    });
  }
  sendJson(response, 200, { ok: true });
}

async function handleNotionLoad(request, response) {
  if (!process.env.NOTION_TOKEN || !process.env.NOTION_DATABASE_ID) {
    sendJson(response, 503, { error: "Notion 미설정" });
    return;
  }
  const records = [];
  let cursor;
  do {
    const result = await notionRequest(`/databases/${process.env.NOTION_DATABASE_ID}/query`, "POST", {
      ...(cursor ? { start_cursor: cursor } : {}),
      page_size: 100,
      sorts: [{ property: "날짜", direction: "ascending" }],
    });
    for (const page of result.results) {
      const jsonText = page.properties.JSON?.rich_text?.[0]?.plain_text;
      if (jsonText) {
        try { records.push(JSON.parse(jsonText)); } catch {}
      }
    }
    cursor = result.has_more ? result.next_cursor : null;
  } while (cursor);
  sendJson(response, 200, { records });
}

async function handleNotionDelete(request, response) {
  if (!process.env.NOTION_TOKEN || !process.env.NOTION_DATABASE_ID) {
    sendJson(response, 503, { error: "Notion 미설정" });
    return;
  }
  const { recordId } = JSON.parse(await readBody(request));
  const existing = await notionRequest(`/databases/${process.env.NOTION_DATABASE_ID}/query`, "POST", {
    filter: { property: "RecordID", rich_text: { equals: String(recordId) } },
    page_size: 1,
  });
  if (existing.results?.length > 0) {
    await notionRequest(`/pages/${existing.results[0].id}`, "PATCH", { archived: true });
  }
  sendJson(response, 200, { ok: true });
}

async function handleAnalyze(request, response) {
  if (!process.env.OPENAI_API_KEY) {
    sendJson(response, 503, { error: "OPENAI_API_KEY가 설정되지 않았다." });
    return;
  }

  const body = JSON.parse(await readBody(request));
  const upstream = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
    },
    body: JSON.stringify({
      model: body.model || "gpt-4.1-mini",
      input: [
        {
          role: "user",
          content: [
            {
              type: "input_text",
              text: [
                "너는 식단, 웨이트 트레이닝, 러닝을 함께 보는 한국어 피트니스 코치다.",
                "의학적 진단이 아니라 일반적인 생활 코칭으로만 답한다.",
                "반드시 JSON 객체만 반환한다. 마크다운은 쓰지 않는다.",
                `분석 작업: ${body.task}`,
                `사용자 입력: ${JSON.stringify(body.context || {})}`,
              ].join("\n"),
            },
            {
              type: "input_image",
              image_url: body.imageUrl,
              detail: "auto",
            },
          ],
        },
      ],
    }),
  });

  const payload = await upstream.json();
  if (!upstream.ok) {
    sendJson(response, upstream.status, { error: payload.error?.message || "AI 분석 실패" });
    return;
  }

  sendJson(response, 200, { text: extractResponseText(payload) });
}

function serveStatic(request, response) {
  const url = new URL(request.url, `http://${request.headers.host}`);
  const cleanPath = url.pathname === "/" ? "/index.html" : url.pathname;
  const filePath = path.normalize(path.join(root, cleanPath));

  if (!filePath.startsWith(root)) {
    response.writeHead(403);
    response.end("Forbidden");
    return;
  }

  fs.readFile(filePath, (error, content) => {
    if (error) {
      response.writeHead(404);
      response.end("Not found");
      return;
    }

    response.writeHead(200, {
      "Content-Type": mimeTypes[path.extname(filePath)] || "application/octet-stream",
    });
    response.end(content);
  });
}

const server = http.createServer(async (request, response) => {
  try {
    if (request.method === "GET" && request.url === "/api/status") {
      sendJson(response, 200, {
        openaiReady: Boolean(process.env.OPENAI_API_KEY),
        notionReady: Boolean(process.env.NOTION_TOKEN && process.env.NOTION_DATABASE_ID),
      });
      return;
    }
    if (request.method === "POST" && request.url === "/api/analyze") {
      await handleAnalyze(request, response);
      return;
    }
    if (request.method === "POST" && request.url === "/api/notion-save") {
      await handleNotionSave(request, response);
      return;
    }
    if (request.method === "GET" && request.url === "/api/notion-load") {
      await handleNotionLoad(request, response);
      return;
    }
    if (request.method === "POST" && request.url === "/api/notion-delete") {
      await handleNotionDelete(request, response);
      return;
    }
    serveStatic(request, response);
  } catch (error) {
    sendJson(response, 500, { error: error.message || "서버 오류" });
  }
});

server.listen(port, () => {
  console.log(`Fit Coach running at http://localhost:${port}`);
});
