# Novel Studio Workflow Guide

This guide defines the deterministic English-only workflow used by Copilot CLI.

The project skeleton must be created first. Every agent then writes only the file assigned in `.novel-studio/workflow_manifest.json`.

## Project Structure

```text
projects/<project_name>/
├── phase1_planning/
│   ├── concept.md
│   ├── story_structure.md
│   ├── character_profiles.md
│   ├── setting_world.md
│   ├── genre_analysis.md
│   ├── pacing_plan.md
│   └── final_plan.md
├── phase2_chapters/
│   ├── chapter_01/
│   │   ├── outline.md
│   │   ├── dialogue_scene.md
│   │   ├── action_scene.md
│   │   ├── emotion_scene.md
│   │   ├── prose_scene.md
│   │   ├── draft.md
│   │   ├── pacing_notes.md
│   │   ├── editorial_notes.md
│   │   └── final.md
│   ├── chapter_02/
│   └── chapter_03/
├── phase3_final/
│   ├── novel.md
│   ├── editorial_report.md
│   ├── feedback_report.md
│   └── novel_final.md
└── .novel-studio/
    ├── status.json
    ├── workflow_manifest.json
    ├── checkpoints/
    └── backups/
```

## Phase 1

- `@main-writer` writes `phase1_planning/concept.md`.
- `@story-writer` writes `phase1_planning/story_structure.md`.
- `@character-writer` writes `phase1_planning/character_profiles.md`.
- `@setting-writer` writes `phase1_planning/setting_world.md`.
- `@genre-specialist` writes `phase1_planning/genre_analysis.md`.
- `@pacing-manager` writes `phase1_planning/pacing_plan.md`.
- `@main-writer` integrates the planning files into `phase1_planning/final_plan.md`.

## Phase 2

For each chapter:

- `@story-writer` creates `outline.md`.
- `@dialogue-writer`, `@action-writer`, `@emotion-writer`, and `@prose-writer` write their scene files.
- `@main-writer` integrates the scene files into `draft.md`.
- `@pacing-manager` writes `pacing_notes.md`.
- `@editorial-team` writes `editorial_notes.md` and `final.md`.

## Phase 3

- `@main-writer` integrates all chapter finals into `phase3_final/novel.md`.
- `@editorial-team` writes `phase3_final/editorial_report.md` and `phase3_final/novel_final.md`.
- `@feedback-agent` writes `phase3_final/feedback_report.md`.

## Resume Rule

Read `.novel-studio/status.json` and continue from `current_step`.

## Approval Points

- Phase 1 completion
- Each chapter completion
- Final completion

## Example

```text
@copilot Read WORKFLOW_GUIDE.md and write a novel about "college students' first love" as project "my_first_novel" in review mode.
```
