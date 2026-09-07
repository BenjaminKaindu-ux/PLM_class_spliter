# PLM Class Splitter Constitution

## Core Principles

### I. Domain-Adaptive PLM Architecture
The system MUST maintain a core PLM architecture that is domain-agnostic and adaptable across subject areas. Domain-specific behavior MUST be achieved through configuration and data pipelines, NOT through architectural changes. The workflow MUST remain consistent regardless of target domain.

### II. Dataset-Driven Training
All PLM models MUST be trained using curated, publicly available datasets from verified sources (e.g., HuggingFace Hub). Datasets MUST be validated for format compatibility before training. Model quality MUST be measured against domain-specific benchmarks.

### III. Class-First Design
Every feature and component MUST be designed with the target classes (Chess, Geography, Python) as first-class concerns. Class-specific adaptations MUST be documented and versioned separately from core architecture.

### IV. Reproducibility & Versioning
All model training runs, dataset versions, and configuration changes MUST be logged with sufficient detail to enable full reproducibility. Semantic versioning MUST be applied to model releases.

### V. Modularity & Extensibility
The system MUST support adding new domain classes without modifying core components. Each class implementation MUST be self-contained and independently testable.

## Supported Classes & Datasets

| Class | Primary Dataset | Secondary Dataset | Source |
|-------|-----------------|-------------------|--------|
| Chess | Lichess/chess-puzzles (6.1M puzzles) | — | HuggingFace |
| Geography | GeoGPT-Research-Project/GeoGPT-QA (41.4K QA) | sahitiy51/geochain (1.4M CoT pairs) | HuggingFace |
| Python | codefuse-ai/CodeExercise-Python-27k (27K exercises) | — | HuggingFace |

## Technical Constraints

- Core architecture MUST NOT be modified when adding or changing classes
- Workflow MUST remain consistent across all supported classes
- All datasets MUST be sourced from HuggingFace Hub
- Models MUST be evaluated using class-appropriate metrics

## Development Workflow

- All changes MUST follow the established Spec Kit workflow
- Constitution updates require version bump and amendment date update
- New classes require dataset validation before integration
- Testing MUST cover all supported classes for regression prevention

## Governance

This constitution is the authoritative reference for project architecture and class support decisions. Amendments require:
1. Documentation of the change rationale
2. Version bump following semantic versioning rules
3. Update of the Last Amended date
4. Review of impact on all supported classes

All PRs and reviews MUST verify compliance with this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-09-07 | **Last Amended**: 2026-09-07
