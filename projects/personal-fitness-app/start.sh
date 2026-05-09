#!/bin/bash
cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo ".env 파일이 없습니다. 생성 후 다시 실행하세요."
  echo "필요한 항목: NOTION_TOKEN, NOTION_DATABASE_ID, OPENAI_API_KEY"
  exit 1
fi

# cloudflared 설치 확인
if ! command -v cloudflared &> /dev/null; then
  echo "cloudflared 설치 중..."
  brew install cloudflare/cloudflare/cloudflared
fi

echo "Fit Coach 서버 시작 중..."
node server.js &
SERVER_PID=$!

sleep 2

echo ""
echo "Cloudflare Tunnel 시작 중 (외부 접속 URL 생성)..."
cloudflared tunnel --url http://localhost:4173

# 터널 종료 시 서버도 종료
kill $SERVER_PID
