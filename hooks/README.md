# hooks

ai-system에서 자동으로 실행되는 hook, scheduler, trigger의 중앙 관제 폴더다.

이 저장소에서 자동화가 언제, 어디서, 무엇을 실행하는지는 먼저 이 폴더에서 확인할 수 있어야 한다.

## 원칙

- 자동화 트리거의 원본은 `hooks/` 아래에 둔다.
- Git이 실제로 실행하는 `.git/hooks/*` 파일은 설치본일 뿐이며 원본이 아니다.
- GitHub Actions처럼 플랫폼이 위치를 강제하는 경우에도 `hooks/registry.yaml`에 등록한다.
- 자동화가 호출하는 일반 유틸리티는 `scripts/`, `monitoring/`에 둘 수 있지만, 자동화 진입점과 목록은 `hooks/`에서 확인 가능해야 한다.

## Registry

```text
hooks/registry.yaml
```

자동화 목록과 실행 위치를 기록하는 중앙 인덱스다.

## Git hooks

`hooks/git/`에는 버전 관리되는 Git hook 원본을 둔다.

```text
hooks/git/pre-commit
hooks/git/pre_commit.py
```

Git이 실제로 실행하는 위치는 `.git/hooks/pre-commit`이다. 이 파일은 저장소에 커밋되지 않으므로 다음 명령으로 설치한다.

```powershell
python hooks/install.py
```

## GitHub Actions

GitHub Actions workflow 파일은 플랫폼 규칙 때문에 `.github/workflows/`에 둔다. 대신 자동화 목록과 운영 설명은 `hooks/`에서 확인할 수 있어야 한다.

```text
hooks/github/
hooks/registry.yaml
.github/workflows/
```

새 workflow를 추가하면 `hooks/registry.yaml`에도 `type: github-actions` 항목으로 등록한다.
