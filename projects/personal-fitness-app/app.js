const storageKey = "fit-coach-records";

const splitPlans = {
  상체: [
    { name: "벤치프레스", target: "가슴", guide: "4세트 6-10회" },
    { name: "바벨로우", target: "등", guide: "4세트 8-10회" },
    { name: "오버헤드프레스", target: "어깨", guide: "3세트 6-10회" },
    { name: "랫풀다운", target: "등", guide: "3세트 10-12회" },
    { name: "컬 + 푸시다운", target: "팔", guide: "각 3세트 10-15회" },
  ],
  하체: [
    { name: "스쿼트", target: "대퇴", guide: "4세트 5-8회" },
    { name: "루마니안 데드리프트", target: "햄스트링", guide: "4세트 8-10회" },
    { name: "레그프레스", target: "대퇴", guide: "3세트 10-12회" },
    { name: "레그컬", target: "햄스트링", guide: "3세트 10-15회" },
    { name: "카프레이즈", target: "종아리", guide: "4세트 12-20회" },
  ],
};

const pplPlans = {
  Push: [
    { name: "벤치프레스", target: "가슴", guide: "4세트 6-10회" },
    { name: "인클라인 덤벨프레스", target: "가슴 상부", guide: "3세트 8-12회" },
    { name: "오버헤드프레스", target: "어깨", guide: "3세트 6-10회" },
    { name: "사이드 레터럴레이즈", target: "어깨 측면", guide: "3세트 12-15회" },
    { name: "삼두 푸시다운", target: "삼두", guide: "3세트 10-15회" },
  ],
  Pull: [
    { name: "데드리프트", target: "등 전체", guide: "4세트 4-6회" },
    { name: "바벨로우", target: "등 중부", guide: "4세트 8-10회" },
    { name: "랫풀다운", target: "광배", guide: "3세트 10-12회" },
    { name: "페이스풀", target: "후면 삼각", guide: "3세트 12-15회" },
    { name: "이두 컬", target: "이두", guide: "3세트 10-15회" },
  ],
  Legs: [
    { name: "스쿼트", target: "대퇴", guide: "4세트 5-8회" },
    { name: "레그프레스", target: "대퇴", guide: "3세트 10-12회" },
    { name: "루마니안 데드리프트", target: "햄스트링", guide: "4세트 8-10회" },
    { name: "레그컬", target: "햄스트링", guide: "3세트 10-15회" },
    { name: "카프레이즈", target: "종아리", guide: "4세트 12-20회" },
  ],
};

const EXERCISE_IMG_BASE = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises";

const liftGuides = {
  벤치프레스: {
    cues: ["견갑을 모으고 가슴을 연다.", "바는 가슴 아래쪽으로 내린다.", "손목은 꺾지 않고 팔꿈치는 45도 정도로 둔다."],
    svg: "bench",
    img: `${EXERCISE_IMG_BASE}/Barbell_Bench_Press_-_Medium_Grip/0.jpg`,
  },
  바벨로우: {
    cues: ["엉덩이를 뒤로 빼고 등을 평평하게 유지한다.", "바를 배꼽 쪽으로 당긴다.", "반동보다 등으로 당기는 느낌을 우선한다."],
    svg: "row",
    img: `${EXERCISE_IMG_BASE}/Bent_Over_Barbell_Row/0.jpg`,
  },
  오버헤드프레스: {
    cues: ["갈비뼈가 들리지 않게 복압을 잡는다.", "바는 얼굴을 지나 수직으로 올린다.", "머리를 살짝 앞으로 넣어 마무리한다."],
    svg: "press",
    img: `${EXERCISE_IMG_BASE}/Barbell_Shoulder_Press_-_Medium_Grip/0.jpg`,
  },
  랫풀다운: {
    cues: ["가슴을 세우고 어깨를 먼저 내린다.", "팔꿈치를 옆구리로 당긴다.", "목 뒤가 아니라 쇄골 앞쪽으로 당긴다."],
    svg: "pulldown",
    img: `${EXERCISE_IMG_BASE}/Wide-Grip_Lat_Pulldown/0.jpg`,
  },
  "컬 + 푸시다운": {
    cues: ["팔꿈치를 몸 옆에 고정한다.", "컬은 반동 없이 끝까지 조인다.", "푸시다운은 손목을 세우고 아래에서 잠깐 멈춘다."],
    svg: "arms",
    img: `${EXERCISE_IMG_BASE}/Barbell_Curl/0.jpg`,
  },
  스쿼트: {
    cues: ["발은 어깨너비, 무릎은 발끝 방향으로 보낸다.", "허리는 중립으로 두고 복압을 유지한다.", "앉았다 일어날 때 발바닥 전체로 민다."],
    svg: "squat",
    img: `${EXERCISE_IMG_BASE}/Barbell_Squat/0.jpg`,
  },
  "루마니안 데드리프트": {
    cues: ["무릎은 살짝 굽히고 엉덩이를 뒤로 보낸다.", "바는 허벅지와 정강이에 가깝게 내린다.", "허리가 말리기 전 범위에서 멈춘다."],
    svg: "hinge",
    img: `${EXERCISE_IMG_BASE}/Romanian_Deadlift/0.jpg`,
  },
  레그프레스: {
    cues: ["엉덩이가 패드에서 뜨지 않게 한다.", "무릎은 발끝 방향으로 움직인다.", "무릎을 완전히 잠그지 않고 반복한다."],
    svg: "legpress",
    img: `${EXERCISE_IMG_BASE}/Leg_Press/0.jpg`,
  },
  레그컬: {
    cues: ["골반이 들리지 않게 패드에 붙인다.", "발뒤꿈치를 엉덩이 쪽으로 당긴다.", "내릴 때 천천히 버틴다."],
    svg: "legcurl",
    img: `${EXERCISE_IMG_BASE}/Lying_Leg_Curls/0.jpg`,
  },
  카프레이즈: {
    cues: ["발목만 움직이고 무릎 반동을 줄인다.", "위에서 1초 멈춰 종아리를 조인다.", "아래에서 충분히 늘린 뒤 반복한다."],
    svg: "calf",
    img: `${EXERCISE_IMG_BASE}/Standing_Calf_Raises/0.jpg`,
  },
  "인클라인 덤벨프레스": {
    cues: ["등받이 30-45도 세팅, 덤벨을 가슴 위쪽으로 밀어올린다.", "내릴 때 팔꿈치를 45도 유지하고 천천히 내린다.", "어깨가 앞으로 말리지 않게 견갑을 모은다."],
    svg: "bench",
    img: `${EXERCISE_IMG_BASE}/Incline_Dumbbell_Press/0.jpg`,
  },
  "사이드 레터럴레이즈": {
    cues: ["팔꿈치를 살짝 굽히고 옆으로 들어올린다.", "어깨 높이 이상 올리지 않는다.", "내릴 때 반동 없이 천천히 버틴다."],
    svg: "press",
    img: `${EXERCISE_IMG_BASE}/Dumbbell_Lateral_Raise/0.jpg`,
  },
  "삼두 푸시다운": {
    cues: ["팔꿈치를 몸 옆에 고정하고 아래로 누른다.", "손목은 꺾지 않고 세운다.", "완전히 펴서 1초 수축 후 천천히 올린다."],
    svg: "arms",
    img: `${EXERCISE_IMG_BASE}/Triceps_Pushdown/0.jpg`,
  },
  데드리프트: {
    cues: ["발은 엉덩이 너비, 바는 발 위 정강이 가까이 둔다.", "등을 평평하게 유지하고 복압을 잡는다.", "발로 바닥을 밀듯이 몸을 세운다."],
    svg: "hinge",
    img: `${EXERCISE_IMG_BASE}/Barbell_Deadlift/0.jpg`,
  },
  페이스풀: {
    cues: ["팔꿈치를 어깨 높이로 유지하며 당긴다.", "줄을 얼굴 쪽으로 당기고 외회전을 느낀다.", "천천히 펴며 어깨 전면 자극을 유지한다."],
    svg: "pulldown",
    img: `${EXERCISE_IMG_BASE}/Face_Pull/0.jpg`,
  },
  "이두 컬": {
    cues: ["팔꿈치를 몸 옆에 고정한다.", "완전히 굽혀 수축 후 천천히 내린다.", "반동 없이 근육으로만 들어올린다."],
    svg: "arms",
    img: `${EXERCISE_IMG_BASE}/Dumbbell_Bicep_Curl/0.jpg`,
  },
};

let activeSplit = "상체";
let activeRoutineMode = "이분할";
let proxyReady = false;
let notionReady = false;

function readStorage(storage, key, fallback = "") {
  try {
    return storage.getItem(key) || fallback;
  } catch {
    return fallback;
  }
}

function getWebStorage(name) {
  try {
    return window[name];
  } catch {
    return null;
  }
}

function writeStorage(storage, key, value) {
  try {
    storage.setItem(key, value);
  } catch {
    // Some IDE previews disable storage. The app should still render and work for the current session.
  }
}

