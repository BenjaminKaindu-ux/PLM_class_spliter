# Implementation Plan: Class Switch to Geography, Python, Chess

**Branch**: `001-class-switch-geo-python-chess` | **Date**: 2026-09-07 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-class-switch-geo-python-chess/spec.md`

## Summary

Replace existing PLM class configurations (MATH 223, CLAS 280, CHEM 251) with Geography, Python, and Chess classes while maintaining the same core architecture and workflow. The system will build perceptual and adaptive learning modules using HuggingFace datasets: Lichess/chess-puzzles (Chess), GeoGPT-QA and geochain (Geography), and CodeExercise-Python-27k (Python).

## Technical Context

**Language/Version**: NEEDS CLARIFICATION

**Primary Dependencies**: NEEDS CLARIFICATION

**Storage**: N/A (model artifacts stored locally)

**Testing**: NEEDS CLARIFICATION

**Target Platform**: NEEDS CLARIFICATION

**Project Type**: NEEDS CLARIFICATION (likely library or CLI tool for PLM training)

**Performance Goals**: Train models within same time framework as previous classes

**Constraints**: Core architecture MUST NOT be modified; only class configurations change

**Scale/Scope**: 3 classes, 4 datasets total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Check (Phase 0)

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Domain-Adaptive PLM Architecture | PASS | Class-specific behavior through configuration, not architecture changes |
| II. Dataset-Driven Training | PASS | All datasets sourced from HuggingFace Hub with validation |
| III. Class-First Design | PASS | Chess, Geography, Python are target classes |
| IV. Reproducibility & Versioning | PASS | Training runs and dataset versions will be logged |
| V. Modularity & Extensibility | PASS | Each class implementation is self-contained |

**Gate Result**: PASS — no violations

### Post-Design Check (Phase 1)

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Domain-Adaptive PLM Architecture | PASS | Design uses configuration-driven class system; core architecture unchanged |
| II. Dataset-Driven Training | PASS | Data model defines dataset references; contracts specify loading interface |
| III. Class-First Design | PASS | Data model entities are class-centric; configurations are per-class |
| IV. Reproducibility & Versioning | PASS | Training Job entity tracks versions; Model Artifact stores metrics |
| V. Modularity & Extensibility | PASS | Each class is self-contained in configuration; new classes can be added without code changes |

**Gate Result**: PASS — design maintains constitutional compliance

## Project Structure

### Documentation (this feature)

```text
specs/001-class-switch-geo-python-chess/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── models/              # PLM model definitions
├── configs/             # Class configurations (Geography, Python, Chess)
├── datasets/            # Dataset loading and preprocessing
├── training/            # Training pipeline
└── utils/               # Shared utilities

tests/
├── unit/
├── integration/
└── contract/
```

**Structure Decision**: Single project structure with clear separation of concerns between models, configurations, datasets, and training pipeline.

## Complexity Tracking

No constitution violations — complexity tracking not required.

## Phase 0: Research

### Research Tasks

1. **Investigate existing PLM architecture**: Understand current class implementations (MATH 223, CLAS 280, CHEM 251) to identify what needs to be replaced
2. **Dataset format validation**: Verify compatibility of HuggingFace datasets with existing training pipeline
3. **Configuration patterns**: Identify how class-specific settings are currently managed
4. **Training pipeline analysis**: Understand the workflow to ensure no architectural changes are needed

### Research Output

See [research.md](./research.md)

## Phase 1: Design & Contracts

### Design Tasks

1. **Data Model**: Define class configuration structure for Geography, Python, Chess
2. **Interface Contracts**: Document how classes interact with the training pipeline
3. **Quickstart Guide**: Create validation scenarios for each new class

### Design Output

See [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)
