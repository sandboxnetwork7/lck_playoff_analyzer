import json
import re

def parse_pgr21_comments(text):
    lines = text.strip().split('\n')
    results = []
    failed_users = []
    debug_info = []
    
    i = 0
    user_count = 0
    
    while i < len(lines):
        # "추천" 으로 시작하는 라인 찾기 (추천 0, 추천 1 등 모두 포함)
        if lines[i].strip().startswith("추천"):
            user_count += 1
            
            # 바로 윗줄이 닉네임
            if i > 0:
                nickname = lines[i-1].strip()
                
                # 디버그 정보 저장
                debug_entry = {
                    "user_number": user_count,
                    "nickname": nickname,
                    "line_number": i,
                    "status": "processing"
                }
                
                # "수정 아이콘" 찾기
                j = i + 1
                found_edit_icon = False
                while j < len(lines) and j < i + 10:  # 최대 10줄까지만 찾기
                    if "수정 아이콘" in lines[j]:
                        found_edit_icon = True
                        break
                    j += 1
                
                if found_edit_icon:
                    j += 1  # "수정 아이콘" 다음줄부터 댓글 내용
                    
                    # 댓글 내용 수집 (다음 "추천"으로 시작하는 줄까지)
                    comment_content = []
                    while j < len(lines):
                        if lines[j].strip().startswith("추천"):
                            break
                        comment_content.append(lines[j].strip())
                        j += 1
                    
                    # 승부예측 패턴 찾기
                    comment_text = '\n'.join(comment_content)
                    prediction, failure_reason = extract_prediction_with_reason(comment_text)
                    
                    if prediction:
                        results.append({
                            "nickname": nickname,
                            "prediction": prediction
                        })
                        debug_entry["status"] = "success"
                    else:
                        failed_users.append({
                            "nickname": nickname,
                            "reason": failure_reason,
                            "comment": comment_text[:100] + "..." if len(comment_text) > 100 else comment_text
                        })
                        debug_entry["status"] = "failed - " + failure_reason
                else:
                    debug_entry["status"] = "failed - 수정 아이콘 없음"
                
                debug_info.append(debug_entry)
                i = j  # 다음 "추천"부터 계속
            else:
                i += 1
        else:
            i += 1
    
    return results, failed_users, debug_info, user_count

def extract_prediction_with_reason(text):
    prediction_pattern = {
        "R1 M1": None,
        "R1 M2": None,
        "GEN이 고른 팀": None,
        "R2 M1": None,
        "R2 M2": None,
        "R1 LB": None,
        "R2 LB": None,
        "R3 UB": None,
        "R3 LB": None,
        "R4 LF": None,
        "Grand Final": None
    }
    
    found_fields = []
    missing_fields = []
    
    # 각 패턴 찾기
    for key in prediction_pattern.keys():
        pattern = rf"{re.escape(key)}\s*:\s*(\w+)"
        match = re.search(pattern, text)
        if match:
            prediction_pattern[key] = match.group(1)
            found_fields.append(key)
        else:
            missing_fields.append(key)
    
    # 모든 필드가 채워졌는지 확인
    if all(value is not None for value in prediction_pattern.values()):
        return prediction_pattern, None
    
    # 실패 이유 생성
    if not found_fields:
        reason = "승부예측 패턴이 전혀 없음"
    else:
        reason = f"일부 필드만 발견됨 - 발견: {len(found_fields)}/11개"
    
    return None, reason

def main():
    # 파일 읽기
    with open('comments.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 파싱
    results, failed_users, debug_info, total_users = parse_pgr21_comments(text)
    
    # JSON 저장
    with open('predictions.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 실패 정보 저장
    if failed_users:
        with open('failed_predictions.json', 'w', encoding='utf-8') as f:
            json.dump(failed_users, f, ensure_ascii=False, indent=2)
    
    # 디버그 정보 저장
    with open('debug_info.json', 'w', encoding='utf-8') as f:
        json.dump(debug_info, f, ensure_ascii=False, indent=2)
    
    # 결과 출력
    print(f"총 발견된 유저: {total_users}명")
    print(f"파싱 성공: {len(results)}개")
    print(f"파싱 실패: {len(failed_users)}개")
    print(f"처리된 총합: {len(results) + len(failed_users)}개")
    
    if total_users != len(results) + len(failed_users):
        print(f"\n⚠️ 누락된 유저: {total_users - len(results) - len(failed_users)}명")
        print("debug_info.json 파일을 확인해보세요.")
    
    if failed_users:
        print(f"\n파싱 실패 사유:")
        for user in failed_users[:5]:  # 처음 5명만 출력
            print(f"- {user['nickname']}: {user['reason']}")
        if len(failed_users) > 5:
            print(f"... 외 {len(failed_users)-5}명 더")

if __name__ == "__main__":
    main()