function removeStorage(storage, key) {
  try {
    storage.removeItem(key);
  } catch {
    // Ignore storage restrictions in preview environments.
  }
}

const elements = {
  openSettings: document.querySelector("#openSettings"),
  closeSettings: document.querySelector("#closeSettings"),
  settingsSheet: document.querySelector("#settingsSheet"),
  settingsBackdrop: document.querySelector("#settingsBackdrop"),
  settingsForm: document.querySelector("#settingsForm"),
  apiKey: document.querySelector("#apiKey"),
  modelName: document.querySelector("#modelName"),
  analysisMode: document.querySelector("#analysisMode"),
  apiStatus: document.querySelector("#apiStatus"),
  quickCards: document.querySelector("#quickCards"),
  quickTabs: document.querySelector("#quickTabs"),
  mealForm: document.querySelector("#mealForm"),
  strengthForm: document.querySelector("#strengthForm"),
  runForm: document.querySelector("#runForm"),
  mealAnalyze: document.querySelector("#mealAnalyze"),
  mealSubmit: document.querySelector("#mealSubmit"),
  runSubmit: document.querySelector("#runSubmit"),
  mealPhoto: document.querySelector("#mealPhoto"),
  mealPhotoCamera: document.querySelector("#mealPhotoCamera"),
  mealPreviewCamera: document.querySelector("#mealPreviewCamera"),
  runPhoto: document.querySelector("#runPhoto"),
  runPhotoCamera: document.querySelector("#runPhotoCamera"),
  runPreviewCamera: document.querySelector("#runPreviewCamera"),
  mealPreview: document.querySelector("#mealPreview"),
  runPreview: document.querySelector("#runPreview"),
  mealInsight: document.querySelector("#mealInsight"),
  runInsight: document.querySelector("#runInsight"),
  liftName: document.querySelector("#liftName"),
  customLiftLabel: document.querySelector("#customLiftLabel"),
  customLiftInput: document.querySelector("#customLiftInput"),
  liftGuide: document.querySelector("#liftGuide"),
  splitRoutine: document.querySelector("#splitRoutine"),
  themeToggle: document.querySelector("#themeToggle"),
  timeline: document.querySelector("#timeline"),
  emptyState: document.querySelector("#emptyState"),
  coachList: document.querySelector("#coachList"),
  clearAll: document.querySelector("#clearAll"),
};

function loadSettings() {
  const session = getWebStorage("sessionStorage");
  const local = getWebStorage("localStorage");
  return {
    apiKey: readStorage(session, "fit-coach-api-key"),
    model: readStorage(local, "fit-coach-model", "gpt-4.1-mini"),
    mode: readStorage(local, "fit-coach-analysis-mode", "auto"),
    notionEnabled: readStorage(local, "fit-coach-notion-enabled", "false") === "true",
    notionToken: readStorage(local, "fit-coach-notion-token"),
    notionDbId: readStorage(local, "fit-coach-notion-db-id"),
  };
}

function saveSettings(settings) {
  const session = getWebStorage("sessionStorage");
  const local = getWebStorage("localStorage");
  if (settings.apiKey) {
    writeStorage(session, "fit-coach-api-key", settings.apiKey);
  } else {
    removeStorage(session, "fit-coach-api-key");
  }
  writeStorage(local, "fit-coach-model", settings.model || "gpt-4.1-mini");
  writeStorage(local, "fit-coach-analysis-mode", settings.mode || "auto");
  writeStorage(local, "fit-coach-notion-enabled", settings.notionEnabled ? "true" : "false");
  if (settings.notionToken) writeStorage(local, "fit-coach-notion-token", settings.notionToken);
  if (settings.notionDbId) writeStorage(local, "fit-coach-notion-db-id", settings.notionDbId);
}

function loadRecords() {
  try {
    const local = getWebStorage("localStorage");
    return JSON.parse(readStorage(local, storageKey, "[]")) ?? [];
  } catch {
    return [];
  }
}

function saveRecords(records) {
  writeStorage(getWebStorage("localStorage"), storageKey, JSON.stringify(records));
}

