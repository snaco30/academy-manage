# 프로젝트: 학원 관리 시스템 (Academy Management System)
## 모듈: 학생 관리 페이지 (Student Management)
### 문서: aiagent.md (확장 통합 명세)
- 작성일: 2026-02-01
- 목적: 학생 관리(관리자/선생님) + 학생 포털(학생) + 숙제/통계 + Excel 비식별화 + 메뉴 UX 규칙을 **하나의 기준 문서**로 고정

---

## 1. 개요 (Overview)
이 문서는 학원 관리 시스템의 **학생 관리 페이지** 및 관련 기능(학생 포털/숙제/통계/Excel)의 명세서입니다.  
전체 레이아웃은 **좌측 목록(Sidebar)**과 **우측 상세 정보(Main Content)**로 구성된 **Master–Detail 구조**입니다.  
시스템은 Docker 기반으로 배포되며, 파이썬(백엔드)과 리액트(프론트엔드)를 사용합니다.

---

## 2. 시스템 아키텍처 및 기술 스택 (System Architecture)

### 2.1 기술 스택
- **Frontend:** React (Vite 권장), Tailwind CSS
- **Backend:** Python (FastAPI 또는 Django)
- **Database:** PostgreSQL
- **Web Server:** Nginx (Reverse Proxy)
- **Infrastructure:** Docker & Docker Compose

### 2.2 배포 구조
1. **Nginx:** 80 포트 리스닝, `/api`는 백엔드로, 나머지는 프론트엔드로 라우팅
2. **Frontend:** Node.js 빌드 후 정적 파일 서빙
3. **Backend:** Python WSGI/ASGI 서버 구동
4. **DB:** PostgreSQL (데이터 볼륨 마운트 필수)

---

## 3. 데이터 필드 명세 (Data Schema)
손그림(Wireframe)에 명시된 모든 필드를 포함합니다.

| 필드명 | 변수명 | 타입 | 필수 | UI 컴포넌트 | 설명 및 로직 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **학생 사진** | `profile_image` | File | Optional | Image Uploader | 1MB 제한, PNG/JPG, 기본 실루엣 아이콘 |
| 학생명 | `student_name` | String | **Required** | Text Input | |
| **출결코드** | `attendance_code` | String | Required | Text Input | 등하원 키패드 입력용 코드 (4-6자리) |
| **학생 ID(폰번호)** | `student_phone` | String | Required | Text Input | 로그인 ID 생성의 기준이 되는 전화번호 |
| **비밀번호** | `password` | String | Required | Password Input | 학생 로그인용 (DB 저장 시 Hash 필수) |
| 성별 | `gender` | Enum | Required | Toggle/Radio | 남/여 |
| 학부모명 | `parent_name` | String | Optional | Text Input | |
| 학부모 연락처 | `parent_phone` | String | **Required** | Text Input | SMS 발송용 |
| 학교명 | `school_name` | String | Optional | Text Input | |
| 주소 | `address` | String | Optional | Address Search | 우편번호 검색 API 연동(카카오 등) |
| 상세주소 | `address_detail` | String | Optional | Text Input | |
| 생년월일 | `birth_date` | Date | Optional | Date Input | |
| 등록일 | `enrollment_date` | Date | Required | Date Picker | |
| **납입일** | `payment_day` | Number | Optional | Number Input | 매월 결제일(예: 25일) |
| **담당자** | `manager_name` | String | Optional | Text Input | 담당 선생님 이름 |
| **상태** | `status` | Enum | Required | Select/Toggle | 재원생(Active), 휴원, 퇴원 |

---

## 4. 화면 레이아웃 (UI/UX Layout Specifications)
화면은 **좌측(검색/목록)**과 **우측(상세/등록)**으로 2분할(Split View) 됩니다.

### 4.1 좌측 사이드바 (List & Search) - Width: 250px~300px
1. **검색 영역**
   - 상단에 `[이름]` 입력창과 `[검색]` 버튼 배치
