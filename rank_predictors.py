import json
from collections import defaultdict

def load_data(predictions_file, results_file):
    """예측 데이터와 경기 결과 데이터를 로드합니다."""
    try:
        with open(predictions_file, 'r', encoding='utf-8') as f:
            predictions = json.load(f)
    except FileNotFoundError:
        print(f"오류: '{predictions_file}' 파일을 찾을 수 없습니다.")
        return None, None
    except json.JSONDecodeError:
        print(f"오류: '{predictions_file}' 파일의 형식이 올바르지 않습니다.")
        return None, None

    match_results = {}
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        if value:  # 결과가 있는 경기만 추가
                            match_results[key] = value
    except FileNotFoundError:
        print(f"오류: '{results_file}' 파일을 찾을 수 없습니다.")
        return None, None

    return predictions, match_results

def calculate_scores(predictions, match_results):
    """참가자별 점수(틀린 개수)를 계산합니다."""
    participant_scores = []
    for participant in predictions:
        nickname = participant['nickname']
        prediction_data = participant['prediction']
        wrong_predictions = 0

        for match_key, actual_winner in match_results.items():
            user_prediction = prediction_data.get(match_key)
            if user_prediction and user_prediction != actual_winner:
                wrong_predictions += 1
        
        participant_scores.append({
            'nickname': nickname,
            'wrong_predictions': wrong_predictions,
            'prediction': prediction_data
        })
    
    # 점수(틀린 개수)가 낮은 순으로, 같으면 닉네임 가나다순으로 정렬
    participant_scores.sort(key=lambda x: (x['wrong_predictions'], x['nickname']))
    
    return participant_scores

def display_top_predictors(ranked_scores):
    """가장 높은 점수를 획득한 참가자 정보를 출력합니다."""
    if not ranked_scores:
        print("분석할 참가자 데이터가 없습니다.")
        return

    top_score = ranked_scores[0]['wrong_predictions']
    top_predictors = [p for p in ranked_scores if p['wrong_predictions'] == top_score]

    print("=" * 50)
    print(f"🏆 현재 1위 (틀린 개수: {top_score}개)")
    print("-" * 50)

    for predictor in top_predictors:
        print(f"닉네임: {predictor['nickname']}")
        print("  [예측 내용]")
        for match, winner in predictor['prediction'].items():
            print(f"    - {match:<15}: {winner}")
        print("-" * 50)

def display_all_ranks(ranked_scores):
    """전체 참가자 순위를 닉네임으로 출력합니다."""
    print("\n" + "=" * 50)
    print("📈 전체 순위 (틀린 개수 순)")
    print("-" * 50)

    # 점수별로 그룹화
    scores_by_rank = defaultdict(list)
    for score_data in ranked_scores:
        scores_by_rank[score_data['wrong_predictions']].append(score_data['nickname'])

    for wrong_count, nicknames in sorted(scores_by_rank.items()):
        print(f"[{wrong_count}개 틀림] ({len(nicknames)}명)")
        print(', '.join(nicknames))
        print()

def main():
    predictions, match_results = load_data('predictions.json', 'match_result.txt')
    if predictions and match_results:
        ranked_scores = calculate_scores(predictions, match_results)
        display_top_predictors(ranked_scores)
        display_all_ranks(ranked_scores)

if __name__ == "__main__":
    main()