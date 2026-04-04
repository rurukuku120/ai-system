#!/bin/bash
# VFX 평가 결과 자동 제출 스크립트
# 사용법: ./vfx-submit.sh "2026-04-04_스킬이름"

set -e

if [ -z "$1" ]; then
  echo "[오류] 파일명을 입력해주세요."
  echo "사용법: ./vfx-submit.sh \"2026-04-04_스킬이름\""
  exit 1
fi

FILENAME="$1"
JSON_PATH="projects/nexon/mabinogi-eternity/evaluations/results/${FILENAME}.json"
REPO_ROOT="$(git rev-parse --show-toplevel)"

cd "$REPO_ROOT"

if [ ! -f "$JSON_PATH" ]; then
  echo "[오류] 파일을 찾을 수 없습니다: $JSON_PATH"
  exit 1
fi

echo "[1/3] 원격 변경사항 동기화 중..."
git pull origin main --rebase

echo "[2/3] 파일 스테이징 및 커밋 중..."
git add "$JSON_PATH"
git commit -m "Add VFX evaluation: ${FILENAME}"

echo "[3/3] 원격 저장소에 푸시 중..."
git push origin main

echo ""
echo "완료: ${FILENAME}.json 이 Git에 저장되었습니다."
echo "다음 단계: Claude에게 Notion 등록 요청"
