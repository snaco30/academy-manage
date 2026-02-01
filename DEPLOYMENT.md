# 웹서버 배포 가이드

학원 관리 시스템을 실제 웹서버에 배포하는 방법을 단계별로 안내합니다.

## 📋 사전 준비사항

### 1. 서버 요구사항
- **OS**: Ubuntu 20.04 LTS 이상 (또는 CentOS, Debian 등)
- **RAM**: 최소 2GB (권장 4GB)
- **저장공간**: 최소 10GB
- **포트**: 80, 443 (HTTP/HTTPS)

### 2. 필요한 소프트웨어
- Docker
- Docker Compose
- Git

---

## 🚀 배포 방법

### 방법 1: Docker를 사용한 배포 (권장)

#### Step 1: 서버 접속
```bash
ssh username@your-server-ip
```

#### Step 2: Docker 설치
```bash
# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER
newgrp docker
```

#### Step 3: 프로젝트 클론
```bash
cd /home/$USER
git clone https://github.com/snaco30/academy-manage.git
cd academy-manage
```

#### Step 4: 환경 변수 설정
```bash
# .env.docker 파일 수정
nano .env.docker
```

**중요 설정 변경:**
```env
DEBUG=0
SECRET_KEY=your-very-secret-key-here-change-this-in-production
ALLOWED_HOSTS=your-domain.com,your-server-ip

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=academy_db
SQL_USER=academy_user
SQL_PASSWORD=strong-password-here
SQL_HOST=db
SQL_PORT=5432
```

#### Step 5: 프로덕션용 설정 추가

**nginx/nginx.conf 수정** (포트 80으로 변경):
```bash
nano nginx/nginx.conf
```

```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name your-domain.com;  # 도메인 또는 IP 주소로 변경

    client_max_body_size 10M;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

**docker-compose.yml 수정** (포트 변경):
```bash
nano docker-compose.yml
```

nginx 포트를 80:80으로 변경:
```yaml
  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"  # 8080에서 80으로 변경
```

#### Step 6: 컨테이너 실행
```bash
# 컨테이너 빌드 및 실행
docker-compose up -d --build

# 데이터베이스 마이그레이션
docker-compose exec web python manage.py migrate

# 정적 파일 수집
docker-compose exec web python manage.py collectstatic --noinput

# 관리자 계정 생성
docker-compose exec web python manage.py createsuperuser
```

#### Step 7: 방화벽 설정
```bash
# Ubuntu/Debian
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

#### Step 8: 서비스 확인
```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f web
```

브라우저에서 `http://your-server-ip` 접속하여 확인!

---

## 🔒 HTTPS 설정 (SSL/TLS)

### Let's Encrypt를 사용한 무료 SSL 인증서

#### Step 1: Certbot 설치
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```

#### Step 2: SSL 인증서 발급
```bash
# 먼저 nginx 컨테이너 중지
docker-compose stop nginx

# 인증서 발급
sudo certbot certonly --standalone -d your-domain.com

# nginx 재시작
docker-compose start nginx
```

#### Step 3: Nginx SSL 설정

**nginx/nginx.conf에 SSL 설정 추가:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    client_max_body_size 10M;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

**docker-compose.yml에 SSL 볼륨 추가:**
```yaml
  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - /etc/letsencrypt:/etc/letsencrypt:ro  # SSL 인증서 추가
```

#### Step 4: 재시작
```bash
docker-compose down
docker-compose up -d
```

---

## 🔄 업데이트 및 유지보수

### 코드 업데이트
```bash
cd /home/$USER/academy-manage

# 최신 코드 가져오기
git pull origin main

# 컨테이너 재빌드 및 재시작
docker-compose down
docker-compose up -d --build

# 마이그레이션 실행
docker-compose exec web python manage.py migrate

# 정적 파일 재수집
docker-compose exec web python manage.py collectstatic --noinput
```

### 백업
```bash
# 데이터베이스 백업
docker-compose exec db pg_dump -U academy_user academy_db > backup_$(date +%Y%m%d).sql

# 미디어 파일 백업
tar -czf media_backup_$(date +%Y%m%d).tar.gz backend/media/
```

### 로그 확인
```bash
# 전체 로그
docker-compose logs

# 특정 서비스 로그
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# 실시간 로그
docker-compose logs -f web
```

---

## 🛠 문제 해결

### 컨테이너가 시작되지 않을 때
```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs

# 컨테이너 재시작
docker-compose restart
```

### 데이터베이스 연결 오류
```bash
# DB 컨테이너 상태 확인
docker-compose exec db pg_isready -U academy_user

# DB 재시작
docker-compose restart db
```

### 정적 파일이 로드되지 않을 때
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

---

## 📊 모니터링

### 리소스 사용량 확인
```bash
# 컨테이너 리소스 사용량
docker stats

# 디스크 사용량
df -h

# 메모리 사용량
free -h
```

### 자동 재시작 설정
**docker-compose.yml에 restart 정책 추가:**
```yaml
services:
  web:
    restart: always
  db:
    restart: always
  nginx:
    restart: always
```

---

## 🔐 보안 체크리스트

- [ ] DEBUG=0으로 설정
- [ ] SECRET_KEY 변경
- [ ] 강력한 데이터베이스 비밀번호 설정
- [ ] ALLOWED_HOSTS 설정
- [ ] CSRF_TRUSTED_ORIGINS 설정
- [ ] 방화벽 설정
- [ ] SSL/TLS 인증서 설치
- [ ] 정기적인 백업 설정
- [ ] 로그 모니터링 설정

---

## 📞 추가 도움말

### AWS EC2 배포 시
1. EC2 인스턴스 생성 (Ubuntu 20.04)
2. 보안 그룹에서 포트 80, 443 열기
3. Elastic IP 할당
4. 위의 배포 방법 따라하기

### 도메인 연결
1. 도메인 구매 (가비아, 호스팅케이알 등)
2. DNS A 레코드를 서버 IP로 설정
3. nginx.conf의 server_name을 도메인으로 변경

### 성능 최적화
- Gunicorn workers 수 조정 (CPU 코어 수 × 2 + 1)
- PostgreSQL 설정 튜닝
- Nginx 캐싱 설정
- CDN 사용 고려

---

## 🎯 빠른 배포 스크립트

전체 과정을 자동화한 스크립트:

```bash
#!/bin/bash
# deploy.sh

echo "🚀 Academy Management System 배포 시작..."

# 1. 코드 업데이트
git pull origin main

# 2. 컨테이너 중지
docker-compose down

# 3. 컨테이너 재빌드
docker-compose up -d --build

# 4. 마이그레이션
docker-compose exec -T web python manage.py migrate

# 5. 정적 파일 수집
docker-compose exec -T web python manage.py collectstatic --noinput

# 6. 상태 확인
docker-compose ps

echo "✅ 배포 완료!"
```

사용법:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

이 가이드를 따라하시면 웹서버에 성공적으로 배포할 수 있습니다! 🎉
