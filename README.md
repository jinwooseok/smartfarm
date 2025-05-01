# 스마트팜 프로젝트

스마트팜 데이터 분석 및 관리 시스템입니다. Django로 구성된 풀스택 애플리케이션입니다.

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