function createId() {
  return window.crypto?.randomUUID ? window.crypto.randomUUID() : `${Date.now()}-${Math.random()}`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function todayKey() {
  return new Date().toISOString().slice(0, 10);
}

function startOfWeek(date) {
  const target = new Date(date);
  const day = target.getDay() || 7;
  target.setHours(0, 0, 0, 0);
  target.setDate(target.getDate() - day + 1);
  return target;
}

function setPreview(input, image) {
  const file = input.files?.[0];
  if (!file) return;
  image.src = URL.createObjectURL(file);
  image.closest(".upload-box").classList.add("has-image");
}

function updateThemeIcon() {
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  const icon = document.getElementById("themeIcon");
  if (!icon) return;
  if (isDark) {
    icon.innerHTML = `<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>`;
  } else {
    icon.innerHTML = `<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>`;
  }
}

function initTheme() {
  const local = getWebStorage("localStorage");
  const saved = readStorage(local, "fit-coach-theme", "");
  const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  const theme = saved || (prefersDark ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", theme);
  updateThemeIcon();
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  writeStorage(getWebStorage("localStorage"), "fit-coach-theme", next);
  updateThemeIcon();
}

function hydrateSettings() {
  const settings = loadSettings();
  elements.apiKey.value = settings.apiKey;
  elements.modelName.value = settings.model;
  elements.analysisMode.value = settings.mode;
  const notionToggle = document.querySelector("#notionEnabled");
  const notionFields = document.querySelector("#notionFields");
  if (notionToggle) {
    notionToggle.checked = settings.notionEnabled;
    if (notionFields) notionFields.style.display = settings.notionEnabled ? "" : "none";
    notionToggle.addEventListener("change", () => {
      if (notionFields) notionFields.style.display = notionToggle.checked ? "" : "none";
    });
  }
  const notionTokenEl = document.querySelector("#notionToken");
  const notionDbIdEl = document.querySelector("#notionDbId");
  if (notionTokenEl) notionTokenEl.value = settings.notionToken || "";
  if (notionDbIdEl) notionDbIdEl.value = settings.notionDbId || "";
  notionReady = settings.notionEnabled && Boolean(settings.notionToken) && Boolean(settings.notionDbId);
  renderApiStatus();
}

function renderApiStatus() {
  const settings = loadSettings();
  const aiReady = settings.mode === "auto" && (Boolean(settings.apiKey) || proxyReady);
  if (notionReady && aiReady) elements.apiStatus.textContent = "AI + Notion 연결";
  else if (notionReady) elements.apiStatus.textContent = "Notion 연결";
  else if (aiReady) elements.apiStatus.textContent = "AI 분석 준비";
  else elements.apiStatus.textContent = "로컬 분석";
  elements.apiStatus.classList.toggle("is-ready", aiReady || notionReady);
  // 서버 키 연결 시 안내
  const notice = document.querySelector("#serverKeyNotice");
  if (notice) notice.style.display = proxyReady ? "" : "none";
}

async function notionFetch(path, method = "GET", body = null) {
  return fetch(path, {
    method,
    headers: { "Content-Type": "application/json" },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
}

async function syncRecordToNotion(record) {
  if (!notionReady) return;
  try {
    await notionFetch("/api/notion-save", "POST", { record });
  } catch {}
}

async function deleteRecordFromNotion(recordId) {
  if (!notionReady) return;
  try {
    await notionFetch("/api/notion-delete", "POST", { recordId });
  } catch {}
}

async function syncWithNotion() {
  if (!notionReady) return;
  try {
    const response = await notionFetch("/api/notion-load");
    if (!response.ok) return;
    const { records: notionRecords } = await response.json();
    if (!Array.isArray(notionRecords)) return;

    const localRecords = loadRecords();
    const notionIds = new Set(notionRecords.map((r) => r.id));

    for (const r of localRecords) {
      if (!notionIds.has(r.id)) syncRecordToNotion(r);
    }

    const localOnlyRecords = localRecords.filter((r) => !notionIds.has(r.id));
    const merged = [...notionRecords, ...localOnlyRecords].sort(
      (a, b) => new Date(a.date) - new Date(b.date),
    );
    saveRecords(merged);
    render();
  } catch {}
}

async function checkProxyStatus() {
  if (window.location.protocol === "file:") return;
  try {
    const response = await fetch("/api/status");
    const status = await response.json();
    proxyReady = Boolean(status.openaiReady);
    notionReady = Boolean(status.notionReady);
  } catch {
    proxyReady = false;
    notionReady = false;
  }
  renderApiStatus();
  if (notionReady) syncWithNotion();
}

function openSettingsSheet() {
  elements.settingsBackdrop.hidden = false;
  elements.settingsSheet.classList.add("is-open");
  elements.settingsSheet.setAttribute("aria-hidden", "false");
  document.body.classList.add("sheet-open");
  elements.apiKey.focus();
}

function closeSettingsSheet() {
  elements.settingsSheet.classList.remove("is-open");
  elements.settingsSheet.setAttribute("aria-hidden", "true");
  elements.settingsBackdrop.hidden = true;
  document.body.classList.remove("sheet-open");
  elements.openSettings.focus();
}

function switchTab(index) {
  const cards = [...elements.quickCards.querySelectorAll(".quick-card")];
  const tabs = [...elements.quickTabs.querySelectorAll(".quick-tab")];
  cards.forEach((card, i) => card.classList.toggle("is-active", i === index));
  tabs.forEach((tab, i) => {
    tab.classList.toggle("is-active", i === index);
    tab.setAttribute("aria-selected", String(i === index));
  });
}

function fileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.addEventListener("load", () => resolve(reader.result));
    reader.addEventListener("error", () => reject(reader.error));
    reader.readAsDataURL(file);
  });
}

function extractResponseText(response) {
  if (response.output_text) return response.output_text;
  const chunks = [];
  for (const item of response.output || []) {
    for (const content of item.content || []) {
      if (content.text) chunks.push(content.text);
      if (content.type === "output_text" && content.text) chunks.push(content.text);
    }
  }
  return chunks.join("\n");
}

function parseJsonLoose(text) {
  try {
    return JSON.parse(text);
  } catch {
    // 첫 번째 { 부터 짝이 맞는 } 까지만 추출
    const start = text.indexOf("{");
    if (start === -1) throw new Error("JSON 응답을 찾지 못했다.");
    let depth = 0;
    let end = -1;
    for (let i = start; i < text.length; i++) {
      if (text[i] === "{") depth++;
      else if (text[i] === "}") { depth--; if (depth === 0) { end = i; break; } }
    }
    if (end === -1) throw new Error("JSON 응답을 찾지 못했다.");
    return JSON.parse(text.slice(start, end + 1));
  }
}

async function analyzeImageWithOpenAI({ file, task, context }) {
  const settings = loadSettings();
  if (settings.mode !== "auto" || !file) return null;

  const imageUrl = await fileToDataUrl(file);
  if (!settings.apiKey && proxyReady) {
    const proxyResponse = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: settings.model,
        task,
        context,
        imageUrl,
      }),
    });
    const proxyPayload = await proxyResponse.json();
    if (!proxyResponse.ok) {
      throw new Error(proxyPayload.error || "서버 분석 실패");
    }
    return parseJsonLoose(proxyPayload.text);
  }

  if (!settings.apiKey) return null;

  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${settings.apiKey}`,
    },
    body: JSON.stringify({
      model: settings.model,
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
                `분석 작업: ${task}`,
                `사용자 입력: ${JSON.stringify(context)}`,
              ].join("\n"),
            },
            {
              type: "input_image",
              image_url: imageUrl,
              detail: "auto",
            },
          ],
        },
      ],
    }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`AI 분석 실패: ${response.status} ${detail}`);
  }

  const data = await response.json();
  return parseJsonLoose(extractResponseText(data));
}

function estimateMeal(memo, goal) {
  const text = memo.toLowerCase();
  const proteinWords = [
    "닭", "계란", "소고기", "돼지", "생선", "두부", "그릭", "프로틴", "참치",
    "닭가슴살", "닭다리", "치킨", "연어", "고등어", "새우", "오징어", "조개",
    "소시지", "햄", "낫토", "콩", "렌틸", "병아리콩", "청국장", "된장",
    "훈제", "스테이크", "삼치", "명태", "대구", "멸치", "굴",
  ];
  const carbWords = [
    "밥", "면", "빵", "감자", "고구마", "파스타", "떡", "오트",
    "쌀", "잡곡", "현미", "퀴노아", "우동", "라면", "냉면", "소면",
    "샌드위치", "피자", "토스트", "베이글", "시리얼", "그래놀라", "국수",
  ];
  const fatWords = [
    "튀김", "치즈", "마요", "버터", "삼겹", "견과", "아보카도",
    "올리브유", "크림", "기름에", "볶음", "전", "튀긴", "라드",
  ];
  const vegetableWords = [
    "샐러드", "야채", "채소", "브로콜리", "양배추", "나물",
    "시금치", "당근", "오이", "파프리카", "케일", "콩나물",
    "무", "버섯", "상추", "깻잎", "쑥갓", "토마토", "피망",
  ];

  const protein = proteinWords.some((word) => text.includes(word));
  const proteinCount = proteinWords.filter((word) => text.includes(word)).length;
  const carb = carbWords.some((word) => text.includes(word));
  const fat = fatWords.some((word) => text.includes(word));
  const vegetable = vegetableWords.some((word) => text.includes(word));

  let score = 40;
  if (protein) score += 18;
  if (proteinCount >= 2) score += 5;
  if (carb) score += goal === "감량" ? 6 : 15;
  if (vegetable) score += 15;
  if (protein && vegetable) score += 5;
  if (fat) score -= goal === "감량" ? 10 : 3;
  score = Math.max(20, Math.min(95, score));

  const missing = [];
  if (!protein) missing.push("단백질");
  if (!vegetable) missing.push("채소");
  if (!carb && goal !== "감량") missing.push("탄수화물");

  let advice;
  if (missing.length === 0) {
    if (goal === "감량") advice = "구성이 좋다. 다음 끼니도 단백질과 채소 위주로 유지하자.";
    else if (goal === "증량") advice = "균형이 잡혔다. 운동 후라면 탄수화물을 한 그릇 더 먹어도 좋다.";
    else advice = "구성이 좋다. 다음 끼니는 비슷한 단백질 양을 유지하자.";
  } else if (missing.includes("단백질") && missing.includes("채소")) {
    advice = "단백질과 채소가 모두 부족하다. 닭가슴살, 두부, 샐러드 중 하나를 추가하자.";
  } else if (missing.includes("단백질")) {
    advice = `단백질이 부족하다. 다음 끼니에 ${goal === "감량" ? "닭가슴살이나 계란" : "고기나 두부"}를 챙기자.`;
  } else if (missing.includes("채소")) {
    advice = "채소가 부족하다. 한 주먹 분량의 샐러드나 쌈채소를 곁들이면 좋다.";
  } else {
    advice = `${missing.join(", ")}을 보강하면 다음 끼니 균형이 좋아진다.`;
  }

  return {
    score,
    macro: `단백질 ${protein ? "충분" : "부족"} · 탄수화물 ${carb ? "있음" : "적음"} · 지방 ${fat ? "높음" : "보통"} · 채소 ${vegetable ? "있음" : "부족"}`,
    advice,
  };
}

function analyzeRun(km, minutes, hr) {
  const pace = km > 0 ? minutes / km : 0;
  const paceMin = Math.floor(pace);
  const paceSec = Math.round((pace - paceMin) * 60);
  const paceText = `${paceMin}'${String(paceSec).padStart(2, "0")}"/km`;
  const intensity = hr >= 165 ? "고강도" : hr >= 145 ? "중강도" : "저강도";
  const advice =
    intensity === "고강도"
      ? "다음 운동은 하체 고중량보다 회복 조깅이나 상체 위주가 좋다."
      : intensity === "중강도"
        ? "유산소 자극이 적당하다. 하체 루틴은 볼륨을 10% 줄이면 안정적이다."
        : "회복 강도에 가깝다. 근력 운동과 병행해도 부담이 낮다.";

  return { paceText, intensity, advice };
}

function normalizeMealAnalysis(aiResult, fallback) {
  if (!aiResult) return fallback;
  return {
    score: Number(aiResult.score ?? fallback.score),
    macro: String(aiResult.macro ?? aiResult.macroSummary ?? fallback.macro),
    advice: String(aiResult.advice ?? aiResult.coachAdvice ?? fallback.advice),
    calories: aiResult.calories ? Number(aiResult.calories) : undefined,
    protein: aiResult.protein ? Number(aiResult.protein) : undefined,
    carbs: aiResult.carbs ? Number(aiResult.carbs) : undefined,
    fat: aiResult.fat ? Number(aiResult.fat) : undefined,
    foodList: Array.isArray(aiResult.foodList) ? aiResult.foodList : undefined,
    detail: aiResult.detail ? String(aiResult.detail) : undefined,
    concerns: Array.isArray(aiResult.concerns) ? aiResult.concerns : undefined,
    nextMeal: aiResult.nextMeal ? String(aiResult.nextMeal) : undefined,
  };
}

function normalizeRunAnalysis(aiResult, fallback, formValues) {
  if (!aiResult) return { ...fallback, ...formValues };
  const km = Number(aiResult.km ?? aiResult.distanceKm ?? formValues.km);
  const minutes = Number(aiResult.minutes ?? aiResult.durationMinutes ?? formValues.minutes);
  const hr = Number(aiResult.hr ?? aiResult.avgHeartRate ?? formValues.hr);
  const computed = analyzeRun(km, minutes, hr);

  return {
    km,
    minutes,
    hr,
    paceText: String(aiResult.paceText ?? aiResult.pace ?? computed.paceText),
    intensity: String(aiResult.intensity ?? computed.intensity),
    advice: String(aiResult.advice ?? aiResult.coachAdvice ?? computed.advice),
    detail: aiResult.detail ? String(aiResult.detail) : undefined,
    splits: Array.isArray(aiResult.splits) ? aiResult.splits : undefined,
    trainingZone: aiResult.trainingZone ? String(aiResult.trainingZone) : undefined,
    recoveryAdvice: aiResult.recoveryAdvice ? String(aiResult.recoveryAdvice) : undefined,
    nextSession: aiResult.nextSession ? String(aiResult.nextSession) : undefined,
    calories: aiResult.calories ? Number(aiResult.calories) : undefined,
  };
}

