#!/bin/bash

echo "🚀 Academy Management System 배포 스크립트"
echo "=========================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 에러 처리
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo -e "${RED}❌ 오류 발생: \"${last_command}\" 명령 실패${NC}"' ERR

echo -e "${YELLOW}1. 최신 코드 가져오기...${NC}"
git pull origin main

echo -e "${YELLOW}2. 컨테이너 중지...${NC}"
docker-compose down

echo -e "${YELLOW}3. 컨테이너 재빌드 및 시작...${NC}"
docker-compose up -d --build

echo -e "${YELLOW}4. 데이터베이스 준비 대기...${NC}"
sleep 5

echo -e "${YELLOW}5. 데이터베이스 마이그레이션...${NC}"
docker-compose exec -T web python manage.py migrate --noinput

echo -e "${YELLOW}6. 정적 파일 수집...${NC}"
docker-compose exec -T web python manage.py collectstatic --noinput

echo -e "${YELLOW}7. 컨테이너 상태 확인...${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}✅ 배포 완료!${NC}"
echo ""
echo "📊 서비스 상태:"
docker-compose ps

echo ""
echo "🌐 접속 URL:"
echo "   - 메인: http://localhost"
echo "   - 관리자: http://localhost/admin"
echo ""
echo "📝 로그 확인: docker-compose logs -f web"
echo "🔄 재시작: docker-compose restart"
echo "🛑 중지: docker-compose down"
