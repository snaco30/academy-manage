# Academy Management System

학원 관리 시스템 - Django, Docker, PostgreSQL 기반

## 🎯 주요 기능

### 📚 학생 관리
- 학생 정보 등록 및 수정
- 사진 업로드 지원
- 학생 검색 기능
- 학부모 정보 관리
- 상태 관리 (재원생, 휴원, 중단, 퇴원)

### 📅 일정 관리
- 캘린더 기반 일정 관리
- 일정 생성/수정/삭제
- 색상별 일정 분류
- 일정 등록/수정 시간 자동 표시

### ✅ 출석 관리
- 학생별 출석 체크
- 날짜별 출석 현황 조회
- 실시간 출석 업데이트

## 🛠 기술 스택

- **Backend**: Django 5.0.3
- **Database**: PostgreSQL
- **Web Server**: Nginx
- **Container**: Docker & Docker Compose
- **Frontend**: HTML, CSS (Tailwind-like), JavaScript

## 🚀 시작하기

### 필수 요구사항

- Docker
- Docker Compose

### 설치 및 실행

1. **저장소 클론**
```bash
git clone https://github.com/snaco30/academy-manage.git
cd academy-manage
```

2. **환경 변수 설정**
`.env.docker` 파일이 이미 포함되어 있습니다. 필요시 수정하세요.

3. **Docker 컨테이너 실행**
```bash
docker-compose up -d
```

4. **데이터베이스 마이그레이션**
```bash
docker-compose exec web python manage.py migrate
```

5. **관리자 계정 생성 (선택사항)**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **접속**
- 메인 페이지: http://localhost:8080
- 학생 관리: http://localhost:8080/management/
- 출석 관리: http://localhost:8080/attendance/
- 관리자 페이지: http://localhost:8080/admin/

## 📁 프로젝트 구조

```
academy-leedo/
├── backend/
│   ├── academy/              # Django 앱
│   │   ├── migrations/       # 데이터베이스 마이그레이션
│   │   ├── templates/        # HTML 템플릿
│   │   ├── models.py         # 데이터 모델
│   │   ├── views.py          # 뷰 로직
│   │   └── urls.py           # URL 라우팅
│   ├── academy_project/      # Django 프로젝트 설정
│   ├── Dockerfile            # Django 컨테이너 설정
│   ├── requirements.txt      # Python 패키지
│   └── entrypoint.sh         # 컨테이너 시작 스크립트
├── nginx/
│   └── nginx.conf            # Nginx 설정
├── docker-compose.yml        # Docker Compose 설정
└── .env.docker               # 환경 변수
```

## 🔧 주요 명령어

### Docker 관리
```bash
# 컨테이너 시작
docker-compose up -d

# 컨테이너 중지
docker-compose down

# 컨테이너 재시작
docker-compose restart

# 로그 확인
docker-compose logs -f web
```

### Django 관리
```bash
# 마이그레이션 생성
docker-compose exec web python manage.py makemigrations

# 마이그레이션 적용
docker-compose exec web python manage.py migrate

# Django 쉘
docker-compose exec web python manage.py shell
```

## 🔐 보안 설정

- CSRF 보호 활성화
- CSRF_TRUSTED_ORIGINS 설정
- 프로덕션 환경에서는 `.env.docker`의 `SECRET_KEY`와 `DEBUG` 설정 변경 필요

## 📝 데이터 모델

### Student (학생)
- 개인 정보 (이름, 전화번호, 학교, 성별 등)
- 학부모 정보
- 사진 업로드
- 출석 코드
- 상태 관리

### Schedule (일정)
- 제목, 설명
- 시작/종료 날짜 및 시간
- 색상 분류
- 생성/수정 시간 자동 기록

### Attendance (출석)
- 학생별 출석 기록
- 날짜별 출석 상태
- 체크인/체크아웃 시간

## 🌐 API 엔드포인트

- `GET /api/schedules/` - 일정 목록 조회
- `POST /api/schedules/save/` - 일정 저장
- `POST /api/schedules/delete/` - 일정 삭제
- `POST /api/attendance/update/` - 출석 업데이트

## 📄 라이선스

이 프로젝트는 개인 학습 및 사용을 위한 것입니다.

## 🤝 기여

버그 리포트나 기능 제안은 Issues를 통해 제출해주세요.

## 📧 문의

프로젝트 관련 문의사항이 있으시면 Issues를 통해 연락주세요.