function guideSvg(type) {
  const common = `
    <defs>
      <style>
        .line{fill:none;stroke:#174f38;stroke-width:7;stroke-linecap:round;stroke-linejoin:round}
        .bar{stroke:#286e9e;stroke-width:8;stroke-linecap:round}
        .thin{fill:none;stroke:#8aa09a;stroke-width:4;stroke-linecap:round}
        .plate{fill:#dfe9f2;stroke:#286e9e;stroke-width:3}
        .head{fill:#287654}
      </style>
    </defs>`;
  const svgs = {
    bench: `${common}<path class="thin" d="M28 93h164M52 78h96"/><circle class="head" cx="78" cy="61" r="10"/><path class="line" d="M88 66l34 14M65 77l64 3M58 80l-18 24M136 82l20 22"/><path class="bar" d="M46 42h132"/><rect class="plate" x="31" y="32" width="15" height="20" rx="3"/><rect class="plate" x="178" y="32" width="15" height="20" rx="3"/>`,
    row: `${common}<circle class="head" cx="76" cy="44" r="10"/><path class="line" d="M86 50l44 24M85 52l-22 36M130 74l30 23M118 68l22-24"/><path class="bar" d="M86 101h106"/><rect class="plate" x="70" y="91" width="16" height="20" rx="3"/><rect class="plate" x="192" y="91" width="16" height="20" rx="3"/>`,
    press: `${common}<circle class="head" cx="108" cy="54" r="10"/><path class="line" d="M108 66v41M108 77l-26 18M108 77l26 18M95 108l-18 29M121 108l18 29M82 95l-4-54M134 95l4-54"/><path class="bar" d="M63 35h90"/><rect class="plate" x="49" y="25" width="14" height="20" rx="3"/><rect class="plate" x="153" y="25" width="14" height="20" rx="3"/>`,
    pulldown: `${common}<path class="thin" d="M50 30h116M108 30v22"/><circle class="head" cx="108" cy="66" r="10"/><path class="line" d="M108 78v36M108 86l-34-18M108 86l34-18M92 115l-20 28M124 115l20 28"/><path class="bar" d="M55 48h106"/>`,
    arms: `${common}<circle class="head" cx="108" cy="48" r="10"/><path class="line" d="M108 60v45M108 72l-28 20M108 72l28 20M80 92l-8 26M136 92l8 26M94 106l-14 30M122 106l14 30"/><path class="bar" d="M58 121h32M126 121h32"/>`,
    squat: `${common}<path class="bar" d="M57 45h102"/><circle class="head" cx="108" cy="61" r="10"/><path class="line" d="M108 73l-9 43M99 116l-33 24M99 116l32 22M100 80l-27-30M116 80l27-30"/><path class="thin" d="M52 142h124"/>`,
    hinge: `${common}<circle class="head" cx="82" cy="51" r="10"/><path class="line" d="M92 57l44 27M94 60l-24 44M136 84l25 35M121 76l-2 38"/><path class="bar" d="M58 119h126"/><rect class="plate" x="42" y="109" width="16" height="20" rx="3"/><rect class="plate" x="184" y="109" width="16" height="20" rx="3"/>`,
    legpress: `${common}<path class="thin" d="M44 121l49-49M55 126h76M150 45v93"/><circle class="head" cx="70" cy="80" r="10"/><path class="line" d="M80 88l34 30M112 116l33-45M108 114l-40 20"/><path class="bar" d="M139 68h42"/>`,
    legcurl: `${common}<path class="thin" d="M42 93h118M60 76h74"/><circle class="head" cx="56" cy="66" r="9"/><path class="line" d="M67 73l49 17M115 90l38 28M112 91l34-20"/><path class="bar" d="M148 119h35"/>`,
    calf: `${common}<circle class="head" cx="108" cy="43" r="10"/><path class="line" d="M108 55v52M108 69l-22 22M108 69l22 22M97 108l-9 35M119 108l9 35"/><path class="thin" d="M72 144h72M84 126h48"/><path class="bar" d="M76 58h64"/>`,
  };

  return `<svg viewBox="0 0 220 160" role="img" aria-hidden="true">${svgs[type] || svgs.squat}</svg>`;
}

function getActivePlan() {
  return activeRoutineMode === "이분할" ? splitPlans[activeSplit] : pplPlans[activeSplit];
}

function renderLiftGuide() {
  const liftValue = elements.liftName.value;
  if (liftValue === "__custom__") {
    elements.liftGuide.innerHTML = `
      <div class="lift-guide-visual" style="display:grid;place-items:center;min-height:138px">
        <p style="color:var(--muted);font-size:0.9rem;text-align:center;padding:20px">운동 자세는 직접 확인하자.</p>
      </div>
    `;
    return;
  }
  const plan = getActivePlan();
  const guide = liftGuides[liftValue] || liftGuides[plan?.[0]?.name] || liftGuides["벤치프레스"];
  const visual = guide.img
    ? `<img src="${guide.img}" alt="${escapeHtml(liftValue)} 동작 예시" loading="lazy"
         onerror="this.style.display='none';this.nextElementSibling.style.display='block'"/>
       <div style="display:none">${guideSvg(guide.svg)}</div>`
    : guideSvg(guide.svg);
  elements.liftGuide.innerHTML = `
    <div class="lift-guide-visual">${visual}</div>
    <div>
      <h4>${escapeHtml(liftValue || plan?.[0]?.name || "")}</h4>
      <ul>${guide.cues.map((cue) => `<li>${escapeHtml(cue)}</li>`).join("")}</ul>
    </div>
  `;
}

function addRecord(record) {
  const records = loadRecords();
  const newRecord = { id: createId(), date: new Date().toISOString(), ...record };
  records.push(newRecord);
  saveRecords(records);
  render();
  syncRecordToNotion(newRecord);
}

function renderSplitButtons() {
  const splitSeg = document.getElementById("splitSeg");
  if (!splitSeg) return;
  const splits = activeRoutineMode === "이분할" ? ["상체", "하체"] : ["Push", "Pull", "Legs"];
  splitSeg.style.gridTemplateColumns = `repeat(${splits.length}, 1fr)`;
  splitSeg.innerHTML = splits
    .map((split) => `<button type="button" class="segment${split === activeSplit ? " is-active" : ""}" data-split="${escapeHtml(split)}">${escapeHtml(split)}</button>`)
    .join("");
  const titleEl = document.getElementById("routineTitle");
  const descEl = document.getElementById("routineDesc");
  if (titleEl) titleEl.textContent = activeRoutineMode === "이분할" ? "오늘의 이분할" : "오늘의 PPL";
  if (descEl) descEl.textContent = activeRoutineMode === "이분할"
    ? "상체와 하체를 바꿔가며 볼륨과 컨디션을 남긴다."
    : "Push · Pull · Legs를 순환하며 볼륨과 컨디션을 남긴다.";
}

function renderSplit() {
  const plan = getActivePlan();
  if (!plan) return;
  elements.liftName.innerHTML = [
    ...plan.map((item) => `<option value="${escapeHtml(item.name)}">${escapeHtml(item.name)}</option>`),
    `<option value="__custom__">직접 입력...</option>`,
  ].join("");
  elements.splitRoutine.innerHTML = plan
    .map(
      (item) => `
        <div class="routine-item">
          <strong>${escapeHtml(item.name)}</strong>
          <span>${escapeHtml(item.target)} · ${escapeHtml(item.guide)}</span>
        </div>
      `,
    )
    .join("");
  renderLiftGuide();
}

function getWeekRecords(records) {
  const weekStart = startOfWeek(new Date());
  return records.filter((record) => new Date(record.date) >= weekStart);
}

function getLast7Days() {
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    days.push(d.toISOString().slice(0, 10));
  }
  return days;
}

function calculateStats(records) {
  const meals = records.filter((record) => record.type === "meal");
  const strength = records.filter((record) => record.type === "strength");
  const runs = records.filter((record) => record.type === "run");
  const weekWorkouts = getWeekRecords(records).filter((record) => record.type !== "meal");
  const volume = strength.reduce(
    (sum, record) => sum + Number(record.sets) * Number(record.reps) * Number(record.weight),
    0,
  );
  const distance = runs.reduce((sum, record) => sum + Number(record.km), 0);

  const last7 = getLast7Days();
  const dailyMealScores = last7.map((date) => {
    const dayMeals = meals.filter((r) => r.date.slice(0, 10) === date);
    return { date, value: dayMeals.length ? Math.round(dayMeals.reduce((s, r) => s + r.score, 0) / dayMeals.length) : 0 };
  });
  const dailyVolume = last7.map((date) => {
    const dayStrength = strength.filter((r) => r.date.slice(0, 10) === date);
    return { date, value: dayStrength.reduce((s, r) => s + Number(r.sets) * Number(r.reps) * Number(r.weight), 0) };
  });
  const dailyDistance = last7.map((date) => {
    const dayRuns = runs.filter((r) => r.date.slice(0, 10) === date);
    return { date, value: Math.round(dayRuns.reduce((s, r) => s + Number(r.km), 0) * 10) / 10 };
  });

  return { meals, strength, runs, weekWorkouts, volume, distance, dailyMealScores, dailyVolume, dailyDistance };
}

