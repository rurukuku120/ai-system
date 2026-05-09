# hooks/github

GitHub Actions 자동화의 관리 문서를 둔다.

## 위치 원칙

GitHub Actions workflow 파일은 GitHub가 인식해야 하므로 반드시 다음 위치에 둔다.

```text
.github/workflows/*.yml
```

다만 ai-system의 자동화 목록과 운영 의도는 `hooks/`에서 확인할 수 있어야 한다.

```text
hooks/registry.yaml
hooks/github/
```

## 새 workflow 추가 기준

1. `.github/workflows/<name>.yml`에 실제 workflow를 만든다.
2. `hooks/registry.yaml`에 `type: github-actions` 항목으로 등록한다.
3. 필요한 helper 스크립트가 자동화 전용이면 `hooks/github/`에 둔다.
4. 사람이 수동으로도 쓰는 공용 유틸이면 `scripts/` 또는 `monitoring/`에 둔다.
