"""
UE5 HTTP Server - 언리얼 에디터 내부에서 실행
localhost:18765에서 Python 코드 실행 요청을 받음

[사용법] UE Python 콘솔에서:
exec(open("C:/tmp/ue_server.py").read())
"""
import unreal
import threading
import queue
import json
import sys
import io
from http.server import HTTPServer, BaseHTTPRequestHandler

_PORT = 18765
_cmd_queue = queue.Queue()
_result_store = {}
_result_events = {}
_cmd_counter = [0]


class _Handler(BaseHTTPRequestHandler):
    """HTTP 요청 핸들러"""

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        data = json.loads(body)
        code = data.get("code", "")

        # 커맨드 ID 생성
        _cmd_counter[0] += 1
        cmd_id = _cmd_counter[0]

        # 게임 스레드에서 실행하도록 큐에 넣기
        evt = threading.Event()
        _result_events[cmd_id] = evt
        _cmd_queue.put((cmd_id, code))

        # 결과 대기 (최대 60초)
        evt.wait(timeout=60)

        result = _result_store.pop(cmd_id, {"output": "", "error": "timeout", "success": False})
        _result_events.pop(cmd_id, None)

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        """헬스체크"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "engine": "UE5"}).encode())

    def log_message(self, format, *args):
        pass  # 로그 억제


def _tick(delta_time):
    """게임 스레드에서 실행 - 큐의 코드를 처리"""
    while not _cmd_queue.empty():
        try:
            cmd_id, code = _cmd_queue.get_nowait()
        except queue.Empty:
            break

        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = captured_out = io.StringIO()
        sys.stderr = captured_err = io.StringIO()

        success = True
        try:
            exec(code, {"unreal": unreal, "__builtins__": __builtins__})
        except Exception as e:
            print(f"Error: {e}", file=captured_err)
            success = False
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        _result_store[cmd_id] = {
            "output": captured_out.getvalue(),
            "error": captured_err.getvalue(),
            "success": success,
        }

        if cmd_id in _result_events:
            _result_events[cmd_id].set()


# 기존 서버가 있으면 정리
if "_ue_http_server" in dir():
    try:
        _ue_http_server.shutdown()
    except Exception:
        pass

if "_ue_tick_handle" in dir():
    try:
        unreal.unregister_slate_post_tick_callback(_ue_tick_handle)
    except Exception:
        pass

# 게임 스레드 틱 콜백 등록
_ue_tick_handle = unreal.register_slate_post_tick_callback(_tick)

# HTTP 서버 시작 (백그라운드 스레드)
_ue_http_server = HTTPServer(("127.0.0.1", _PORT), _Handler)
_ue_http_thread = threading.Thread(target=_ue_http_server.serve_forever, daemon=True)
_ue_http_thread.start()

unreal.log(f"=== UE HTTP Server started on http://127.0.0.1:{_PORT} ===")
