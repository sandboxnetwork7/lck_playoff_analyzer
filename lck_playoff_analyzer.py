import json
import sys
from collections import Counter

class TournamentAnalyzer:
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # 인코딩 문제 수정을 위한 키 매핑
        self.key_mapping = {
            'GENì´ ê³ ë¥¸ íŒ€': 'GEN이 고른 팀'
        }
        
        self.total_predictions = len(self.data)
        print(f"총 {self.total_predictions}개의 예측 데이터 로드됨")
    
    def get_prediction_value(self, prediction, key):
        """인코딩 문제를 고려하여 예측 값을 가져옴"""
        if key in prediction:
            return prediction[key]
        
        # 인코딩된 키로 시도
        for encoded_key, correct_key in self.key_mapping.items():
            if correct_key == key and encoded_key in prediction:
                return prediction[encoded_key]
        
        return None
    
    def list_nicknames(self):
        """닉네임만 콤마 구분으로 출력"""
        nicknames = [entry['nickname'] for entry in self.data]
        result = ', '.join(nicknames)
        print(f"\n전체 닉네임 ({len(nicknames)}명):")
        print(result)
        return result
    
    def championship_predictions(self):
        """우승자 예측 확률"""
        grand_finals = []
        for entry in self.data:
            winner = entry['prediction'].get('Grand Final')
            if winner:
                grand_finals.append(winner)
        
        counter = Counter(grand_finals)
        total = len(grand_finals)
        
        print(f"\n우승자 예측 ({total}명 응답):")
        for team, count in counter.most_common():
            percentage = (count / total) * 100
            print(f"{team}: {count}명 ({percentage:.1f}%)")
    
    def match_predictions(self, match_key, match_name):
        """특정 매치의 팀별 승리 예측 비율"""
        teams = []
        for entry in self.data:
            team = entry['prediction'].get(match_key)
            if team:
                teams.append(team)
        
        counter = Counter(teams)
        total = len(teams)
        
        print(f"\n{match_name} 승리 예측 ({total}명 응답):")
        for team, count in counter.most_common():
            percentage = (count / total) * 100
            print(f"{team}: {count}명 ({percentage:.1f}%)")
    
    def gen_choice_analysis(self):
        """R1 결과에 따른 GEN 선택 예측 분석"""
        scenarios = {}
        
        for entry in self.data:
            pred = entry['prediction']
            r1m1_winner = pred.get('R1 M1')
            r1m2_winner = pred.get('R1 M2')
            gen_choice = self.get_prediction_value(pred, 'GEN이 고른 팀')
            
            if r1m1_winner and r1m2_winner and gen_choice:
                scenario = f"{r1m1_winner} vs {r1m2_winner}"
                if scenario not in scenarios:
                    scenarios[scenario] = []
                scenarios[scenario].append(gen_choice)
        
        print(f"\nR1 결과별 GEN 선택 예측:")
        for scenario, choices in scenarios.items():
            counter = Counter(choices)
            total = len(choices)
            print(f"\n{scenario} 상황 ({total}명 예측):")
            for team, count in counter.most_common():
                percentage = (count / total) * 100
                print(f"  GEN이 {team} 선택: {count}명 ({percentage:.1f}%)")
    
    def team_statistics(self):
        """팀별 전체 통계"""
        all_picks = []
        
        for entry in self.data:
            pred = entry['prediction']
            for key, value in pred.items():
                if value and key != 'GEN이 고른 팀':
                    # 인코딩된 키 제외
                    if key not in self.key_mapping:
                        all_picks.append(value)
        
        counter = Counter(all_picks)
        total = len(all_picks)
        
        print(f"\n전체 팀별 선택 횟수:")
        for team, count in counter.most_common():
            percentage = (count / total) * 100
            print(f"{team}: {count}회 선택 ({percentage:.1f}%)")
    
    def round_analysis(self, round_name):
        """라운드별 상세 분석"""
        round_keys = {
            'R1': ['R1 M1', 'R1 M2'],
            'R2': ['R2 M1', 'R2 M2'],
            'R3': ['R3 UB', 'R3 LB'],
            'LB': ['R1 LB', 'R2 LB'],
            'FINAL': ['R4 LF', 'Grand Final']
        }
        
        if round_name.upper() not in round_keys:
            print("유효한 라운드: R1, R2, R3, LB, FINAL")
            return
        
        keys = round_keys[round_name.upper()]
        print(f"\n{round_name.upper()} 라운드 분석:")
        
        for key in keys:
            teams = []
            for entry in self.data:
                team = entry['prediction'].get(key)
                if team:
                    teams.append(team)
            
            counter = Counter(teams)
            total = len(teams)
            
            print(f"\n{key} ({total}명 응답):")
            for team, count in counter.most_common():
                percentage = (count / total) * 100
                print(f"  {team}: {count}명 ({percentage:.1f}%)")

def show_menu():
    print("\n" + "="*50)
    print("토너먼트 예측 분석기")
    print("="*50)
    print("1. 전체 닉네임 출력")
    print("2. 우승자 예측 확률")
    print("3. R1 M1 승리 예측")
    print("4. R1 M2 승리 예측")
    print("5. R2 M1 승리 예측")
    print("6. R2 M2 승리 예측")
    print("7. GEN 선택 예측 분석")
    print("8. 팀별 전체 통계")
    print("9. 라운드별 분석")
    print("0. 종료")
    print("-"*50)

def main():
    if len(sys.argv) != 2:
        print("사용법: python tournament_analyzer.py predictions.json")
        return
    
    try:
        analyzer = TournamentAnalyzer(sys.argv[1])
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {sys.argv[1]}")
        return
    except json.JSONDecodeError:
        print("JSON 파일 형식이 올바르지 않습니다.")
        return
    
    while True:
        show_menu()
        choice = input("선택하세요 (0-9): ").strip()
        
        if choice == '0':
            print("분석기를 종료합니다.")
            break
        elif choice == '1':
            analyzer.list_nicknames()
        elif choice == '2':
            analyzer.championship_predictions()
        elif choice == '3':
            analyzer.match_predictions('R1 M1', 'R1 M1')
        elif choice == '4':
            analyzer.match_predictions('R1 M2', 'R1 M2')
        elif choice == '5':
            analyzer.match_predictions('R2 M1', 'R2 M1')
        elif choice == '6':
            analyzer.match_predictions('R2 M2', 'R2 M2')
        elif choice == '7':
            analyzer.gen_choice_analysis()
        elif choice == '8':
            analyzer.team_statistics()
        elif choice == '9':
            round_name = input("라운드를 입력하세요 (R1/R2/R3/LB/FINAL): ").strip()
            analyzer.round_analysis(round_name)
        else:
            print("올바른 번호를 입력하세요.")
        
        input("\n계속하려면 Enter를 누르세요...")

if __name__ == "__main__":
    main()