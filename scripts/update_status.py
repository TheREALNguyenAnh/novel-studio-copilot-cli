#!/usr/bin/env python3
"""Update project status using deterministic file-level milestones."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path


PHASE1_PROGRESS = {
    "concept.md": ("phase1", 10, "concept"),
    "story_structure.md": ("phase1", 20, "story_structure"),
    "character_profiles.md": ("phase1", 30, "character_profiles"),
    "setting_world.md": ("phase1", 40, "setting_world"),
    "genre_analysis.md": ("phase1", 50, "genre_analysis"),
    "pacing_plan.md": ("phase1", 60, "pacing_plan"),
    "final_plan.md": ("phase1", 70, "final_plan"),
}


def _normalize_file_name(completed_file: str) -> str:
    return Path(completed_file).name.lower()


def _chapter_progress(completed_file: str) -> tuple[str, int, str] | None:
    name = _normalize_file_name(completed_file)
    match = re.search(r"chapter_?(\d+)", name)
    if not match:
        return None

    chapter_number = int(match.group(1))
    if name.endswith("outline.md"):
        return ("phase2", 70 + chapter_number, f"chapter_{chapter_number:02d}_outline")
    if name.endswith("draft.md"):
        return ("phase2", 73 + chapter_number, f"chapter_{chapter_number:02d}_draft")
    if name.endswith("pacing_notes.md"):
        return ("phase2", 76 + chapter_number, f"chapter_{chapter_number:02d}_pacing_notes")
    if name.endswith("editorial_notes.md"):
        return ("phase2", 79 + chapter_number, f"chapter_{chapter_number:02d}_editorial_notes")
    if name.endswith("final.md"):
        return ("phase2", 82 + chapter_number, f"chapter_{chapter_number:02d}_final")

    return ("phase2", 70 + chapter_number, f"chapter_{chapter_number:02d}")


def _final_progress(completed_file: str) -> tuple[str, int, str] | None:
    name = _normalize_file_name(completed_file)
    if "phase3_final" not in Path(completed_file).as_posix().lower():
        return None

    if name.endswith("novel.md"):
        return ("phase3", 90, "novel")
    if name.endswith("editorial_report.md"):
        return ("phase3", 95, "editorial_report")
    if name.endswith("feedback_report.md"):
        return ("phase3", 98, "feedback_report")
    if name.endswith("novel_final.md"):
        return ("phase3", 100, "novel_final")

    return ("phase3", 90, "phase3_final")


def update_status(project_dir: str, operation: str, completed_file: str) -> None:
    """Update .novel-studio/status.json with exact file-level progress."""

    status_file = Path(project_dir) / ".novel-studio" / "status.json"
    status_file.parent.mkdir(parents=True, exist_ok=True)

    if status_file.exists():
        status = json.loads(status_file.read_text(encoding="utf-8"))
    else:
        status = {
            "project_id": Path(project_dir).name,
            "created_at": datetime.now().isoformat(),
            "phase": "init",
            "progress": 0,
            "completed_tasks": [],
        }

    timestamp = datetime.now().isoformat()
    status["last_updated"] = timestamp
    status["last_operation"] = operation
    status["last_file"] = completed_file

    phase_info = PHASE1_PROGRESS.get(_normalize_file_name(completed_file))
    if phase_info is None:
        phase_info = _chapter_progress(completed_file)
    if phase_info is None:
        phase_info = _final_progress(completed_file)

    if phase_info is not None:
        status["phase"], status["progress"], status["current_step"] = phase_info

    status["completed_tasks"].append(
        {
            "operation": operation,
            "file": completed_file,
            "timestamp": timestamp,
        }
    )

    status_file.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"📊 상태 업데이트: {status['phase']} ({status['progress']}%)")


def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: update_status.py <project_dir> <operation> <file>")
        sys.exit(1)

    update_status(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
