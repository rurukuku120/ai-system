"""
ue_send.py
VSCode에서 현재 .py 파일을 UE5로 전송 실행
사용법: python ue_send.py <전송할_파일경로>
"""

import sys
import os

# remote_execution.py가 같은 폴더에 있어야 함
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import remote_execution as remote
except ImportError:
    print("=" * 50)
    print("[오류] remote_execution.py 없음")
    print("아래 경로에서 복사해주세요:")
    print("C:/Program Files/Epic Games/UE_5.x/Engine/Plugins/Experimental/PythonScriptPlugin/Content/Python/remote_execution.py")
    print("→ 이 파일(ue_send.py)과 같은 폴더에 붙여넣기")
    print("=" * 50)
    sys.exit(1)

def send_to_ue(script_path):
    if not os.path.exists(script_path):
        print(f"[오류] 파일 없음: {script_path}")
        sys.exit(1)

    with open(script_path, 'r', encoding='utf-8') as f:
        code = f.read()

    print(f"[UE5] 전송 중: {os.path.basename(script_path)}")

    try:
        config = remote.RemoteExecutionConfig()
        config.multicast_bind_address = '0.0.0.0'
        config.multicast_ttl = 0
        config.command_endpoint = ('0.0.0.0', 6776)
        rc = remote.RemoteExecution(config)
        rc.start()

        # UE 에디터가 열려있는 노드 탐색 (최대 3초 대기)
        timeout = 3.0
        import time
        elapsed = 0.0
        while not rc.remote_nodes and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1

        if not rc.remote_nodes:
            print("[오류] UE5 에디터에 연결할 수 없음")
            print("확인사항:")
            print("  1. UE5 에디터가 실행 중인지 확인")
            print("  2. Project Settings > Python > 원격 실행 활성화 체크 확인")
            rc.stop()
            sys.exit(1)

        rc.open_command_connection(rc.remote_nodes)
        result = rc.run_command(code, unattended=True)
        rc.stop()

        # 결과 출력
        if result and result.get('output'):
            for line in result['output']:
                print(f"[UE] {line.get('output', '')}")

        print(f"[UE5] 실행 완료: {os.path.basename(script_path)}")

    except Exception as e:
        print(f"[오류] 연결 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python ue_send.py <파일경로>")
        sys.exit(1)

    send_to_ue(sys.argv[1])