function createCoachItems(records) {
  const todayRecords = records.filter((r) => r.date.slice(0, 10) === todayKey());
  const meals = todayRecords.filter((r) => r.type === "meal");
  const lifts = todayRecords.filter((r) => r.type === "strength");
  const runs = todayRecords.filter((r) => r.type === "run");
  const hasAny = meals.length || lifts.length || runs.length;

  if (!hasAny) {
    return [
      "오늘 기록이 아직 없어요. 식단 한 장, 운동 한 세트, 러닝 결과 중 하나만 남겨도 제가 바로 분석해드릴 수 있어요.",
      "내일 제안: 지금 시작한다면 가볍게 20분 유산소나 상체 루틴 한 세션 어떨까요?"
    ];
  }

  const items = [];

  // 종합 평가
  const mealAvg = meals.length
    ? Math.round(meals.reduce((s, r) => s + r.score, 0) / meals.length) : null;
  const liftVol = lifts.reduce((s, r) => s + (r.volume || 0), 0);
  const runKm = runs.reduce((s, r) => s + (r.km || 0), 0);
  const highRpe = lifts.some((r) => Number(r.rpe) >= 9);
  const hardRun = runs.some((r) => r.intensity === "고강도");

  // 식단 코칭
  if (meals.length) {
    if (mealAvg >= 80) {
      items.push(`오늘 식단 구성 정말 잘 하셨어요 (평균 ${mealAvg}점). 단백질과 채소 밸런스가 잘 잡혀 있어요. 이 흐름 그대로 유지하시면 됩니다.`);
    } else if (mealAvg >= 60) {
      items.push(`식단 평균 ${mealAvg}점으로 무난한 수준이에요. 다음 끼니엔 정제 탄수화물 대신 현미나 고구마로 교체하고, 단백질을 30g 이상 맞춰보세요.`);
    } else {
      items.push(`식단 점수가 ${mealAvg}점으로 좀 아쉬워요. 탄수화물 과다 또는 단백질 부족이 원인일 수 있어요. 내일 아침부터 달걀 2개 + 채소로 시작해보는 건 어떨까요?`);
    }
  }

  // 헬스 코칭
  if (lifts.length) {
    if (highRpe) {
      items.push(`오늘 운동 강도가 매우 높았어요 (${Math.round(liftVol).toLocaleString("ko-KR")}kg). 근육 회복에 48시간이 필요하니 같은 부위는 모레 이후에 다시 하세요. 충분한 수면과 단백질 섭취가 지금 가장 중요합니다.`);
    } else {
      items.push(`헬스 볼륨 ${Math.round(liftVol).toLocaleString("ko-KR")}kg, 안정적인 강도였어요. 다음 세션에서는 주 동작 1개에만 2.5kg 또는 1회를 올려보세요. 점진적 과부하가 성장의 핵심입니다.`);
    }
  }

  // 러닝 코칭
  if (runs.length) {
    if (hardRun) {
      items.push(`${runKm.toFixed(1)}km 고강도 러닝, 잘 하셨어요! 하지만 내일 하체 고중량은 피하는 게 좋아요. 폼롤러 스트레칭과 충분한 수분 보충을 꼭 해주세요.`);
    } else {
      items.push(`${runKm.toFixed(1)}km 달리셨어요. 이 정도 페이스라면 헬스와 병행해도 회복에 무리가 없어요. 꾸준히 이어가면 2주 안에 체감 페이스가 달라질 겁니다.`);
    }
  }

  // 내일 제안
  const tomorrowMsg = (() => {
    if (hardRun && highRpe) return "내일 제안: 하체와 러닝 모두 고강도였으니 내일은 완전 휴식이나 가벼운 스트레칭만 하세요. 회복도 훈련입니다.";
    if (hardRun) return "내일 제안: 고강도 러닝 다음 날은 상체 루틴이 이상적이에요. 가슴·어깨·삼두 위주로 구성해보세요.";
    if (highRpe) return "내일 제안: 고강도 웨이트 후라면 내일은 30분 이하 가벼운 조깅이나 코어 루틴을 추천해요.";
    if (lifts.length && !runs.length) return "내일 제안: 오늘 근력 운동을 하셨으니 내일 20~30분 가벼운 러닝을 더하면 심폐 능력과 회복 순환에 도움이 돼요.";
    if (runs.length && !lifts.length) return "내일 제안: 러닝만 하셨다면 내일은 상체 또는 하체 근력 운동을 한 세션 넣어보세요. 근육량이 기초대사를 올려줍니다.";
    if (mealAvg && mealAvg < 65) return "내일 제안: 내일은 아침에 고단백 식사로 시작해보세요. 삶은 달걀 2개 + 통곡물 식빵 + 채소 조합이 간단하면서도 효과적이에요.";
    return "내일 제안: 오늘 기록을 바탕으로 내일도 같은 흐름을 유지해보세요. 꾸준함이 가장 강력한 루틴입니다.";
  })();
  items.push(tomorrowMsg);

  return items;
}

function renderMiniBarChart(containerId, data, colorClass) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const max = Math.max(...data.map((d) => d.value), 1);
  const W = 26, GAP = 5, H = 52;
  const totalW = data.length * W + (data.length - 1) * GAP;
  const bars = data
    .map((d, i) => {
      const x = i * (W + GAP);
      const barH = Math.max(Math.round((d.value / max) * H), d.value > 0 ? 3 : 1);
      const y = H - barH;
      const dayLabel = new Date(d.date + "T12:00:00").toLocaleDateString("ko-KR", { weekday: "narrow" });
      return `<g>
        <rect x="${x}" y="${y}" width="${W}" height="${barH}" class="chart-bar ${d.value > 0 ? colorClass : "bar-empty"}" rx="4"/>
        <text x="${x + W / 2}" y="${H + 14}" text-anchor="middle" class="bar-day-label">${escapeHtml(dayLabel)}</text>
      </g>`;
    })
    .join("");
  container.innerHTML = `<svg viewBox="0 0 ${totalW} ${H + 18}" width="100%" style="overflow:visible" aria-hidden="true">${bars}</svg>`;
}

function renderWeeklyStats(records) {
  const stats = calculateStats(records);
  renderMiniBarChart("chartMealScore", stats.dailyMealScores, "bar-green");
  renderMiniBarChart("chartVolume", stats.dailyVolume, "bar-blue");
  renderMiniBarChart("chartDistance", stats.dailyDistance, "bar-amber");
}

// ─── 통계 탭 ───────────────────────────────────────────
let activeStatsPeriod = "daily";

function getDateRange(period) {
  const now = new Date();
  const today = todayKey();
  if (period === "daily") return { start: today, end: today, label: "오늘" };
  if (period === "weekly") {
    const d = new Date(now); d.setDate(d.getDate() - 6);
    return { start: d.toISOString().slice(0, 10), end: today, label: "최근 7일" };
  }
  if (period === "monthly") {
    const d = new Date(now); d.setDate(1);
    return { start: d.toISOString().slice(0, 10), end: today, label: "이번 달" };
  }
  // yearly
  return { start: `${now.getFullYear()}-01-01`, end: today, label: `${now.getFullYear()}년` };
}

function buildBarData(records, period, accessor) {
  const { start, end } = getDateRange(period);
  const days = [];
  const cur = new Date(start + "T12:00:00");
  const endD = new Date(end + "T12:00:00");
  while (cur <= endD) {
    days.push(cur.toISOString().slice(0, 10));
    cur.setDate(cur.getDate() + 1);
  }
  // For monthly/yearly, group by week or month
  if (period === "monthly") {
    const weeks = [];
    for (let i = 0; i < days.length; i += 7) {
      const chunk = days.slice(i, i + 7);
      const val = chunk.reduce((s, d) => s + accessor(records, d), 0);
      weeks.push({ date: chunk[0], value: val });
    }
    return weeks;
  }
  if (period === "yearly") {
    const months = {};
    days.forEach((d) => {
      const m = d.slice(0, 7);
      if (!months[m]) months[m] = { date: d, value: 0 };
      months[m].value += accessor(records, d);
    });
    return Object.values(months);
  }
  return days.map((d) => ({ date: d, value: accessor(records, d) }));
}

