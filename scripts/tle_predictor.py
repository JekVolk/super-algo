#!/usr/bin/env python3
"""
Time Limit Exceeded (TLE) & Complexity Budget Predictor.
Calculates approximate operations and checks against contest time limits.
"""

import argparse
import math
import sys

# Force UTF-8 for Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def estimate_ops(complexity_expr: str, n: int, m: int = 0) -> float:
    c = complexity_expr.lower().replace(" ", "").replace("*", "")
    
    if c in ["1", "o(1)"]:
        return 1.0
    if c in ["logn", "o(logn)"]:
        return math.log2(n)
    if c in ["sqrtn", "o(sqrtn)"]:
        return math.isqrt(n)
    if c in ["n", "o(n)"]:
        return float(n)
    if c in ["nlogn", "o(nlogn)"]:
        return n * math.log2(n)
    if c in ["n^2", "n2", "o(n^2)", "o(n2)"]:
        return float(n) ** 2
    if c in ["n^3", "n3", "o(n^3)", "o(n3)"]:
        return float(n) ** 3
    if c in ["n*m", "nm", "o(nm)"]:
        return float(n) * (float(m) if m > 0 else float(n))
    if c in ["2^n", "2n", "o(2^n)"]:
        return 2.0 ** min(n, 60)
    if c in ["2^n*n", "o(2^n*n)"]:
        return (2.0 ** min(n, 60)) * n
    if c in ["3^n", "o(3^n)"]:
        return 3.0 ** min(n, 38)
    
    raise ValueError(f"Невідомий формат складності: {complexity_expr}")

def check_budget(n: int, m: int, complexity: str, time_limit: float = 1.0, lang: str = "cpp"):
    ops = estimate_ops(complexity, n, m)
    
    # Heuristics:
    # Modern online judge (Codeforces/Eolymp/AtCoder):
    # C++ ~ 4 * 10^8 simple operations / second
    # Python ~ 3 * 10^7 simple operations / second
    ops_per_sec = 4e8 if lang.lower() in ["cpp", "c++"] else 3.5e7
    estimated_time = ops / ops_per_sec
    safe_limit = time_limit * 0.7  # 30% margin for I/O and constants
    
    print("=" * 65)
    print(" ⏱️ TLE PREDICTOR & COMPLEXITY BUDGET (SUPER-ALGO)")
    print("=" * 65)
    print(f" Параметри: N = {n:,}, M = {m:,}, Складність = {complexity.upper()}")
    print(f" Ліміт часу: {time_limit}с | Мова: {lang.upper()}")
    print(f" Орієнтовна кількість базових операцій: {ops:,.0f}")
    print(f" Очікуваний час виконання: ~{estimated_time:.3f}с")
    print("-" * 65)

    if estimated_time <= safe_limit:
        print(" [OK] БЕЗПЕЧНО! Рішення гарантовано вкладається в ліміт часу з запасом.")
    elif estimated_time <= time_limit:
        print(" [?] РИЗИКОВАНА ЗОНА! Можливий TLE через константи (std::endl, vector copy, I/O).")
        print("    Порада: оптимізуйте ввід (fast I/O), уникайте зайвих алокацій.")
    else:
        print(f" [!] TLE ГАРАНТОВАНО! Перевищення ліміту у {estimated_time / time_limit:.1f} разів.")
        print("    Порада: оберіть більш оптимальний алгоритм з docs/ALGORITHM_DECISION_TREE.md.")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Predict TLE and check complexity budget")
    parser.add_argument("--n", type=int, required=True, help="Розмір вхідних даних N")
    parser.add_argument("--m", type=int, default=0, help="Параметр M (якщо є)")
    parser.add_argument("--complexity", "-c", type=str, required=True, help="Складність (напр. 'N', 'NlogN', 'N^2', '2^N*N')")
    parser.add_argument("--tl", type=float, default=1.0, help="Ліміт часу в секундах (за замовчуванням 1.0)")
    parser.add_argument("--lang", type=str, default="cpp", help="Мова ('cpp' або 'py')")
    args = parser.parse_args()

    check_budget(args.n, args.m, args.complexity, args.tl, args.lang)

if __name__ == "__main__":
    main()
