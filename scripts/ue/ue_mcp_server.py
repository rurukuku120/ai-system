"""
Unreal Engine MCP Server for Claude Code (SDK 기반)
UE5 HTTP Server(localhost:18765)와 통신하는 MCP 서버

Claude Code 설정 (.mcp.json):
{
  "mcpServers": {
    "unreal": {
      "command": "python",
      "args": ["C:/Users/cukirang/Documents/GitHub/ue_scripts/ue_mcp_server.py"]
    }
  }
}
"""
import json
import urllib.request
import urllib.error
from mcp.server.fastmcp import FastMCP

UE_URL = "http://127.0.0.1:18765"

mcp = FastMCP("unreal-engine")


def _send_to_ue(code: str) -> dict:
    """UE HTTP 서버에 Python 코드 전송"""
    data = json.dumps({"code": code}).encode("utf-8")
    req = urllib.request.Request(
        UE_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {
            "output": "",
            "error": f"UE5 연결 실패: {e}. HTTP 서버가 실행 중인지 확인하세요.",
            "success": False,
        }


@mcp.tool()
def execute_python(code: str) -> str:
    """UE5 에디터에서 Python 코드를 실행합니다. unreal 모듈이 사용 가능합니다. 결과는 print()로 출력하세요."""
    result = _send_to_ue(code)
    parts = []
    if result.get("output"):
        parts.append(result["output"])
    if result.get("error"):
        parts.append(f"[ERROR] {result['error']}")
    if not parts:
        parts.append("(실행 완료, 출력 없음)")
    return "\n".join(parts)


@mcp.tool()
def healthcheck() -> str:
    """UE5 HTTP 서버 연결 상태를 확인합니다."""
    try:
        req = urllib.request.Request(UE_URL, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.dumps(
                json.loads(resp.read().decode("utf-8")),
                indent=2,
                ensure_ascii=False,
            )
    except Exception as e:
        return json.dumps(
            {"status": "disconnected", "error": str(e)},
            indent=2,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    mcp.run(transport="stdio")
