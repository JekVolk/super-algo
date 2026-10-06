import subprocess
import sys
import os
import time

PROBLEMS = [
    "problem_A_antivirus",
    "problem_B_collectible_pairs",
    "problem_C_dance_of_remainders",
    "problem_D_evens_and_odds",
    "problem_E_four_numbers",
    "problem_F_confused_readings",
    "problem_G_number_game",
    "problem_H_pattern",
    "problem_I_round_table",
    "problem_J_scales",
    "problem_K_sum_and_product",
    "problem_L_three_computers",
    "problem_M_garland",
    "problem_N_weather_diary"
]

def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stage1_dir = os.path.join(base_dir, "ucpc2026_stage1")
    
    print("==================================================================")
    print("[*] RUNNING COMPLETE VERIFICATION SUITE: UCPC 2026 STAGE I (ALL 14)")
    print("==================================================================")
    
    passed = 0
    total = len(PROBLEMS)
    start_time = time.time()
    
    for prob in PROBLEMS:
        prob_dir = os.path.join(stage1_dir, prob)
        runner_path = os.path.join(prob_dir, "test_runner.py")
        if not os.path.exists(runner_path):
            print(f"❌ {prob}: test_runner.py NOT FOUND!")
            continue
            
        p = subprocess.run([sys.executable, runner_path], capture_output=True, text=True, cwd=prob_dir)
        if p.returncode == 0:
            print(f"[OK]   [{prob:28}] -> PASSED (Python 3.12 & verified tests)")
            passed += 1
        else:
            print(f"[FAIL] [{prob:28}] -> FAILED!")
            print(p.stderr or p.stdout)
            
    elapsed = time.time() - start_time
    print("------------------------------------------------------------------")
    print(f"SUMMARY: {passed}/{total} problems verified in {elapsed:.2f}s.")
    if passed == total:
        print("[SUCCESS] 100% PERFECT SCORE! ALL 14 PROBLEMS PASSED AUTOMATED VERIFICATION.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
