#!/usr/bin/env python3
"""
Launcher for Super-Algo Visualizers.
Usage:
  python scripts/open_visualizer.py         -> Opens Skill Tree & 5-Level Explorer
  python scripts/open_visualizer.py anim    -> Opens UCPC 2026 Interactive Animator
"""
import sys
import webbrowser
from pathlib import Path

def main():
    target = "ucpc_animator.html" if len(sys.argv) > 1 and "anim" in sys.argv[1].lower() else "index.html"
    html_path = Path(__file__).parent.parent / "web" / target
    abs_uri = html_path.resolve().as_uri()
    print(f"Відкриваємо {target} у браузері: {abs_uri}")
    webbrowser.open(abs_uri)

if __name__ == "__main__":
    main()
