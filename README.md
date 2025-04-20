# 스마트팜 프로젝트

스마트팜 데이터 분석 및 관리 시스템입니다. Django 백엔드와 Next.js 프론트엔드로 구성된 풀스택 애플리케이션입니다.

## 프로젝트 구조

```
smartfarm/
├── frontend/                # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/             # Next.js App Router
│   │   │   ├── page.tsx     # 메인 페이지
│   │   │   ├── login/       # 로그인 페이지
│   │   │   ├── register/    # 회원가입 페이지
│   │   │   ├── files/       # 파일 목록 페이지
│   │   │   ├── analyze/     # 데이터 분석 페이지
│   │   │   ├── abms/        # ABMS 페이지
│   │   │   ├── merge/       # 데이터 병합 페이지
│   │   │   └── revise/      # 데이터 수정 페이지
│   │   ├── components/      # 재사용 가능한 컴포넌트
│   │   ├── lib/             # 유틸리티 라이브러리
│   │   ├── hooks/           # 커스텀 훅
│   │   ├── types/           # TypeScript 타입 정의
│   │   ├── services/        # API 서비스
│   │   ├── utils/           # 유틸리티 함수
│   │   ├── constants/       # 상수 정의
│   │   └── styles/          # 스타일 관련 파일
│   ├── public/              # 정적 파일
│   │   ├── images/          # 이미지 파일
│   └── Dockerfile           # 프론트엔드 Docker 설정
├── users/                   # 사용자 관리 앱
├── file/                    # 파일 관리 앱
├── file_data/               # 파일 데이터 처리 앱
├── farm_process/            # 농업 처리 앱
├── feature/                 # 특성 분석 앱
├── analytics/               # 데이터 분석 앱
├── common/                  # 공통 유틸리티
├── config/                  # Django 설정
├── nginx/                   # Nginx 설정
├── media/                   # 미디어 파일
├── docker-compose.yml       # Docker Compose 설정
└── Dockerfile               # 백엔드 Docker 설정
```

## 기술 스택

### 프론트엔드
- **Next.js**: React 프레임워크
- **TypeScript**: 정적 타입 지원
- **Tailwind CSS**: 유틸리티 기반 CSS 프레임워크
- **React Query**: 서버 상태 관리
- **Zustand**: 클라이언트 상태 관리
- **Axios**: HTTP 클라이언트
- **Chart.js**: 데이터 시각화
- **React Hook Form**: 폼 관리
- **Zod**: 스키마 검증

### 백엔드
- **Django**: Python 웹 프레임워크
- **Django REST Framework**: API 개발
- **SQLite**: 개발용 데이터베이스
- **Redis**: 캐싱 및 세션 관리
- **Celery**: 비동기 작업 처리
- **Pandas**: 데이터 처리
- **NumPy**: 수치 연산
- **Scikit-learn**: 머신러닝

## 실행 방법

### 개발 환경 설정

1. 저장소 클론
```bash
git clone https://github.com/yourusername/smartfarm.git
cd smartfarm
```

2. 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env
# .env 파일 편집
```

3. Docker Compose로 실행
```bash
docker compose up --build
```

4. 브라우저에서 접속
```
http://localhost:8000
```

### 개별 실행 (개발용)

#### 프론트엔드
```bash
cd frontend
npm install
npm run dev
```

#### 백엔드
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

## API 문서

API 문서는 Swagger UI를 통해 제공됩니다:
```
http://localhost:8000/api/docs/
```

## 배포

프로덕션 환경 배포는 Docker Compose를 사용합니다:

```bash
docker compose -f docker-compose.prod.yml up -d
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.