function dayMealScore(records, date) {
  const meals = records.filter((r) => r.type === "meal" && r.date.slice(0, 10) === date);
  return meals.length ? Math.round(meals.reduce((s, r) => s + r.score, 0) / meals.length) : 0;
}
function dayVolume(records, date) {
  return records.filter((r) => r.type === "strength" && r.date.slice(0, 10) === date)
    .reduce((s, r) => s + (r.volume || 0), 0);
}
function dayDistance(records, date) {
  return records.filter((r) => r.type === "run" && r.date.slice(0, 10) === date)
    .reduce((s, r) => s + (r.km || 0), 0);
}

function renderInlineBarChart(data, colorClass, period) {
  if (!data.length) return '<p style="color:var(--muted);font-size:0.82rem;text-align:center;padding:8px 0">기록 없음</p>';
  const max = Math.max(...data.map((d) => d.value), 1);
  const bars = data.map((d) => {
    const h = Math.max((d.value / max) * 52, d.value > 0 ? 4 : 1);
    const label = period === "yearly"
      ? (d.date.slice(5, 7) + "월")
      : new Date(d.date + "T12:00:00").toLocaleDateString("ko-KR", { month: "numeric", day: "numeric" });
    return `<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:3px">
      <div style="width:100%;max-width:28px;height:${h}px;background:var(--${colorClass.replace("bar-","")});border-radius:4px;margin:0 auto"></div>
      <span style="font-size:0.62rem;color:var(--muted)">${escapeHtml(label)}</span>
    </div>`;
  }).join("");
  return `<div style="display:flex;align-items:flex-end;gap:2px;height:70px;padding-top:8px">${bars}</div>`;
}

function renderStatsContent(records, period) {
  const el = document.querySelector("#statsContent");
  if (!el) return;
  const { start, end, label } = getDateRange(period);
  const inRange = records.filter((r) => {
    const d = r.date.slice(0, 10);
    return d >= start && d <= end;
  });
  const meals = inRange.filter((r) => r.type === "meal");
  const runs = inRange.filter((r) => r.type === "run");
  const workouts = inRange.filter((r) => r.type === "strength");
  const avgScore = meals.length ? Math.round(meals.reduce((s, r) => s + r.score, 0) / meals.length) : 0;
  const totalKm = runs.reduce((s, r) => s + (r.km || 0), 0);
  const totalVol = workouts.reduce((s, r) => s + (r.volume || 0), 0);

  const mealData = buildBarData(records, period, dayMealScore);
  const volData = buildBarData(records, period, dayVolume);
  const distData = buildBarData(records, period, dayDistance);

  el.innerHTML = `
    <p style="margin:0;font-size:0.78rem;color:var(--muted);font-weight:700">${escapeHtml(label)} 요약</p>
    <div class="stats-summary-row">
      <div class="stat-chip">
        <span class="stat-chip-label">식단 점수</span>
        <span class="stat-chip-value green">${avgScore || "—"}</span>
      </div>
      <div class="stat-chip">
        <span class="stat-chip-label">러닝</span>
        <span class="stat-chip-value amber">${totalKm.toFixed(1)}km</span>
      </div>
      <div class="stat-chip">
        <span class="stat-chip-label">헬스 볼륨</span>
        <span class="stat-chip-value blue">${Math.round(totalVol).toLocaleString("ko-KR")}kg</span>
      </div>
    </div>
    <div class="stats-chart-section">
      <div class="stats-chart-row">
        <p class="stats-chart-label">식단 점수</p>
        ${renderInlineBarChart(mealData, "bar-green", period)}
      </div>
      <div class="stats-chart-row">
        <p class="stats-chart-label">헬스 볼륨 (kg)</p>
        ${renderInlineBarChart(volData, "bar-blue", period)}
      </div>
      <div class="stats-chart-row">
        <p class="stats-chart-label">러닝 (km)</p>
        ${renderInlineBarChart(distData, "bar-amber", period)}
      </div>
    </div>
  `;
}

document.querySelector("#statsPeriodTabs")?.addEventListener("click", (e) => {
  const btn = e.target.closest(".stats-period-tab");
  if (!btn) return;
  document.querySelectorAll(".stats-period-tab").forEach((b) => b.classList.remove("is-active"));
  btn.classList.add("is-active");
  activeStatsPeriod = btn.dataset.period;
  renderStatsContent(loadRecords(), activeStatsPeriod);
});

function renderDashboard(records) {
  const stats = calculateStats(records);
  const todayRecords = records.filter((record) => record.date.slice(0, 10) === todayKey());
  const mealScore = todayRecords
    .filter((record) => record.type === "meal")
    .reduce((sum, record) => sum + record.score, 0);
  const mealCount = todayRecords.filter((record) => record.type === "meal").length;
  const hasWorkout = todayRecords.some((record) => record.type !== "meal");
  const score = Math.min(100, Math.round((mealCount ? mealScore / mealCount : 35) + (hasWorkout ? 20 : 0)));

  document.querySelector("#mealCount").textContent = `${stats.meals.length}개`;
  document.querySelector("#strengthVolume").textContent = `${Math.round(stats.volume).toLocaleString("ko-KR")}kg`;
  document.querySelector("#runDistance").textContent = `${stats.distance.toFixed(1)}km`;
  document.querySelector("#weekWorkouts").textContent = `${stats.weekWorkouts.length}회`;
  const finalScore = records.length ? score : 0;
  document.querySelector("#balanceScore").textContent = finalScore;
  document.querySelector("#coachHeadline").textContent = createCoachItems(records)[0];
  const ring = document.querySelector("#scoreRing");
  if (ring) {
    const circumference = 314.16;
    ring.style.strokeDashoffset = circumference * (1 - finalScore / 100);
  }
}

function recordTitle(record) {
  if (record.type === "meal") return `${record.mealType} 식단`;
  if (record.type === "strength") return `${record.split} · ${record.name}`;
  return `러닝 ${record.km}km`;
}

function recordMeta(record) {
  if (record.type === "meal") {
    const nutrition = [
      record.calories ? `${record.calories}kcal 추정` : "",
      record.protein ? `단백질 ${record.protein}g 추정` : "",
    ]
      .filter(Boolean)
      .join(" · ");
    return [record.macro, nutrition, record.advice].filter(Boolean).join(" · ");
  }
  if (record.type === "strength") {
    const volume = Number(record.sets) * Number(record.reps) * Number(record.weight);
    return `${record.sets}세트 · ${record.reps}회 · ${record.weight}kg · 볼륨 ${volume.toLocaleString("ko-KR")}kg`;
  }
  return `페이스 ${record.paceText} · ${record.intensity} · ${record.advice}`;
}

function renderTimeline(records) {
  elements.timeline.innerHTML = "";
  elements.emptyState.classList.toggle("is-visible", records.length === 0);

  records
    .slice()
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .forEach((record) => {
      const item = document.createElement("li");
      item.className = "timeline-item";
      const date = new Intl.DateTimeFormat("ko-KR", {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }).format(new Date(record.date));
      item.innerHTML = `
        <div>
          <div class="timeline-title">
            <strong>${escapeHtml(recordTitle(record))}</strong>
            <span class="pill">${escapeHtml(record.typeLabel)}</span>
            <span class="pill">${date}</span>
          </div>
          <p class="timeline-meta">${escapeHtml(recordMeta(record))}</p>
        </div>
        <button class="delete-button" type="button" aria-label="기록 삭제" data-id="${record.id}">×</button>
      `;
      elements.timeline.append(item);
    });
}

function renderCoach(records) {
  const items = createCoachItems(records);
  elements.coachList.innerHTML = items.map((item, i) => {
    const isTomorrow = item.startsWith("내일 제안:");
    if (isTomorrow) {
      const text = item.replace("내일 제안: ", "");
      return `<li class="coach-tomorrow"><span class="coach-tomorrow-badge">내일 제안</span>${escapeHtml(text)}</li>`;
    }
    return `<li>${escapeHtml(item)}</li>`;
  }).join("");
}

function render() {
  const records = loadRecords();
  renderDashboard(records);
  renderCoach(records);
  renderTimeline(records);
  renderStatsContent(records, activeStatsPeriod);
}

document.getElementById("routineModeSeg")?.addEventListener("click", (event) => {
  const button = event.target.closest("[data-mode]");
  if (!button) return;
  activeRoutineMode = button.dataset.mode;
  activeSplit = activeRoutineMode === "이분할" ? "상체" : "Push";
  writeStorage(getWebStorage("localStorage"), "fit-coach-routine-mode", activeRoutineMode);
  writeStorage(getWebStorage("localStorage"), "fit-coach-active-split", activeSplit);
  document.querySelectorAll("#routineModeSeg [data-mode]").forEach((b) => {
    b.classList.toggle("is-active", b === button);
  });
  renderSplitButtons();
  renderSplit();
});

document.getElementById("splitSeg")?.addEventListener("click", (event) => {
  const button = event.target.closest("[data-split]");
  if (!button) return;
  activeSplit = button.dataset.split;
  writeStorage(getWebStorage("localStorage"), "fit-coach-active-split", activeSplit);
  document.querySelectorAll("#splitSeg [data-split]").forEach((b) => {
    b.classList.toggle("is-active", b === button);
  });
  renderSplit();
});

