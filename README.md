# Novel Studio for Copilot CLI

Novel Studio is an English-only, multi-agent novel creation workflow for GitHub Copilot CLI. It uses deterministic file targets, a generated workflow manifest, and fixed project folders so agents do not improvise their outputs.

## Overview

The system uses specialized agents for planning, chapter writing, editing, and feedback. The main controller creates the project skeleton first, then runs each step in order.

## Core Workflow

1. Bootstrap a project with `scripts/bootstrap_project.py`.
2. Write the request concept into `phase1_planning/concept.md`.
3. Generate the remaining planning files in `phase1_planning/`.
4. Write each chapter through `phase2_chapters/`.
5. Integrate the complete novel into `phase3_final/`.

## Project Structure

```text
projects/<project_name>/
├── phase1_planning/
├── phase2_chapters/
├── phase3_final/
└── .novel-studio/
```

## Features

- Deterministic file targets for every agent
- Project-level workflow manifest
- Status tracking and resume support
- Chapter-by-chapter scene specialization
- Post-write validation hooks

## Quick Start

```bash
python scripts/bootstrap_project.py projects/<project_name> --title "<title>" --mode review --language English
```

Then open the project in Copilot CLI and request a novel in English.

## Documentation

- `AGENTS.md`
- `WORKFLOW_GUIDE.md`
- `.github/agents/`
- `hooks/README.md`
- `scripts/`

## Contributing

Contributions are welcome. Keep changes deterministic, English-only, and file-targeted.
