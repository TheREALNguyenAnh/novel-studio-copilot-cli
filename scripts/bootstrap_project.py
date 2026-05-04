#!/usr/bin/env python3
"""Create a deterministic Novel Studio project skeleton and workflow manifest."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


PHASE1_FILES = [
    "concept.md",
    "story_structure.md",
    "character_profiles.md",
    "setting_world.md",
    "genre_analysis.md",
    "pacing_plan.md",
    "final_plan.md",
]

CHAPTER_FILES = [
    "outline.md",
    "dialogue_scene.md",
    "action_scene.md",
    "emotion_scene.md",
    "prose_scene.md",
    "draft.md",
    "pacing_notes.md",
    "editorial_notes.md",
    "final.md",
]

PHASE3_FILES = [
    "novel.md",
    "editorial_report.md",
    "feedback_report.md",
    "novel_final.md",
]


def build_manifest(project_name: str, title: str, mode: str, language: str, chapters: int) -> dict:
    workflow_steps = [
        {"id": "phase1.concept", "agent": "main-writer", "input": ["request.md"], "output": "phase1_planning/concept.md"},
        {"id": "phase1.story_structure", "agent": "story-writer", "input": ["phase1_planning/concept.md"], "output": "phase1_planning/story_structure.md"},
        {"id": "phase1.character_profiles", "agent": "character-writer", "input": ["phase1_planning/concept.md"], "output": "phase1_planning/character_profiles.md"},
        {"id": "phase1.setting_world", "agent": "setting-writer", "input": ["phase1_planning/concept.md"], "output": "phase1_planning/setting_world.md"},
        {"id": "phase1.genre_analysis", "agent": "genre-specialist", "input": ["phase1_planning/concept.md"], "output": "phase1_planning/genre_analysis.md"},
        {"id": "phase1.pacing_plan", "agent": "pacing-manager", "input": ["phase1_planning/final_plan.md", "phase1_planning/story_structure.md"], "output": "phase1_planning/pacing_plan.md"},
        {"id": "phase1.final_plan", "agent": "main-writer", "input": ["phase1_planning/story_structure.md", "phase1_planning/character_profiles.md", "phase1_planning/setting_world.md", "phase1_planning/genre_analysis.md", "phase1_planning/pacing_plan.md"], "output": "phase1_planning/final_plan.md"},
    ]

    for chapter_number in range(1, chapters + 1):
        chapter = f"chapter_{chapter_number:02d}"
        workflow_steps.extend(
            [
                {
                    "id": f"phase2.{chapter}.outline",
                    "agent": "story-writer",
                    "input": ["phase1_planning/final_plan.md"],
                    "output": f"phase2_chapters/{chapter}/outline.md",
                },
                {
                    "id": f"phase2.{chapter}.dialogue_scene",
                    "agent": "dialogue-writer",
                    "input": [f"phase2_chapters/{chapter}/outline.md", "phase1_planning/character_profiles.md"],
                    "output": f"phase2_chapters/{chapter}/dialogue_scene.md",
                },
                {
                    "id": f"phase2.{chapter}.action_scene",
                    "agent": "action-writer",
                    "input": [f"phase2_chapters/{chapter}/outline.md", "phase1_planning/setting_world.md"],
                    "output": f"phase2_chapters/{chapter}/action_scene.md",
                },
                {
                    "id": f"phase2.{chapter}.emotion_scene",
                    "agent": "emotion-writer",
                    "input": [f"phase2_chapters/{chapter}/outline.md", "phase1_planning/character_profiles.md"],
                    "output": f"phase2_chapters/{chapter}/emotion_scene.md",
                },
                {
                    "id": f"phase2.{chapter}.prose_scene",
                    "agent": "prose-writer",
                    "input": [f"phase2_chapters/{chapter}/outline.md", "phase1_planning/final_plan.md"],
                    "output": f"phase2_chapters/{chapter}/prose_scene.md",
                },
                {
                    "id": f"phase2.{chapter}.draft",
                    "agent": "main-writer",
                    "input": [
                        f"phase2_chapters/{chapter}/outline.md",
                        f"phase2_chapters/{chapter}/dialogue_scene.md",
                        f"phase2_chapters/{chapter}/action_scene.md",
                        f"phase2_chapters/{chapter}/emotion_scene.md",
                        f"phase2_chapters/{chapter}/prose_scene.md",
                    ],
                    "output": f"phase2_chapters/{chapter}/draft.md",
                },
                {
                    "id": f"phase2.{chapter}.pacing_notes",
                    "agent": "pacing-manager",
                    "input": [f"phase2_chapters/{chapter}/draft.md", "phase1_planning/pacing_plan.md"],
                    "output": f"phase2_chapters/{chapter}/pacing_notes.md",
                },
                {
                    "id": f"phase2.{chapter}.editorial_notes",
                    "agent": "editorial-team",
                    "input": [f"phase2_chapters/{chapter}/draft.md"],
                    "output": f"phase2_chapters/{chapter}/editorial_notes.md",
                },
                {
                    "id": f"phase2.{chapter}.final",
                    "agent": "editorial-team",
                    "input": [f"phase2_chapters/{chapter}/draft.md", f"phase2_chapters/{chapter}/editorial_notes.md", f"phase2_chapters/{chapter}/pacing_notes.md"],
                    "output": f"phase2_chapters/{chapter}/final.md",
                },
            ]
        )

    workflow_steps.extend(
        [
            {
                "id": "phase3.novel",
                "agent": "main-writer",
                "input": [f"phase2_chapters/chapter_{chapter_number:02d}/final.md" for chapter_number in range(1, chapters + 1)],
                "output": "phase3_final/novel.md",
            },
            {
                "id": "phase3.editorial_report",
                "agent": "editorial-team",
                "input": ["phase3_final/novel.md"],
                "output": "phase3_final/editorial_report.md",
            },
            {
                "id": "phase3.novel_final",
                "agent": "editorial-team",
                "input": ["phase3_final/novel.md", "phase3_final/editorial_report.md"],
                "output": "phase3_final/novel_final.md",
            },
            {
                "id": "phase3.feedback_report",
                "agent": "feedback-agent",
                "input": ["phase3_final/novel_final.md"],
                "output": "phase3_final/feedback_report.md",
            },
        ]
    )

    return {
        "project_id": project_name,
        "title": title,
        "mode": mode,
        "language": language,
        "created_at": datetime.now().isoformat(),
        "current_step": "phase1.concept",
        "status": "planning",
        "chapters": chapters,
        "workflow_steps": workflow_steps,
    }


def create_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap a deterministic Novel Studio project skeleton.")
    parser.add_argument("project_dir", help="Project directory to create")
    parser.add_argument("--title", default="Untitled Novel", help="Novel title")
    parser.add_argument("--mode", default="review", choices=["auto", "review", "manual"], help="Workflow mode")
    parser.add_argument("--language", default="English", help="Workflow language")
    parser.add_argument("--chapters", type=int, default=3, help="Number of chapters")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    novel_studio_dir = project_dir / ".novel-studio"
    phase1_dir = project_dir / "phase1_planning"
    phase2_dir = project_dir / "phase2_chapters"
    phase3_dir = project_dir / "phase3_final"

    for folder in [novel_studio_dir / "checkpoints", novel_studio_dir / "backups", phase1_dir, phase2_dir, phase3_dir]:
        folder.mkdir(parents=True, exist_ok=True)

    for file_name in PHASE1_FILES:
        create_text_file(phase1_dir / file_name, f"# {file_name.replace('_', ' ').replace('.md', '').title()}\n\n[To be written by the assigned agent]\n")

    for chapter_number in range(1, args.chapters + 1):
        chapter_dir = phase2_dir / f"chapter_{chapter_number:02d}"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        for file_name in CHAPTER_FILES:
            title = file_name.replace("_", " ").replace(".md", "").title()
            create_text_file(chapter_dir / file_name, f"# Chapter {chapter_number:02d} - {title}\n\n[To be written by the assigned agent]\n")

    for file_name in PHASE3_FILES:
        create_text_file(phase3_dir / file_name, f"# {file_name.replace('_', ' ').replace('.md', '').title()}\n\n[To be written by the assigned agent]\n")

    create_text_file(
        project_dir / "request.md",
        "# Request\n\n[Paste the user prompt or project brief here before starting the workflow.]\n",
    )

    manifest = build_manifest(project_dir.name, args.title, args.mode, args.language, args.chapters)
    (novel_studio_dir / "workflow_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    status = {
        "project_id": project_dir.name,
        "title": args.title,
        "mode": args.mode,
        "language": args.language,
        "created_at": datetime.now().isoformat(),
        "phase": "init",
        "progress": 0,
        "current_step": "phase1.concept",
        "completed_tasks": [],
    }
    (novel_studio_dir / "status.json").write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Created deterministic project skeleton at {project_dir}")
    print(f"Workflow manifest: {novel_studio_dir / 'workflow_manifest.json'}")
    print(f"Status file: {novel_studio_dir / 'status.json'}")


if __name__ == "__main__":
    main()