2. **학생 목록**
   - 세로 스크롤 가능한 리스트
   - 각 아이템: **이름 (학교명)** (예: "김시현 (보람초)")
   - 클릭 시 우측 영역에 해당 학생 상세 정보 로드

### 4.2 우측 메인 영역 (Detail & Form) - Width: Flex

#### 4.2.1 상단 툴바 (Top Actions)
- 좌측: `[신규]`(폼 초기화), `[출력]`, `[저장]`(DB 반영)
- 중앙: `[Excel]`(현재 데이터 엑셀 다운로드)
- 우측: `상태: [재원생]` (드롭다운/토글)

#### 4.2.2 상세 정보 입력 폼 (Grid Layout)
- **사진 영역(좌측 상단)**:
  - 약 150x150px
  - 하단에 `[신규]`, `[수정]`, `[삭제]` 텍스트 버튼
  - 로직: 이미지 없으면 실루엣 표시, 업로드 시 1024KB/JPG,PNG 제한 체크
- **정보 입력 영역(사진 우측 및 하단)**:
  - 손그림 배치를 존중하여 Grid로 그룹 배치
  - 예: `학생명` 옆 `출결코드`, `학생폰번` 옆 `성별`

#### 4.2.3 하단 위젯 영역 (Bottom Widgets)
- **메모(Memo History) - 좌측**
  - 최근 상담/특이사항 기록 리스트
  - `[날짜] 내용...` 형태로 최근 3~4건
- **출석 달력(Attendance Calendar) - 우측**
  - 이번 달 달력(Mini Calendar) 표시
  - 등원한 날짜 Highlight
  - `<< 1월 >>` 네비게이션 + `[5회 출석]` 요약 카운트

---

## 5. 기능적 요구사항 (Functional Requirements)

### 5.1 이미지 처리 (Strict)
- 업로드 시 Client Side에서 파일 크기(1024KB 이하) 및 확장자(jpg, png) 검사 필수
- 위반 시 `alert` 경고

### 5.2 데이터 저장 흐름
- `[신규]` → 우측 폼 비우기(Create Mode)
- `[저장]` →
  - 신규: `POST /students`
  - 수정: `PUT /students/{id}`
- 성공 시 좌측 리스트 갱신

### 5.3 엑셀 다운로드
- `[Excel]` 클릭 시 현재 필터링된 학생 리스트 `.xlsx` 다운로드(Backend 권장)

---

## 6. 참고 사항 (AI Instruction)
- 깔끔하고 직관적인 **Dashboard 스타일**
- 폼은 `gap/padding` 충분히 확보(빽빽 금지)
- 손그림의 배치(파란 선/글씨)를 최대한 존중

---

## 7. Excel 다운로드 및 개인정보 보호 규칙 (Excel & Privacy Policy)
- Excel은 외부 공유 가능 문서로 간주
- DB 원본 데이터는 변경하지 않음
- Excel 출력 시 회원가입 및 개인식별 정보는 원본 그대로 노출 금지

---

## 8. Excel 변환 대상 필드 및 처리 방식 (Mandatory)

| 원본 필드 | 변수명 | 처리 방식 | Excel 출력 예시 |
|---|---|---|---|
| 학생명 | `student_name` | 가명 치환 | 학생001 |
| 학생 전화번호 | `student_phone` | 가상번호 치환 | 010-0000-0001 |
| 출결코드 | `attendance_code` | 랜덤 재생성 | A9F3 |
| 비밀번호/해시 | `password`/`password_hash` | **출력 금지(컬럼 제거)** | - |
| 학부모명 | `parent_name` | 가명 치환 | 보호자001 |
| 학부모 연락처 | `parent_phone` | 마스킹 | 010-****-1234 |
| 주소 | `address` | 축약 | 서울시 ○○구 |
| 상세주소 | `address_detail` | **출력 금지(컬럼 제거)** | - |
| 사진 | `profile_image` | **출력 금지(컬럼 제거)** | - |

---

## 9. Excel 유지 허용 필드 (Allowed Fields)
- `school_name`, `gender`
- `birth_date`는 **연도만 표시(YYYY) 권장**
- `enrollment_date`, `payment_day`, `manager_name`, `status`
- 출석 요약(월 출석 횟수)