elements.liftName.addEventListener("change", () => {
  const isCustom = elements.liftName.value === "__custom__";
  if (elements.customLiftLabel) elements.customLiftLabel.style.display = isCustom ? "" : "none";
  if (!isCustom && elements.customLiftInput) elements.customLiftInput.value = "";
  renderLiftGuide();
});

elements.settingsForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const notionToggle = document.querySelector("#notionEnabled");
  const notionTokenEl = document.querySelector("#notionToken");
  const notionDbIdEl = document.querySelector("#notionDbId");
  const notionEnabled = notionToggle?.checked || false;
  saveSettings({
    apiKey: elements.apiKey.value.trim(),
    model: elements.modelName.value.trim(),
    mode: elements.analysisMode.value,
    notionEnabled,
    notionToken: notionTokenEl?.value.trim() || "",
    notionDbId: notionDbIdEl?.value.trim() || "",
  });
  notionReady = notionEnabled && Boolean(notionTokenEl?.value.trim()) && Boolean(notionDbIdEl?.value.trim());
  renderApiStatus();
  closeSettingsSheet();
});

elements.themeToggle?.addEventListener("click", toggleTheme);
elements.openSettings.addEventListener("click", openSettingsSheet);
elements.closeSettings.addEventListener("click", closeSettingsSheet);
elements.settingsBackdrop.addEventListener("click", closeSettingsSheet);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && elements.settingsSheet.classList.contains("is-open")) {
    closeSettingsSheet();
  }
});

[...elements.quickTabs.querySelectorAll(".quick-tab")].forEach((tab) => {
  tab.addEventListener("click", () => switchTab(Number(tab.dataset.cardIndex)));
});

function setupAttachMenu(btnId, menuId, galleryInput, cameraInput, onFile) {
  const btn = document.getElementById(btnId);
  const menu = document.getElementById(menuId);
  if (!btn || !menu) return;

  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    menu.hidden = !menu.hidden;
  });

  menu.querySelector("[data-action='camera']").addEventListener("click", () => {
    menu.hidden = true;
    cameraInput.click();
  });

  menu.querySelector("[data-action='gallery']").addEventListener("click", () => {
    menu.hidden = true;
    galleryInput.click();
  });

  document.addEventListener("click", () => { menu.hidden = true; });

  galleryInput.addEventListener("change", () => {
    const file = galleryInput.files?.[0];
    if (file) onFile(file);
  });
  cameraInput.addEventListener("change", () => {
    const file = cameraInput.files?.[0];
    if (file) onFile(file);
  });
}

function addThumb(thumbRowId, file) {
  const row = document.getElementById(thumbRowId);
  if (!row) return;
  const url = URL.createObjectURL(file);
  row.innerHTML = `<div class="photo-thumb"><img src="${url}" alt="미리보기" /><button type="button" class="thumb-remove" aria-label="제거">×</button></div>`;
  row.querySelector(".thumb-remove").addEventListener("click", () => { row.innerHTML = ""; });
}

function showMealAnalyzeButton() {
  if (elements.mealAnalyze) elements.mealAnalyze.style.display = "";
}

async function runMealAnalysis() {
  const file = elements.mealPhotoCamera?.files?.[0] || elements.mealPhoto.files?.[0];
  const goal = document.querySelector("#mealGoal").value;
  const mealType = document.querySelector("#mealType").value;
  const memo = document.querySelector("#mealMemo").value.trim();
  const fallback = estimateMeal(memo, goal);

  elements.mealAnalyze.disabled = true;
  elements.mealAnalyze.textContent = "분석 중...";
  elements.mealInsight.style.display = "";
  elements.mealInsight.textContent = "AI가 이미지를 읽는 중...";

  try {
    const aiResult = await analyzeImageWithOpenAI({
      file,
      task: "식사 사진을 보고 피트니스 코치 관점에서 상세히 분석하라. 반드시 JSON만 반환한다. 스키마: {\"score\": number(0-100, 목표 달성 적합도), \"macro\": string(단백질/탄수화물/지방/채소 한 줄 요약), \"advice\": string(다음 끼니 핵심 조언 한 문장), \"calories\": number(추정 총 kcal), \"protein\": number(추정 단백질 g), \"carbs\": number(추정 탄수화물 g), \"fat\": number(추정 지방 g), \"foodList\": [{\"name\": string, \"kcal\": number, \"note\": string}](음식별 칼로리와 한 줄 코멘트), \"detail\": string(이 식사의 전반적인 구성 평가, 3-4문장, 목표와 연계해서), \"concerns\": string[](나트륨/당분/포화지방 등 주의할 점 목록), \"nextMeal\": string(다음 끼니 구체적인 추천 메뉴 예시)}",
      context: { mealType, goal, memo },
    });
    const result = normalizeMealAnalysis(aiResult, fallback);
    const nutritionLine = [
      result.calories ? `${result.calories}kcal` : "",
      result.protein ? `단백질 ${result.protein}g` : "",
      result.carbs ? `탄수화물 ${result.carbs}g` : "",
      result.fat ? `지방 ${result.fat}g` : "",
    ].filter(Boolean).join(" · ");
    elements.mealInsight.innerHTML = [
      result.detail ? `<p>${escapeHtml(result.detail)}</p>` : "",
      result.foodList?.length
        ? `<ul style="margin:8px 0 0;padding-left:1.2em">${result.foodList.map((f) => {
            const item = typeof f === "object" ? f : { name: f };
            return `<li><strong>${escapeHtml(item.name || "")}</strong>${item.kcal ? ` ${item.kcal}kcal` : ""}${item.note ? ` — ${escapeHtml(item.note)}` : ""}</li>`;
          }).join("")}</ul>` : "",
      nutritionLine ? `<p style="margin-top:10px;font-size:0.85rem;opacity:.8">${escapeHtml(nutritionLine)}</p>` : "",
      result.concerns?.length
        ? `<p style="margin-top:8px;color:var(--amber)">⚠ ${result.concerns.map(escapeHtml).join(" · ")}</p>` : "",
      result.nextMeal ? `<p style="margin-top:8px">다음 끼니 추천: <strong>${escapeHtml(result.nextMeal)}</strong></p>` : "",
      `<p style="margin-top:8px"><strong>${escapeHtml(result.advice)}</strong></p>`,
    ].filter(Boolean).join("");
    elements.mealInsight._result = result;
    // 분석된 음식 목록을 "보이는 음식" 입력창에 자동 채움
    if (result.foodList?.length) {
      const memoEl = document.querySelector("#mealMemo");
      if (!memoEl.value.trim()) {
        memoEl.value = result.foodList
          .map((f) => (typeof f === "object" ? f.name : f))
          .join(", ");
      }
    }
  } catch (err) {
    console.error("meal analysis error:", err);
    elements.mealInsight.textContent = "분석 실패. 저장 시 로컬 추정값을 사용한다.";
  } finally {
    elements.mealAnalyze.disabled = false;
    elements.mealAnalyze.textContent = "다시 분석";
  }
}

setupAttachMenu("mealAttachBtn", "mealAttachMenu", elements.mealPhoto, elements.mealPhotoCamera, (file) => {
  addThumb("mealThumbRow", file);
  showMealAnalyzeButton();
});

elements.mealAnalyze?.addEventListener("click", runMealAnalysis);

function calcRunCalories() {
  const km = parseFloat(document.querySelector("#runKm").value) || 0;
  const minutes = parseFloat(document.querySelector("#runMinutes").value) || 0;
  if (km > 0 && minutes > 0) {
    // MET 기반 추정: 체중 70kg 기준, 달리기 MET ≈ 8~10
    const hours = minutes / 60;
    const speed = km / hours; // km/h
    const met = speed < 8 ? 8 : speed < 10 ? 9.5 : speed < 13 ? 11 : 13;
    const cal = Math.round(met * 70 * hours);
    document.querySelector("#runCalories").value = cal;
  } else {
    document.querySelector("#runCalories").value = "";
  }
}

document.querySelector("#runKm").addEventListener("input", calcRunCalories);
document.querySelector("#runMinutes").addEventListener("input", calcRunCalories);

async function autoFillRunFields(file) {
  if (!file) return;
  const submitEl = elements.runSubmit;
  const prevText = submitEl.textContent;
  submitEl.textContent = "이미지 읽는 중...";
  submitEl.disabled = true;
  try {
    const aiResult = await analyzeImageWithOpenAI({
      file,
      task: "러닝 앱 스크린샷에서 수치만 추출하라. 반드시 JSON만 반환한다. 스키마: {\"km\": number, \"minutes\": number, \"pace\": string(예: \"5'30\\\"/km\"), \"calories\": number}",
      context: {},
    });
    if (aiResult) {
      const parsed = typeof aiResult === "string" ? JSON.parse(aiResult) : aiResult;
      if (parsed.km > 0) document.querySelector("#runKm").value = parsed.km;
      if (parsed.minutes > 0) document.querySelector("#runMinutes").value = Math.round(parsed.minutes);
      if (parsed.pace) document.querySelector("#runPace").value = parsed.pace;
      if (parsed.calories > 0) {
        document.querySelector("#runCalories").value = parsed.calories;
      } else {
        calcRunCalories();
      }
    }
  } catch (e) { console.error("run autofill error:", e); }
  finally {
    submitEl.textContent = prevText;
    submitEl.disabled = false;
  }
}

