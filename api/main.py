"""
FastAPI Modular Backend for Super-Algo.
Stores team member progress, solved problem statuses, notes, and syncs knowledge tree.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Super-Algo API",
    description="Backend сервіс синхронізації знань, прогресу олімпіадної команди та аналітики",
    version="1.0.0"
)

DATA_FILE = Path(__file__).parent / "team_state.json"
KB_FILE = Path(__file__).parent.parent / "docs" / "knowledge_tree.json"

class MemberProgress(BaseModel):
    id: str
    name: str
    role: str
    skills: Dict[str, Any] = {}
    nanos: Dict[str, bool] = {}

class TeamState(BaseModel):
    members: List[MemberProgress]

def load_state() -> List[Dict[str, Any]]:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []

def save_state(data: List[Dict[str, Any]]):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

@app.get("/")
def get_root():
    return {"app": "Super-Algo API", "status": "online", "docs_url": "/docs"}

@app.get("/api/knowledge-tree")
def get_knowledge_tree():
    """Returns the full 5-level knowledge tree hierarchy."""
    if not KB_FILE.exists():
        raise HTTPException(status_code=404, detail="Knowledge tree not found")
    return json.loads(KB_FILE.read_text(encoding="utf-8"))

@app.get("/api/team", response_model=List[Dict[str, Any]])
def get_team_progress():
    """Returns saved progress for all team members."""
    return load_state()

@app.post("/api/team")
def update_team_progress(payload: List[Dict[str, Any]]):
    """Saves updated team progress state."""
    save_state(payload)
    return {"status": "saved", "members_count": len(payload)}

@app.get("/api/stats")
def get_overall_stats():
    """Calculates overall team metrics."""
    members = load_state()
    total_solved = 0
    total_mastered = 0
    for m in members:
        skills = m.get("skills", {})
        for s in skills.values():
            if isinstance(s, dict):
                total_solved += s.get("solved", 0)
                if s.get("status", 0) >= 2:
                    total_mastered += 1
    return {
        "members_count": len(members),
        "total_solved_problems": total_solved,
        "mastered_topics_count": total_mastered
    }