---

## 10. Excel 가명 생성 규칙 (Deterministic Rule)
- 동일 Excel 파일 내에서 같은 학생은 항상 같은 가명
- 기본 규칙: `학생{index:03d}`, `보호자{index:03d}`

---

## 11. Excel UI 안내 문구 (Mandatory)
Excel 다운로드 시 다음 안내 문구를 표시:
> “본 엑셀 파일에는 개인정보 보호를 위해 일부 정보가 가명 또는 마스킹 처리되어 포함됩니다.”

---

## 12. Excel 권한 레벨 정책 (Authorization)
| 권한 | Excel 유형 |
|---|---|
| STAFF | 비식별화 Excel |
| MANAGER | 비식별화 Excel |
| ADMIN | 비식별화 Excel(기본) + 원본 Excel(선택) |

---

## 13. 원본 Excel (ADMIN 전용)
- 기본 UI 비노출(관리자 전용 화면/버튼에서만)
- 원본 Excel 다운로드 시 감사 로그 필수

---

## 14. 다운로드 감사 로그 (Audit)
- Excel 다운로드 이벤트 기록:
  - 시각, 사용자, action, type(ANONYMIZED/RAW_EXPORT), 필터 조건(기간/클래스 등)

---

## 15. AI 데이터 보호 판단 우선순위
1) 개인정보 보호  
2) 운영 리스크 최소화  
3) 유지보수성  
4) 개발 편의성  

---

## 16. 상담 메모 접근 정책 (Consultation Memo Policy)
- 상담 메모는 **학원 내부 사용자(직원/선생님/관리자) 누구나** 조회 가능
- 상담 메모는 **학원 내부 운영 정보**이며, 학생 포털에는 노출하지 않는다

---

## 17. 학생 로그인 계정 발급 규칙 (Student Account Policy)
- 학생 신규 등록 시 자동으로 학생 로그인 계정 생성
- 로그인 ID = 학생 전화번호 **뒤 4자리**
- 초기 비밀번호 = `stu` + 전화번호 뒤 4자리 (예: `stu5678`)
- 비밀번호는 DB에 평문 저장 금지(해시 저장 필수)
- 최초 로그인 후 비밀번호 변경 가능(강제 아님)

---

## 18. 학생 포털 개인정보 최소화 정책 (Student Portal Minimum PII)
학생 포털에는 최소한의 개인정보만 표시한다.

| 항목 | 표시 |
|---|---|
| 학생명 | ⭕ |
| 전화번호/주소/학부모정보/출결코드/성별/생년월일 | ❌ |
| 상태(재원/휴원/퇴원) | ❌(내부 관리용) |

---

## 19. 학생 포털 제공 기능 (Student Portal Features)
- 본인 **현재 수강중인 클래스** 조회
- 숙제:
  - 숙제 확인
  - 지난 숙제 확인
  - 숙제 업로드 상황/미제출 숙제 확인
  - 숙제 제출 등록/수정/삭제

---

## 20. 숙제 목록 분류 (Homework Tabs)
- 현재 숙제(Current)
- 미제출 숙제(Overdue)
- 지난 숙제(Past)

---

## 21. 숙제 제출 기능 (Homework Submission)
- 파일 업로드 제출(기본: 1개)
- 제출 상태: 미제출/제출 완료/수정 제출/지각 제출
- 마감 전: 수정/삭제 가능
- 마감 후: 수정 가능(지각 제출), 삭제 불가

---

## 22. 학생 포털 접근 제한 (Access Control)
학생 계정은 아래 기능만 접근:
- 본인 클래스 조회
- 숙제 확인/제출/수정/삭제
- (확장) 본인 출결 조회(읽기 전용)
관리자/선생님 페이지 접근 불가

---

## 23. 관리자·선생님 숙제 관리 메뉴 (Homework Management for Staff)
관리자/선생님 로그인 시 숙제 제출 관련 확인 및 통계 메뉴를 제공한다.
- 제출 현황 조회(리스트)
- 기간/클래스/상태/학생명 필터
- 통계(KPI/그래프/Top 리스트)