setupAttachMenu("runAttachBtn", "runAttachMenu", elements.runPhoto, elements.runPhotoCamera, (file) => {
  addThumb("runThumbRow", file);
  autoFillRunFields(file);
});

elements.mealForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const mealType = document.querySelector("#mealType").value;
  const goal = document.querySelector("#mealGoal").value;
  const memo = document.querySelector("#mealMemo").value.trim();

  // 이미 분석된 결과 재사용
  const result = elements.mealInsight._result || estimateMeal(memo, goal);

  addRecord({
    type: "meal",
    typeLabel: "식단",
    mealType,
    goal,
    memo,
    ...result,
  });

  elements.mealForm.reset();
  elements.mealInsight.style.display = "none";
  elements.mealInsight._result = null;
  if (elements.mealAnalyze) { elements.mealAnalyze.style.display = "none"; elements.mealAnalyze.textContent = "분석 시작"; }
  elements.mealPreview.removeAttribute("src");
  elements.mealPreview.closest(".upload-box").classList.remove("has-image");
  if (elements.mealPreviewCamera) {
    elements.mealPreviewCamera.removeAttribute("src");
    elements.mealPreviewCamera.closest(".upload-box").classList.remove("has-image");
  }
});

elements.strengthForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const liftValue = elements.liftName.value;
  const customName = elements.customLiftInput?.value.trim();
  const name = liftValue === "__custom__" ? (customName || "커스텀 운동") : liftValue;
  addRecord({
    type: "strength",
    typeLabel: "헬스",
    split: activeSplit,
    routineMode: activeRoutineMode,
    name,
    sets: Number(document.querySelector("#liftSets").value || 0),
    reps: Number(document.querySelector("#liftReps").value || 0),
    weight: Number(document.querySelector("#liftWeight").value || 0),
    rpe: Number(document.querySelector("#liftRpe").value || 8),
  });
});

elements.runForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const km = Number(document.querySelector("#runKm").value || 0);
  const minutes = Number(document.querySelector("#runMinutes").value || 0);
  const pace = document.querySelector("#runPace").value.trim();
  const calories = Number(document.querySelector("#runCalories").value || 0);
  const fallback = analyzeRun(km, minutes, 0);
  let result = { km, minutes, paceText: pace || fallback.paceText, calories: calories || undefined, ...fallback };

  elements.runSubmit.disabled = true;
  elements.runSubmit.textContent = "분석 중";
  try {
    const file = elements.runPhotoCamera?.files?.[0] || elements.runPhoto.files?.[0];
    if (file) {
      const aiResult = await analyzeImageWithOpenAI({
        file,
        task: "러닝 앱 스크린샷을 보고 피트니스 코치 관점에서 상세히 분석하라. 반드시 JSON만 반환한다. 스키마: {\"km\": number, \"minutes\": number, \"pace\": string(평균 페이스, 예: \"5'30\\\"/km\"), \"calories\": number, \"intensity\": string(저강도/중강도/고강도), \"advice\": string(다음 운동 핵심 조언 한 문장), \"detail\": string(이번 러닝 전체 총평 3-4문장), \"splits\": string[], \"trainingZone\": string, \"recoveryAdvice\": string, \"nextSession\": string}",
        context: { km, minutes, pace, calories },
      });
      if (aiResult) {
        result = {
          ...result,
          km: aiResult.km || km,
          minutes: aiResult.minutes || minutes,
          paceText: aiResult.pace || pace || fallback.paceText,
          calories: aiResult.calories || calories || undefined,
          intensity: aiResult.intensity || fallback.intensity,
          advice: aiResult.advice || fallback.advice,
          detail: aiResult.detail,
          splits: aiResult.splits,
          trainingZone: aiResult.trainingZone,
          recoveryAdvice: aiResult.recoveryAdvice,
          nextSession: aiResult.nextSession,
        };
        // 폼 필드 업데이트
        if (aiResult.km) document.querySelector("#runKm").value = aiResult.km;
        if (aiResult.minutes) document.querySelector("#runMinutes").value = aiResult.minutes;
        if (aiResult.pace) document.querySelector("#runPace").value = aiResult.pace;
        if (aiResult.calories) document.querySelector("#runCalories").value = aiResult.calories;
      }
    }
  } catch (error) {
    console.warn(error);
  } finally {
    elements.runSubmit.disabled = false;
    elements.runSubmit.textContent = "러닝 분석 저장";
  }

  elements.runInsight.innerHTML = [
    result.detail ? `<p>${escapeHtml(result.detail)}</p>` : "",
    result.splits?.length
      ? `<ul style="margin:8px 0 0;padding-left:1.2em">${result.splits.map((s) => `<li>${escapeHtml(s)}</li>`).join("")}</ul>`
      : "",
    [result.paceText && `페이스 ${escapeHtml(result.paceText)}`, result.intensity && escapeHtml(result.intensity), result.trainingZone && escapeHtml(result.trainingZone), result.calories && `${result.calories}kcal`].filter(Boolean).join(" · ")
      ? `<p style="margin-top:10px;font-size:0.85rem;opacity:.8">${[result.paceText && `페이스 ${escapeHtml(result.paceText)}`, result.intensity && escapeHtml(result.intensity), result.trainingZone && escapeHtml(result.trainingZone), result.calories && `${result.calories}kcal`].filter(Boolean).join(" · ")}</p>`
      : "",
    result.recoveryAdvice ? `<p style="margin-top:8px">회복: ${escapeHtml(result.recoveryAdvice)}</p>` : "",
    result.nextSession ? `<p style="margin-top:4px">다음 세션: <strong>${escapeHtml(result.nextSession)}</strong></p>` : "",
    result.advice ? `<p style="margin-top:8px"><strong>${escapeHtml(result.advice)}</strong></p>` : "",
  ].filter(Boolean).join("");

  addRecord({ type: "run", typeLabel: "러닝", ...result });

  elements.runForm.reset();
  document.getElementById("runThumbRow").innerHTML = "";
});

elements.timeline.addEventListener("click", (event) => {
  const button = event.target.closest("[data-id]");
  if (!button) return;
  deleteRecordFromNotion(button.dataset.id);
  saveRecords(loadRecords().filter((record) => record.id !== button.dataset.id));
  render();
});

elements.clearAll.addEventListener("click", () => {
  if (!loadRecords().length) return;
  if (!window.confirm("모든 코칭 기록을 삭제할까요?")) return;
  saveRecords([]);
  render();
});

initTheme();
hydrateSettings();
checkProxyStatus();

(function loadRoutineState() {
  const local = getWebStorage("localStorage");
  activeRoutineMode = readStorage(local, "fit-coach-routine-mode", "이분할");
  const defaultSplit = activeRoutineMode === "이분할" ? "상체" : "Push";
  activeSplit = readStorage(local, "fit-coach-active-split", defaultSplit);
  document.querySelectorAll("#routineModeSeg [data-mode]").forEach((b) => {
    b.classList.toggle("is-active", b.dataset.mode === activeRoutineMode);
  });
})();

renderSplitButtons();
renderSplit();
render();
switchTab(0);

// PWA 설치
(function initPwaInstall() {
  const installBtn = document.getElementById("installApp");
  const iosSheet = document.getElementById("iosInstallSheet");
  const iosBackdrop = document.getElementById("iosInstallBackdrop");
  const closeIos = document.getElementById("closeIosInstall");

  const isStandalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone;
  if (isStandalone) return;

  // 항상 버튼 표시
  installBtn.removeAttribute("hidden");

  function openIosSheet() {
    iosSheet.removeAttribute("hidden");
    iosBackdrop.removeAttribute("hidden");
    iosSheet.classList.add("is-open");
    iosSheet.setAttribute("aria-hidden", "false");
    document.body.classList.add("sheet-open");
  }

  function closeIosSheet() {
    iosSheet.classList.remove("is-open");
    iosSheet.setAttribute("aria-hidden", "true");
    iosBackdrop.setAttribute("hidden", "");
    document.body.classList.remove("sheet-open");
    setTimeout(() => iosSheet.setAttribute("hidden", ""), 300);
  }

  closeIos?.addEventListener("click", closeIosSheet);
  iosBackdrop?.addEventListener("click", closeIosSheet);

  let deferredPrompt;
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
  });

  installBtn.addEventListener("click", async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      if (outcome === "accepted") installBtn.setAttribute("hidden", "");
      deferredPrompt = null;
    } else {
      openIosSheet();
    }
  });

  window.addEventListener("appinstalled", () => {
    installBtn.setAttribute("hidden", "");
  });
}());
