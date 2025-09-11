# LCK 플레이오프 프로젝트 설정 가이드

## 📁 1. 프로젝트 폴더 구성

다음과 같이 폴더를 구성하세요:

```
lck-playoff-analyzer/
├── streamlit_app.py
├── lck_playoff_parser.py
├── lck_playoff_analyzer.py
├── update_match.py
├── predictions.json
├── match_result.txt
├── comments.txt
├── debug_info.json
├── failed_predictions.json
├── requirements.txt
├── README.md
├── .gitignore
└── setup_guide.md
```

## 🐙 2. GitHub 저장소 생성 및 업로드

### 2.1 GitHub에서 새 저장소 생성
1. GitHub.com에 로그인
2. "New repository" 클릭
3. 저장소 이름: `lck-playoff-analyzer`
4. Public으로 설정 (Streamlit Cloud 무료 배포를 위해)
5. "Create repository" 클릭

### 2.2 로컬에서 Git 초기화 및 업로드
```bash
# 프로젝트 폴더에서 실행
cd lck-playoff-analyzer

# Git 초기화
git init

# 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: LCK playoff prediction tracker"

# GitHub 저장소 연결
git remote add origin https://github.com/YOUR_USERNAME/lck-playoff-analyzer.git

# 업로드
git branch -M main
git push -u origin main
```

## 🚀 3. Streamlit Cloud 배포

### 3.1 Streamlit Cloud 계정 설정
1. [share.streamlit.io](https://share.streamlit.io) 방문
2. GitHub 계정으로 로그인
3. "New app" 클릭

### 3.2 앱 배포 설정
- **Repository**: `YOUR_USERNAME/lck-playoff-analyzer`
- **Branch**: `main`
- **Main file path**: `streamlit_app.py`
- **App URL**: 원하는 URL 설정

### 3.3 배포 완료
- "Deploy!" 클릭
- 몇 분 후 앱이 온라인으로 공개됩니다

## ⚙️ 4. 경기 결과 업데이트 워크플로우

### 4.1 대화형 업데이트 (추천)
```bash
python update_match.py
```

### 4.2 직접 업데이트
```bash
python update_match.py "R1 M1" "T1"
```

### 4.3 수동 업데이트
1. `match_result.txt` 파일을 직접 편집
2. Git 커밋 및 푸시:
```bash
git add match_result.txt
git commit -m "Update: R1 M1 결과 - T1 승리"
git push
```

## 📱 5. 자동 업데이트 설정 (선택사항)

### 5.1 GitHub Actions 워크플로우
`.github/workflows/update.yml` 파일 생성:

```yaml
name: Update Match Results
on:
  workflow_dispatch:
    inputs:
      match:
        description: 'Match name (e.g., R1 M1)'
        required: true
      winner:
        description: 'Winner team'
        required: true

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Update match result
      run: |
        python update_match.py "${{ github.event.inputs.match }}" "${{ github.event.inputs.winner }}"
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add match_result.txt
        git commit -m "Update: ${{ github.event.inputs.match }} - ${{ github.event.inputs.winner }} 승리"
        git push
```

## 🔧 6. 로컬 개발 환경 설정

### 6.1 가상환경 생성 (권장)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 6.2 패키지 설치
```bash
pip install -r requirements.txt
```

### 6.3 로컬에서 앱 실행
```bash
streamlit run streamlit_app.py
```

## 📊 7. 데이터 백업 권장사항

### 7.1 정기 백업
- `predictions.json`: 예측 데이터 (중요!)
- `match_result.txt`: 경기 결과
- `comments.txt`: 원본 댓글 데이터

### 7.2 백업 스크립트 예시
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p backups
cp predictions.json backups/predictions_$DATE.json
cp match_result.txt backups/match_result_$DATE.txt
echo "Backup completed: $DATE"
```

## 🆘 8. 문제 해결

### 8.1 Streamlit 앱이 안 뜰 때
1. `requirements.txt` 확인
2. GitHub 저장소의 파일 경로 확인
3. Streamlit Cloud 로그 확인

### 8.2 한글 인코딩 문제
- 모든 파일이 UTF-8로 저장되었는지 확인
- `encoding='utf-8'` 파라미터 확인

### 8.3 Git 푸시 실패
```bash
git pull origin main  # 충돌 해결 후
git push origin main
```

## 🎯 9. 운영 팁

### 9.1 경기 일정 관리
- 경기 시작 전에 미리 업데이트 스크립트 준비
- 경기 종료 즉시 결과 업데이트로 실시간성 확보

### 9.2 사용자 참여 유도
- SNS에 대시보드 링크 공유
- 실시간 업데이트 알림

### 9.3 데이터 분석 확장
- 추가 통계 지표 구현
- 예측 패턴 분석 기능 추가

---
🎮 **LCK 플레이오프 화이팅!** 🏆