---

## 24. 숙제 관리 메뉴 위치 (Navigation)
좌측 사이드바:
- 학사관리 > 숙제관리
- 통계관리 > 숙제통계(선택)

---

## 25. 숙제 관리 화면 구성 (Dashboard)
### 25.1 필터 바
- 클래스(전체/특정)
- 기간(이번주/이번달/사용자지정)
- 제출 상태(전체/제출/미제출/지각/수정)
- 학생명 검색

### 25.2 제출 현황 리스트 컬럼(권장)
- 학생명, 클래스명, 숙제 제목, 제출 상태, 제출 일시, 마감일, 파일 다운로드

---

## 26. 숙제 제출 통계 (Statistics)
- KPI: 전체 숙제 수, 제출률, 미제출 수, 지각 제출 수
- 그래프: 제출률 추이, 클래스별 비교, 미제출 TOP

---

## 27. 권한별 데이터 범위 제한 (RBAC Scope)
- 선생님: 담당 클래스 범위만 조회/통계
- 관리자: 전체 조회/통계

---

## 28. 좌측 메뉴 접기/펼치기 (Collapsible Sidebar)
- 관리자/선생님 좌측 메뉴는 **접기/펼치기(Accordion)** 지원
- 대분류/소분류 계층 구조
- 페이지 이동 후에도 열린 상태 유지(localStorage 권장)
- 권한 없는 메뉴는 비활성화가 아니라 **미표시**

---

## 29. 메뉴 트리 예시 (Menu Tree Example)
```
학사관리 ▼
  - 학생관리
  - 클래스관리
  - 숙제관리
  - 출결관리

통계관리 ▶
  - 숙제통계
  - 출결통계

시스템 ▶
  - 사용자관리
  - 설정
```

---

## 30. UI/UX 저장 후 동작(권장)
- 저장 성공 토스트: “저장되었습니다”
- 좌측 리스트 자동 갱신
- 저장한 학생 자동 선택 유지
- `[출력]`: 학생 상세를 프린트(PDF/print CSS)로 출력

---

## 31. 추가 디테일: 로그인/권한 상세 규칙 (Auth Specification)

### 31.1 사용자 유형
- STUDENT / TEACHER / ADMIN

### 31.2 학생 ID 중복 처리(필수 규칙)
전화번호 뒤 4자리는 중복될 수 있으므로 중복 시 확장 규칙 적용:
- 기본: `5678`
- 중복 시: `5678-1`, `5678-2` …
- 학생 안내: “아이디가 중복되면 자동으로 확장된 아이디가 부여됩니다.”

> 구현 권장: `student_login_id` 별도 UNIQUE 필드

---

## 32. 추가 디테일: 데이터 관계 (Data Relationships)
- Student : Class = N:M (수강 관계 Enrollment)
- Class : Homework = 1:N
- Homework : Submission = 1:N (학생별 1개 제출 원칙)
- Student : Submission = 1:N

---

## 33. 추가 디테일: 파일 업로드 정책 (Upload Policy)
### 33.1 숙제 업로드
- 허용 확장자(기본): pdf, jpg, jpeg, png, docx
- 최대 용량(기본): 10MB
- 저장 위치(기본): `/data/uploads/submissions/`
- 파일명 규칙(권장): `{student_id}_{homework_id}_{uuid}.{ext}`

---

## 34. 추가 디테일: Excel 비식별화 결정적 매핑 (Deterministic Export)
- 필터/정렬이 바뀌어도 가명/가상번호가 바뀌지 않도록 결정적 매핑 권장
- 권장 방식: 내부 고유키(student_id) 기반 해시로 `학생XYZ` 생성

---

## 35. 구현 시 API 라우팅 규칙 (Nginx)
- `/api/*` → backend
- `/` 및 나머지 → frontend 정적 파일

---

## 36. 최종 선언 (AI Compliance)
AI는 위 명세를 우선하며, 모호한 경우 **더 보수적(개인정보 보호/권한 제한)인 방향**으로 구현한다.
