#!/usr/bin/env python3
"""
Common Pitfalls & Anti-Pattern Detector for Competitive Programming.
Scans C++ and Python source files for known bugs that cause WA, TLE, MLE, or UB.
"""

import argparse
import re
import sys
from pathlib import Path

# Force UTF-8 for stdout/stderr to avoid Windows cp1251 console encoding errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

PITFALL_RULES_CPP = [
    {
        "id": "CPP-001",
        "name": "32-bit Bitwise Shift Overflow",
        "pattern": r"\b1\s*<<\s*([3-9]\d|[3-6][0-9])\b",
        "severity": "CRITICAL",
        "msg": "Зсув `1 << k` при k >= 31 спричиняє невизначену поведінку (UB / переповнення 32-біт). Замініть на `1LL << k` або `1ULL << k`.",
    },
    {
        "id": "CPP-002",
        "name": "std::endl Performance Trap (TLE)",
        "pattern": r"\bcout\s*<<.*<<\s*endl\b",
        "severity": "WARNING",
        "msg": "Використання `std::endl` форсує скидання буфера (flush) після кожного виводу. Замініть на `'\\n'` для уникнення TLE.",
    },
    {
        "id": "CPP-003",
        "name": "Missing Fast I/O Sync Disconnect",
        "custom_check": lambda code: ("cin >>" in code or "cout <<" in code) and not ("cin.tie" in code or "sync_with_stdio" in code),
        "severity": "WARNING",
        "msg": "Код використовує cin/cout без `ios_base::sync_with_stdio(0); cin.tie(0);`. Це може призвести до TLE на тестах з великим вводом.",
    },
    {
        "id": "CPP-004",
        "name": "Undefined Behavior with __builtin_clz(0) or __builtin_ctz(0)",
        "pattern": r"\b__builtin_c[lt]z(ll)?\s*\(\s*0\s*\)",
        "severity": "CRITICAL",
        "msg": "Виклик `__builtin_clz(0)` або `__builtin_ctz(0)` повертає UB на більшості архітектур x86/ARM! Додайте перевірку `if (x > 0)`.",
    },
    {
        "id": "CPP-005",
        "name": "Suspicious Modulo Order (Operator Precedence)",
        "pattern": r"\b(1LL\s*\*\s*)?[a-zA-Z0-9_]+\s*\+\s*[a-zA-Z0-9_]+\s*%\s*(MOD|mod|1000000007|998244353)\b",
        "severity": "HIGH",
        "msg": "Оператор `%` має вищий пріоритет за `+`. Вираз `a + b % MOD` обчислюється як `a + (b % MOD)`. Потрібно `(a + b) % MOD`.",
    },
    {
        "id": "CPP-006",
        "name": "Segment Tree Array Size (< 4 * N)",
        "pattern": r"\b(tree|seg|segtree)\s*\[\s*(2\s*\*\s*(MAXN|N|100000|200000|500000)|MAXN|N)\s*\]",
        "severity": "HIGH",
        "msg": "Виділення пам'яті для дерева відрізків менше ніж `4 * N` часто веде до Out of Bounds / SIGSEGV на неповних шарах дерева.",
    }
]

PITFALL_RULES_PYTHON = [
    {
        "id": "PY-001",
        "name": "Slow sys.stdin Input",
        "custom_check": lambda code: "for _ in range(" in code and "input()" in code and "sys.stdin.readline" not in code,
        "severity": "WARNING",
        "msg": "Використання вбудованого `input()` у циклах. Замініть на `sys.stdin.readline` для 5x-10x прискорення читання.",
    },
    {
        "id": "PY-002",
        "name": "Default Recursion Limit Trap",
        "custom_check": lambda code: ("def dfs" in code or "def traverse" in code) and "setrecursionlimit" not in code,
        "severity": "HIGH",
        "msg": "Рекурсивний DFS без `sys.setrecursionlimit(300000)`. За замовчуванням ліміт 1000 викличе `RecursionError`.",
    },
    {
        "id": "PY-003",
        "name": "Quadratic String Concatenation in Loop",
        "pattern": r"for\s+.*:\s*\n\s+([a-zA-Z_]\w*)\s*\+=\s*",
        "severity": "MEDIUM",
        "msg": "Конкатенація рядків у циклі `s += char` створює нові копії рядка за O(N^2). Використовуйте списки та `''.join(arr)`.",
    }
]

def scan_file(file_path: Path):
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8", errors="ignore")
    findings = []
    suffix = file_path.suffix.lower()

    rules = PITFALL_RULES_CPP if suffix in [".cpp", ".cc", ".cxx", ".h", ".hpp"] else (
        PITFALL_RULES_PYTHON if suffix == ".py" else []
    )

    for rule in rules:
        matched = False
        if "pattern" in rule:
            if re.search(rule["pattern"], content):
                matched = True
        elif "custom_check" in rule:
            if rule["custom_check"](content):
                matched = True

        if matched:
            findings.append((rule["severity"], rule["id"], rule["name"], rule["msg"]))

    return findings

def main():
    parser = argparse.ArgumentParser(description="Common Pitfalls & Anti-Pattern Detector for CP")
    parser.add_argument("paths", nargs="+", help="Файли або директорії для сканування")
    args = parser.parse_args()

    total_issues = 0
    scanned_count = 0

    print("=" * 65)
    print(" [*] ДЕТЕКТОР ГРАБЛІВ ТА ОЛІМПІАДНИХ АНТИПАТТЕРНІВ (SUPER-ALGO)")
    print("=" * 65)

    files_to_scan = []
    for p_str in args.paths:
        p = Path(p_str)
        if p.is_file():
            files_to_scan.append(p)
        elif p.is_dir():
            files_to_scan.extend(p.glob("**/*.cpp"))
            files_to_scan.extend(p.glob("**/*.py"))

    for f in files_to_scan:
        scanned_count += 1
        issues = scan_file(f)
        if issues:
            print(f"\n[FILE] {f}")
            for sev, rule_id, name, msg in issues:
                total_issues += 1
                icon = "[!]" if sev == "CRITICAL" else ("[?]" if sev == "HIGH" else "[i]")
                print(f"  {icon} [{sev}] {rule_id}: {name}")
                print(f"      Порада: {msg}")

    print("\n" + "=" * 65)
    print(f" Підсумок: проскановано {scanned_count} файлів, виявлено {total_issues} зауважень.")
    if total_issues == 0:
        print(" Все чисто! Код відповідає високим стандартам олімпіадного захисту.")
    print("=" * 65)

if __name__ == "__main__":
    main()
