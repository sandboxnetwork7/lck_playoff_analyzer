#!/usr/bin/env python3
"""
LCK 플레이오프 경기 결과 업데이트 스크립트
"""

import os
import subprocess
import sys
from datetime import datetime

class MatchUpdater:
    def __init__(self):
        self.match_file = 'match_result.txt'
        self.teams = ['T1', 'DK', 'KT', 'BFX', 'GEN', 'HLE']
        self.matches = [
            'R1 M1', 'R1 M2', 'GEN이 고른 팀', 'R2 M1', 'R2 M2',
            'R1 LB', 'R2 LB', 'R3 UB', 'R3 LB', 'R4 LF', 'Grand Final'
        ]
    
    def load_current_results(self):
        """현재 경기 결과 로드"""
        results = {}
        if os.path.exists(self.match_file):
            with open(self.match_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        key, value = line.strip().split(' : ', 1)
                        results[key.strip()] = value.strip() if value.strip() else None
        else:
            # 파일이 없으면 생성
            results = {match: None for match in self.matches}
            self.save_results(results)
        
        return results
    
    def save_results(self, results):
        """경기 결과 저장"""
        with open(self.match_file, 'w', encoding='utf-8') as f:
            for match in self.matches:
                result = results.get(match, '')
                f.write(f"{match} : {result}\n")
    
    def display_current_status(self, results):
        """현재 상태 표시"""
        print("\n=== 현재 경기 결과 ===")
        for i, match in enumerate(self.matches, 1):
            result = results.get(match)
            status = f"✅ {result}" if result else "⏳ 경기 예정"
            print(f"{i:2d}. {match:<15} : {status}")
        
        completed = sum(1 for r in results.values() if r)
        print(f"\n진행률: {completed}/{len(self.matches)} ({completed/len(self.matches)*100:.1f}%)")
    
    def get_next_match(self, results):
        """다음 경기 찾기"""
        for match in self.matches:
            if not results.get(match):
                return match
        return None
    
    def update_match_interactive(self):
        """대화형 경기 결과 업데이트"""
        print("🏆 LCK 플레이오프 경기 결과 업데이트")
        print("=" * 50)
        
        results = self.load_current_results()
        self.display_current_status(results)
        
        next_match = self.get_next_match(results)
        
        if not next_match:
            print("\n🎉 모든 경기가 완료되었습니다!")
            return
        
        print(f"\n📢 다음 경기: {next_match}")
        
        # 팀 선택
        print(f"\n사용 가능한 팀: {', '.join(self.teams)}")
        
        while True:
            winner = input(f"\n{next_match}의 승리팀을 입력하세요 (취소: q): ").strip()
            
            if winner.lower() == 'q':
                print("업데이트가 취소되었습니다.")
                return
            
            if winner in self.teams:
                break
            else:
                print(f"❌ 올바른 팀명을 입력하세요: {', '.join(self.teams)}")
        
        # 결과 업데이트
        results[next_match] = winner
        self.save_results(results)
        
        print(f"\n✅ {next_match}: {winner} 승리로 업데이트되었습니다!")
        
        # Git 커밋 여부 확인
        if self.is_git_repo():
            commit_msg = f"Update: {next_match} 결과 - {winner} 승리"
            
            if input(f"\nGit에 커밋하시겠습니까? (y/n): ").lower() == 'y':
                if self.git_commit(commit_msg):
                    print("✅ Git 커밋이 완료되었습니다!")
                    
                    if input("GitHub에 푸시하시겠습니까? (y/n): ").lower() == 'y':
                        if self.git_push():
                            print("✅ GitHub 푸시가 완료되었습니다!")
                        else:
                            print("❌ 푸시 실패. 수동으로 푸시해주세요.")
                else:
                    print("❌ 커밋 실패.")
        
        # 업데이트된 상태 표시
        self.display_current_status(results)
    
    def is_git_repo(self):
        """Git 저장소 여부 확인"""
        return os.path.exists('.git')
    
    def git_commit(self, message):
        """Git 커밋"""
        try:
            subprocess.run(['git', 'add', self.match_file], check=True)
            subprocess.run(['git', 'commit', '-m', message], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def git_push(self):
        """Git 푸시"""
        try:
            subprocess.run(['git', 'push'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def update_match_direct(self, match_name, winner):
        """직접 경기 결과 업데이트"""
        if match_name not in self.matches:
            print(f"❌ 올바르지 않은 경기명: {match_name}")
            print(f"사용 가능한 경기: {', '.join(self.matches)}")
            return False
        
        if winner not in self.teams:
            print(f"❌ 올바르지 않은 팀명: {winner}")
            print(f"사용 가능한 팀: {', '.join(self.teams)}")
            return False
        
        results = self.load_current_results()
        results[match_name] = winner
        self.save_results(results)
        
        print(f"✅ {match_name}: {winner} 승리로 업데이트되었습니다!")
        return True

def main():
    updater = MatchUpdater()
    
    if len(sys.argv) == 1:
        # 대화형 모드
        updater.update_match_interactive()
    elif len(sys.argv) == 3:
        # 직접 업데이트 모드
        match_name = sys.argv[1]
        winner = sys.argv[2]
        updater.update_match_direct(match_name, winner)
    else:
        print("사용법:")
        print("  python update_match.py                    # 대화형 모드")
        print("  python update_match.py '경기명' '승리팀'   # 직접 업데이트")
        print()
        print("예시:")
        print("  python update_match.py 'R1 M1' 'T1'")

if __name__ == "__main__":
    main()