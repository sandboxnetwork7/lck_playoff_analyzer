import json
import plotly.graph_objects as go

class TournamentTracker:
    def __init__(self):
        self.teams = ['T1', 'DK', 'KT', 'BFX', 'GEN', 'HLE']
        self.predictions = []
        self.match_results = {}
        self.load_data()
        
    def load_data(self):
        """데이터 로드"""
        try:
            # 예측 데이터 로드
            with open('predictions.json', 'r', encoding='utf-8') as f:
                self.predictions = json.load(f)
            print(f"예측 데이터 로드 완료: {len(self.predictions)}개")
        except FileNotFoundError:
            print("predictions.json 파일을 찾을 수 없습니다.")
            self.predictions = []
        
        # 경기 결과 로드
        self.match_results = self.load_match_results()
        
    def load_match_results(self):
        """경기 결과 파일 로드"""
        results = {}
        default_matches = ['R1 M1', 'R1 M2', 'GEN이 고른 팀', 'R2 M1', 'R2 M2', 
                          'R1 LB', 'R2 LB', 'R3 UB', 'R3 LB', 'R4 LF', 'Grand Final']
        
        try:
            with open('match_result.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line and line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            results[key] = value if value else None
        except FileNotFoundError:
            print("match_result.txt 파일을 찾을 수 없습니다.")
        
        # 기본 매치들이 없으면 추가
        for match in default_matches:
            if match not in results:
                results[match] = None
                
        return results
    
    def get_match_info(self, match_key):
        """개별 매치 정보 생성"""
        winner = self.match_results.get(match_key)
        
        if match_key == 'R1 M1':
            return {
                'match_id': 'R1 M1',
                'title': 'R1 M1',
                'team1': 'T1',
                'team2': 'DK',
                'winner': winner,
                'status': '완료' if winner else '예정'
            }
            
        elif match_key == 'R1 M2':
            return {
                'match_id': 'R1 M2', 
                'title': 'R1 M2',
                'team1': 'KT',
                'team2': 'BFX',
                'winner': winner,
                'status': '완료' if winner else '예정'
            }
            
        elif match_key == 'R2 M1':
            gen_choice = self.match_results.get('GEN이 고른 팀')
            if gen_choice:
                return {
                    'match_id': 'R2 M1',
                    'title': 'R2 M1 (승자조)',
                    'team1': 'GEN',
                    'team2': gen_choice,
                    'winner': winner,
                    'status': '완료' if winner else '예정'
                }
            else:
                return {
                    'match_id': 'R2 M1',
                    'title': 'R2 M1 (승자조)',
                    'team1': 'GEN',
                    'team2': '미정',
                    'winner': None,
                    'status': 'GEN 선택 대기'
                }
                
        elif match_key == 'R2 M2':
            gen_choice = self.match_results.get('GEN이 고른 팀')
            r1_m1_winner = self.match_results.get('R1 M1')
            r1_m2_winner = self.match_results.get('R1 M2')
            
            if gen_choice and r1_m1_winner and r1_m2_winner:
                # GEN이 선택하지 않은 팀
                other_team = r1_m2_winner if gen_choice == r1_m1_winner else r1_m1_winner
                return {
                    'match_id': 'R2 M2',
                    'title': 'R2 M2 (승자조)',
                    'team1': 'HLE',
                    'team2': other_team,
                    'winner': winner,
                    'status': '완료' if winner else '예정'
                }
            else:
                return {
                    'match_id': 'R2 M2',
                    'title': 'R2 M2 (승자조)',
                    'team1': 'HLE',
                    'team2': '미정',
                    'winner': None,
                    'status': 'R1 완료/GEN 선택 대기'
                }
                
        elif match_key == 'R1 LB':
            r1_m1_winner = self.match_results.get('R1 M1')
            r1_m2_winner = self.match_results.get('R1 M2')
            
            if r1_m1_winner and r1_m2_winner:
                loser1 = 'DK' if r1_m1_winner == 'T1' else 'T1'
                loser2 = 'BFX' if r1_m2_winner == 'KT' else 'KT'
                return {
                    'match_id': 'R1 LB',
                    'title': 'R1 LB (패자조)',
                    'team1': loser1,
                    'team2': loser2,
                    'winner': winner,
                    'status': '완료' if winner else '예정'
                }
            else:
                return {
                    'match_id': 'R1 LB',
                    'title': 'R1 LB (패자조)',
                    'team1': '미정',
                    'team2': '미정',
                    'winner': None,
                    'status': 'R1 완료 대기'
                }
                
        elif match_key == 'R3 UB':
            r2_m1_winner = self.match_results.get('R2 M1')
            r2_m2_winner = self.match_results.get('R2 M2')
            
            if r2_m1_winner and r2_m2_winner:
                return {
                    'match_id': 'R3 UB',
                    'title': 'R3 UB (승자조 결승)',
                    'team1': r2_m1_winner,
                    'team2': r2_m2_winner,
                    'winner': winner,
                    'status': '완료' if winner else '예정'
                }
            else:
                return {
                    'match_id': 'R3 UB',
                    'title': 'R3 UB (승자조 결승)',
                    'team1': '미정',
                    'team2': '미정',
                    'winner': None,
                    'status': 'R2 완료 대기'
                }
                
        # 다른 매치들도 비슷한 방식으로 처리
        else:
            return {
                'match_id': match_key,
                'title': match_key,
                'team1': '미정',
                'team2': '미정', 
                'winner': winner,
                'status': '대기' if not winner else '완료'
            }
    
    def get_all_matches(self):
        """모든 매치 정보 반환"""
        match_order = ['R1 M1', 'R1 M2', 'R2 M1', 'R2 M2', 'R1 LB', 'R2 LB', 'R3 UB', 'R3 LB', 'R4 LF', 'Grand Final']
        matches = []
        
        for match_key in match_order:
            match_info = self.get_match_info(match_key)
            matches.append(match_info)
            
        return matches
    
    def get_gen_choice_status(self):
        """GEN 선택 상태 반환"""
        r1_m1_winner = self.match_results.get('R1 M1')
        r1_m2_winner = self.match_results.get('R1 M2')
        gen_choice = self.match_results.get('GEN이 고른 팀')
        
        if gen_choice:
            return f"GEN이 선택한 팀: {gen_choice}"
        elif r1_m1_winner and r1_m2_winner:
            return f"GEN이 선택 가능한 팀: {r1_m1_winner}, {r1_m2_winner}"
        elif r1_m1_winner or r1_m2_winner:
            completed = r1_m1_winner or r1_m2_winner
            return f"R1 진행 중 (완료: {completed})"
        else:
            return "R1 경기 시작 대기"
    
    def calculate_prediction_stats(self):
        """예측 통계 계산"""
        if not self.predictions:
            return [], 0
            
        actual_matches = ['R1 M1', 'R1 M2', 'R2 M1', 'R2 M2', 'R1 LB', 'R2 LB', 'R3 UB', 'R3 LB', 'R4 LF', 'Grand Final']
        participant_stats = []
        
        for participant in self.predictions:
            nickname = participant['nickname']
            prediction = participant['prediction']
            wrong_count = 0
            total_matches = 0
            
            for match_key in actual_matches:
                actual_result = self.match_results.get(match_key)
                if actual_result:
                    total_matches += 1
                    predicted = prediction.get(match_key)
                    
                    if predicted and predicted != actual_result:
                        wrong_count += 1
            
            participant_stats.append({
                'nickname': nickname,
                'wrong_count': wrong_count,
                'total_matches': total_matches,
                'is_eliminated': wrong_count > 0,
                'accuracy': (total_matches - wrong_count) / total_matches if total_matches > 0 else 1.0
            })
        
        return participant_stats, len(self.predictions)
    
    def create_survivor_display(self, participant_stats, total_participants):
        """생존자 표시 정보 생성"""
        eliminated = sum(1 for p in participant_stats if p['is_eliminated'])
        surviving = total_participants - eliminated
        survival_rate = (surviving / total_participants) * 100 if total_participants > 0 else 0
        
        if survival_rate > 70:
            color = "#10B981"
            status_emoji = "🟢"
            status_text = "안전"
        elif survival_rate > 40:
            color = "#F59E0B"
            status_emoji = "🟡"
            status_text = "주의"
        elif survival_rate > 20:
            color = "#EF4444"
            status_emoji = "🟠"
            status_text = "위험"
        else:
            color = "#DC2626"
            status_emoji = "🔴"
            status_text = "극한"
            
        return surviving, eliminated, survival_rate, color, status_emoji, status_text
    
    def create_stats_charts(self, participant_stats, total_participants):
        """통계 차트 생성"""
        eliminated = sum(1 for p in participant_stats if p['is_eliminated'])
        surviving = total_participants - eliminated
        
        # 파이 차트
        pie_fig = go.Figure(data=[go.Pie(
            labels=['생존자', '탈락자'],
            values=[surviving, eliminated],
            hole=0.4,
            marker_colors=['#10B981', '#EF4444']
        )])
        
        pie_fig.update_layout(
            title=f"참가자 현황 (총 {total_participants}명)",
            height=400
        )
        
        # 히스토그램
        if participant_stats:
            wrong_counts = [p['wrong_count'] for p in participant_stats]
            max_wrong = max(wrong_counts) if wrong_counts else 0
            
            hist_data = {}
            for count in wrong_counts:
                hist_data[count] = hist_data.get(count, 0) + 1
            
            x_vals = list(range(max_wrong + 1))
            y_vals = [hist_data.get(i, 0) for i in x_vals]
            
            hist_fig = go.Figure(data=[go.Bar(
                x=x_vals,
                y=y_vals,
                marker_color='#3B82F6'
            )])
            
            hist_fig.update_layout(
                title="틀린 예측 수별 참가자 분포",
                xaxis_title="틀린 예측 수",
                yaxis_title="참가자 수",
                height=400
            )
        else:
            hist_fig = go.Figure()
            hist_fig.update_layout(title="데이터 없음", height=400)
        
        return pie_fig, hist_fig