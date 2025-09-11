import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="LCK 플레이오프 2025 - 승부예측 대시보드",
    page_icon="🏆",
    layout="wide"
)

def load_all_data():
    """모든 데이터 로드"""
    # 예측 데이터 로드
    predictions = []
    try:
        with open('predictions.json', 'r', encoding='utf-8') as f:
            predictions = json.load(f)
    except FileNotFoundError:
        st.warning("predictions.json 파일을 찾을 수 없습니다.")
    
    # 경기 결과 로드
    match_results = {}
    try:
        with open('match_result.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        match_results[key] = value if value else None
    except FileNotFoundError:
        st.warning("match_result.txt 파일을 찾을 수 없습니다.")
    
    return predictions, match_results

def get_schedule():
    """경기 일정"""
    return {
        'R1 M1': '9월 10일 수요일 오후 5시',
        'R1 M2': '9월 11일 목요일 오후 5시', 
        'R2 M1': '9월 13일 토요일 오후 3시',
        'R2 M2': '9월 14일 일요일 오후 3시',
        'R1 LB': '9월 17일 수요일 오후 5시',
        'R2 LB': '9월 18일 목요일 오후 5시',
        'R3 UB': '9월 20일 토요일 오후 3시',
        'R3 LB': '9월 21일 일요일 오후 3시',
        'R4 LF': '9월 27일 토요일 오후 2시',
        'Grand Final': '9월 28일 일요일 오후 2시'
    }

def show_match(match_id, team1, team2, winner, schedule_time):
    """개별 매치 표시"""
    # 상태 결정
    if winner:
        status_color = "#10B981"
        status_emoji = "✅"
        result_text = f"승자: {winner}"
    elif team1 == "미정" or team2 == "미정":
        status_color = "#6B7280"
        status_emoji = "⏸️"
        result_text = "대기 중"
    else:
        status_color = "#F59E0B"
        status_emoji = "⏳"
        result_text = "경기 예정"
    
    st.markdown(f"""
    <div style='
        border: 2px solid {status_color}; 
        border-radius: 10px; 
        padding: 12px; 
        margin: 8px 0; 
        background: white;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    '>
        <div style='font-weight: bold; color: {status_color}; font-size: 1.1em;'>
            {status_emoji} {match_id}
        </div>
        <div style='font-size: 1.2em; margin: 8px 0; font-weight: bold;'>
            {team1} vs {team2}
        </div>
        <div style='color: #666; font-size: 0.9em; margin: 5px 0;'>
            {result_text}
        </div>
        <div style='color: #888; font-size: 0.8em; font-style: italic;'>
            {schedule_time}
        </div>
    </div>
    """, unsafe_allow_html=True)

def calculate_survivor_stats(predictions, match_results):
    """생존자 통계 계산"""
    if not predictions:
        return 0, 0, 0, "#6B7280", "⏸️", "데이터 없음"
    
    actual_matches = ['R1 M1', 'R1 M2', 'R2 M1', 'R2 M2', 'R1 LB', 'R2 LB', 'R3 UB', 'R3 LB', 'R4 LF', 'Grand Final']
    total_participants = len(predictions)
    eliminated = 0
    
    for participant in predictions:
        prediction = participant['prediction']
        is_eliminated = False
        
        for match_key in actual_matches:
            actual_result = match_results.get(match_key)
            if actual_result:
                predicted = prediction.get(match_key)
                if predicted and predicted != actual_result:
                    is_eliminated = True
                    break
        
        if is_eliminated:
            eliminated += 1
    
    surviving = total_participants - eliminated
    survival_rate = (surviving / total_participants) * 100 if total_participants > 0 else 0
    
    # 생존율에 따른 색상과 상태
    if survival_rate > 70:
        color = "#10B981"
        emoji = "🟢"
        status = "안전"
    elif survival_rate > 40:
        color = "#F59E0B"
        emoji = "🟡"
        status = "주의"
    elif survival_rate > 20:
        color = "#EF4444"
        emoji = "🟠"
        status = "위험"
    else:
        color = "#DC2626"
        emoji = "🔴"
        status = "극한"
    
    return surviving, eliminated, survival_rate, color, emoji, status

def main():
    st.title("🏆 LCK 플레이오프 2025 - 승부예측 대시보드")
    
    # 데이터 로드
    predictions, match_results = load_all_data()
    schedule = get_schedule()
    
    # 사이드바
    st.sidebar.header("📊 현재 상황")
    
    # 완료된 경기 수 계산
    actual_matches = ['R1 M1', 'R1 M2', 'R2 M1', 'R2 M2', 'R1 LB', 'R2 LB', 'R3 UB', 'R3 LB', 'R4 LF', 'Grand Final']
    completed = sum(1 for match in actual_matches if match_results.get(match))
    st.sidebar.metric("완료된 경기", f"{completed}/10")
    
    # 다음 경기
    next_match = None
    for match in actual_matches:
        if not match_results.get(match):
            next_match = match
            break
    
    if next_match:
        st.sidebar.info(f"다음 경기: {next_match}")
        st.sidebar.info(f"일정: {schedule.get(next_match, '')}")
    else:
        st.sidebar.success("모든 경기 완료!")
    
    # 탭 생성
    tab1, tab2 = st.tabs(["🏟️ 토너먼트 브라켓", "📈 예측 통계"])
    
    with tab1:
        st.header("토너먼트 브라켓")
        
        # 경기 결과로부터 팀 결정
        r1_m1_winner = match_results.get('R1 M1')
        r1_m2_winner = match_results.get('R1 M2')
        gen_choice = match_results.get('GEN이 고른 팀')
        r2_m1_winner = match_results.get('R2 M1')
        r2_m2_winner = match_results.get('R2 M2')
        
        # GEN 선택 정보
        if gen_choice:
            st.info(f"🎯 GEN이 선택한 팀: {gen_choice}")
        elif r1_m1_winner and r1_m2_winner:
            st.info(f"🎯 GEN이 선택 가능한 팀: {r1_m1_winner}, {r1_m2_winner}")
        else:
            st.info("🎯 R1 경기 완료 후 GEN이 상대를 선택합니다")
        
        # 승자조 브라켓
        st.subheader("🏆 승자조 대진표")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**1라운드**")
            show_match("R1 M1", "T1", "DK", r1_m1_winner, schedule['R1 M1'])
            st.markdown("")
            show_match("R1 M2", "KT", "BFX", r1_m2_winner, schedule['R1 M2'])
        
        with col2:
            st.markdown("**2라운드**")
            # R2 M1
            if gen_choice:
                show_match("R2 M1", "GEN", gen_choice, r2_m1_winner, schedule['R2 M1'])
            else:
                show_match("R2 M1", "GEN", "미정", None, schedule['R2 M1'])
            
            st.markdown("")
            
            # R2 M2
            if gen_choice and r1_m1_winner and r1_m2_winner:
                other_team = r1_m2_winner if gen_choice == r1_m1_winner else r1_m1_winner
                show_match("R2 M2", "HLE", other_team, match_results.get('R2 M2'), schedule['R2 M2'])
            else:
                show_match("R2 M2", "HLE", "미정", None, schedule['R2 M2'])
        
        with col3:
            st.markdown("**승자조 결승**")
            if r2_m1_winner and r2_m2_winner:
                show_match("R3 UB", r2_m1_winner, r2_m2_winner, match_results.get('R3 UB'), schedule['R3 UB'])
            else:
                show_match("R3 UB", "미정", "미정", None, schedule['R3 UB'])
        
        st.markdown("---")
        
        # 패자조 브라켓
        st.subheader("⚔️ 패자조 대진표")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**패자조 1R**")
            if r1_m1_winner and r1_m2_winner:
                loser1 = "DK" if r1_m1_winner == "T1" else "T1"
                loser2 = "BFX" if r1_m2_winner == "KT" else "KT"
                show_match("R1 LB", loser1, loser2, match_results.get('R1 LB'), schedule['R1 LB'])
            else:
                show_match("R1 LB", "미정", "미정", None, schedule['R1 LB'])
        
        with col2:
            st.markdown("**패자조 2R**")
            show_match("R2 LB", "미정", "미정", match_results.get('R2 LB'), schedule['R2 LB'])
        
        with col3:
            st.markdown("**패자조 3R**")
            show_match("R3 LB", "미정", "미정", match_results.get('R3 LB'), schedule['R3 LB'])
        
        with col4:
            st.markdown("**패자조 결승**")
            show_match("R4 LF", "미정", "미정", match_results.get('R4 LF'), schedule['R4 LF'])
        
        st.markdown("---")
        
        # 그랜드 파이널
        st.subheader("🏆 GRAND FINAL")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            r3_ub_winner = match_results.get('R3 UB')
            r4_lf_winner = match_results.get('R4 LF')
            
            if r3_ub_winner and r4_lf_winner:
                show_match("Grand Final", r3_ub_winner, r4_lf_winner, match_results.get('Grand Final'), schedule['Grand Final'])
            else:
                show_match("Grand Final", "미정", "미정", None, schedule['Grand Final'])
    
    with tab2:
        st.header("예측 통계")
        
        if completed > 0:
            # 생존자 통계
            surviving, eliminated, survival_rate, color, emoji, status = calculate_survivor_stats(predictions, match_results)
            
            if predictions:
                # 대형 생존자 표시
                st.markdown(f"""
                <div style='
                    text-align: center; 
                    padding: 30px; 
                    background: linear-gradient(135deg, {color}22, {color}11); 
                    border-radius: 20px; 
                    margin: 20px 0;
                    border: 3px solid {color};
                '>
                    <h1 style='color: {color}; margin: 0; font-size: 4em;'>{emoji} {surviving}</h1>
                    <h2 style='color: {color}; margin: 10px 0; font-size: 2em;'>SURVIVORS REMAINING</h2>
                    <p style='color: #666; margin: 0; font-size: 1.4em;'>
                        생존율 {survival_rate:.1f}% - 상태: {status}
                    </p>
                    <p style='color: #888; margin: 10px 0; font-size: 1.1em;'>
                        총 {len(predictions)}명 중 {eliminated}명 탈락
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # 메트릭
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("총 참가자", len(predictions))
                
                with col2:
                    st.metric("생존자", surviving, delta=f"-{eliminated}")
                
                with col3:
                    # 평균 정확도 계산
                    participant_stats = []
                    for participant in predictions:
                        prediction = participant['prediction']
                        wrong = 0
                        total = 0
                        for match in actual_matches:
                            actual = match_results.get(match)
                            if actual:
                                total += 1
                                predicted = prediction.get(match)
                                if predicted and predicted != actual:
                                    wrong += 1
                        accuracy = (total - wrong) / total if total > 0 else 1.0
                        participant_stats.append(accuracy)
                    
                    avg_accuracy = sum(participant_stats) / len(participant_stats) if participant_stats else 0
                    st.metric("평균 정확도", f"{avg_accuracy:.1%}")
                
                with col4:
                    perfect = surviving if completed > 0 else len(predictions)
                    st.metric("완벽한 예측", perfect)
                
                # 차트
                col1, col2 = st.columns(2)
                
                with col1:
                    # 파이 차트
                    pie_fig = go.Figure(data=[go.Pie(
                        labels=['생존자', '탈락자'],
                        values=[surviving, eliminated],
                        hole=0.4,
                        marker_colors=['#10B981', '#EF4444']
                    )])
                    pie_fig.update_layout(
                        title=f"참가자 현황 (총 {len(predictions)}명)",
                        height=400
                    )
                    st.plotly_chart(pie_fig, use_container_width=True)
                
                with col2:
                    # 히스토그램 - 틀린 예측 수별 분포
                    wrong_counts = []
                    for participant in predictions:
                        prediction = participant['prediction']
                        wrong = 0
                        for match in actual_matches:
                            actual = match_results.get(match)
                            if actual:
                                predicted = prediction.get(match)
                                if predicted and predicted != actual:
                                    wrong += 1
                        wrong_counts.append(wrong)
                    
                    if wrong_counts:
                        max_wrong = max(wrong_counts)
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
                        st.plotly_chart(hist_fig, use_container_width=True)
                
                # 경고 메시지
                if survival_rate < 30:
                    st.error(f"🚨 위기 상황! 참가자의 {100-survival_rate:.1f}%가 탈락했습니다!")
                elif survival_rate < 50:
                    st.warning("⚠️ 경기가 치열해지고 있습니다. 절반 이상이 탈락 위기입니다.")
            else:
                st.warning("예측 데이터를 불러올 수 없습니다.")
        else:
            st.info("아직 완료된 경기가 없어 통계를 표시할 수 없습니다.")
    
    # 푸터
    st.markdown("---")
    st.markdown(f"📅 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()