# kweblog

[assignment link](https://kwebofficial.notion.site/2025-16355c7781bc80a09841feaf1c141070)

## 모의 실행 환경 구성 (파이썬 설치 필수)

### 로컬 가상 환경 구성 (선택)

```
>>python -m venv venv
>>.\venv\Scripts\activate
```

### 의존성 설치 명령어

```
>>pip install -r requirements.txt
```

### .env 파일 작성

#### 예시 데이터가 포함된 db 사용 시 SECRET_KEY를 그대로 사용 해야합니다!

```
FLASK_APP=app.py
FLASK_ENV=development

SECRET_KEY=89ced2322b6dafbf56fc29f4e80c925bb52da9d33d67fc92
SQLALCHEMY_DATABASE_URI = sqlite:///kweblog.db
```

### 실행 명령어 및 로컬 접속 url

```
>>python app.py
```

[127.0.0.1:5000](http://127.0.0.1:5000)

### 사용자명 및 비밀번호 (포함된 예시 데이터)

```
username: user1
password: T5+L8}Ew
```

## API 명세

### 인증 관련 API

| 엔드포인트  | 메소드 | 설명            | 인증 필요 |
| ----------- | ------ | --------------- | --------- |
| `/register` | GET    | 회원가입 페이지 | 아니오    |
| `/register` | POST   | 회원가입 처리   | 아니오    |
| `/login`    | GET    | 로그인 페이지   | 아니오    |
| `/login`    | POST   | 로그인 처리     | 아니오    |
| `/logout`   | GET    | 로그아웃 처리   | 예        |

### 메인 및 프로필 관련 API

| 엔드포인트            | 메소드 | 설명                 | 인증 필요 |
| --------------------- | ------ | -------------------- | --------- |
| `/`                   | GET    | 메인 페이지          | 아니오    |
| `/profile/<username>` | GET    | 사용자 프로필 페이지 | 아니오    |
| `/edit_profile`       | GET    | 프로필 편집 페이지   | 예        |
| `/edit_profile`       | POST   | 프로필 편집 처리     | 예        |
| `/request_friend`     | POST   | 서로이웃 요청 전송   | 예        |
| `/remove_friend`      | POST   | 서로이웃 삭제        | 예        |
| `/accept_friend`      | POST   | 서로이웃 승인        | 예        |
| `/reject_friend`      | POST   | 서로이웃 거부        | 예        |
| `/saved_posts`        | GET    | 저장한 게시물 보기   | 예        |

### 게시물 관련 API

| 엔드포인트                | 메소드 | 설명                  | 인증 필요 |
| ------------------------- | ------ | --------------------- | --------- |
| `/new_post`               | GET    | 새 게시물 작성 페이지 | 예        |
| `/new_post`               | POST   | 게시물 작성 처리      | 예        |
| `/post/<post_id>`         | GET    | 게시물 상세 페이지    | 아니오    |
| `/post/<post_id>/comment` | POST   | 댓글 작성 처리        | 예        |
| `/post/<post_id>/like`    | POST   | 게시물 좋아요 처리    | 예        |
| `/post/<post_id>/save`    | POST   | 게시물 저장 처리      | 예        |

### 알림 관련 API

| 엔드포인트                  | 메소드 | 설명                       | 인증 필요 |
| --------------------------- | ------ | -------------------------- | --------- |
| `/notifications`            | GET    | 알림 목록 페이지           | 예        |
| `/api/unread_notifications` | GET    | 읽지 않은 알림 개수 (JSON) | 예        |

## 사이트맵

```
KWEBLOG
├── 홈페이지 (/)
│   └── 모든 게시물 목록
├── 인증
│   ├── 회원가입 (/register)
│   ├── 로그인 (/login)
│   └── 로그아웃 (/logout)
├── 프로필
│   ├── 프로필 보기 (/profile/<username>)
│   ├── 프로필 수정 (/edit_profile)
│   ├── 서로이웃 신청
│   ├── 서로이웃 수락
│   ├── 서로이웃 거부
│   └── 저장한 게시물 (/saved_posts)
├── 게시물
│   ├── 게시물 작성 (/new_post)
│   └── 게시물 상세 (/post/<post_id>)
│       ├── 댓글 작성
│       ├── 좋아요
│       └── 저장하기
└── 알림
    └── 알림 목록 (/notifications)
```
