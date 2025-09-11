# LCK 플레이오프 2025 승부예측 대시보드

LCK 2025 플레이오프 토너먼트의 승부예측 결과를 실시간으로 추적하는 Streamlit 대시보드입니다.

## 🚀 기능

- **토너먼트 브라켓 시각화**: 현재 토너먼트 진행상황을 실시간으로 확인
- **예측 통계**: 참가자들의 예측 정확도 및 통계 분석
- **참가자 현황**: 생존자/탈락자 현황 및 개별 성과 추적
- **실시간 업데이트**: 경기 결과 업데이트 시 자동 반영

## 📁 파일 구조

```
lck-playoff-analyzer/
├── streamlit_app.py          # 메인 Streamlit 애플리케이션
├── lck_playoff_parser.py     # 댓글 파싱 스크립트
├── lck_playoff_analyzer.py   # 분석 도구
├── predictions.json          # 파싱된 예측 데이터
├── match_result.txt          # 경기 결과 파일
├── comments.txt              # 원본 댓글 데이터
├── requirements.txt          # 필요한 Python 패키지
└── README.md                # 프로젝트 설명
```

## 🛠️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/lck-playoff-analyzer.git
cd lck-playoff-analyzer
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행
```bash
streamlit run streamlit_app.py
```

## 📝 경기 결과 업데이트 방법

`match_result.txt` 파일을 다음 형식으로 업데이트하세요:

```
R1 M1 : T1
R1 M2 : KT
GEN이 고른 팀 : T1
R2 M1 : GEN
R2 M2 : 
R1 LB : 
R2 LB : 
R3 UB : 
R3 LB : 
R4 LF : 
Grand Final : 
```

경기가 완료되면 해당 라인의 결과를 팀명으로 업데이트하고 GitHub에 커밋하세요.

### Git 업데이트 예시
```bash
# 경기 결과 업데이트 후
git add match_result.txt
git commit -m "Update: R1 M1 결과 - T1 승리"
git push origin main
```

## 📊 데이터 구조

### 예측 데이터 형식 (predictions.json)
```json
[
  {
    "nickname": "참가자닉네임",
    "prediction": {
      "R1 M1": "T1",
      "R1 M2": "KT",
      "GEN이 고른 팀": "T1",
      ...
    }
  }
]
```

### 경기 결과 형식 (match_result.txt)
```
매치명 : 승리팀명
```

## 🏆 토너먼트 구조

- **R1 M1**: T1 vs DK
- **R1 M2**: KT vs BFX  
- **GEN이 고른 팀**: GEN의 R2 상대 선택
- **R2 M1**: GEN vs (GEN이 선택한 팀)
- **R2 M2**: HLE vs (R1 M2 승자)
- **패자조**: R1 LB → R2 LB → R3 LB → R4 LF
- **승자조**: R3 UB
- **Grand Final**: 승자조 우승자 vs 패자조 우승자

## 🔧 개발 및 기여

### 새로운 기능 추가 시
1. Fork 후 브랜치 생성
2. 기능 개발 및 테스트
3. Pull Request 제출

### 버그 리포트
Issues 탭에서 버그를 리포트해주세요.

## 📄 라이선스

MIT License

## 👥 참가자 통계

- **총 참가자**: 166명
- **성공적으로 파싱된 예측**: 166개
- **파싱 실패**: 3개

---
**Last Updated**: 2025년 9월 10일