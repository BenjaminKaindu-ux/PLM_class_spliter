# Tasks: Class Switch to Geography, Python, Chess

**Input**: Design documents from `/specs/001-class-switch-geo-python-chess/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in feature specification - tests are OPTIONAL

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan (src/models/, src/configs/, src/datasets/, src/training/, src/utils/)
- [ ] T002 Initialize Python project with required dependencies (datasets, transformers, pytorch)
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create base Class Configuration entity in src/models/class_config.py
- [ ] T005 Create base Dataset Reference entity in src/models/dataset_reference.py
- [ ] T006 Create base Training Job entity in src/models/training_job.py
- [ ] T007 Create base Model Artifact entity in src/models/model_artifact.py
- [ ] T008 [P] Implement Class Configuration loading interface in src/configs/loader.py
- [ ] T009 [P] Implement Dataset Loading interface in src/datasets/loader.py
- [ ] T010 [P] Implement Preprocessing interface in src/training/preprocessor.py
- [ ] T011 [P] Implement Training Pipeline interface in src/training/pipeline.py
- [ ] T012 [P] Implement Model Evaluation interface in src/training/evaluator.py
- [ ] T013 [P] Implement System Startup interface in src/utils/startup.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Geography PLM Training (Priority: P1) 🎯 MVP

**Goal**: Train a perceptual and adaptive learning module on Geography using GeoGPT-QA and geochain datasets

**Independent Test**: Run PLM training pipeline with Geography datasets and verify model produces geography-appropriate outputs

### Implementation for User Story 1

- [ ] T014 [P] [US1] Create Geography class configuration in src/configs/geography.yaml
- [ ] T015 [P] [US1] Create GeoGPT-QA dataset adapter in src/datasets/geogpt_qa.py
- [ ] T016 [P] [US1] Create geochain dataset adapter in src/datasets/geochain.py
- [ ] T017 [US1] Implement Geography preprocessing rules in src/training/preprocessors/geography.py
- [ ] T018 [US1] Implement Geography evaluation metrics in src/training/metrics/geography.py
- [ ] T019 [US1] Test Geography class configuration loading
- [ ] T020 [US1] Test Geography dataset loading (GeoGPT-QA and geochain)
- [ ] T021 [US1] Test Geography preprocessing pipeline
- [ ] T022 [US1] Run Geography training pipeline with small dataset subset
- [ ] T023 [US1] Validate Geography model outputs

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Python PLM Training (Priority: P2)

**Goal**: Train a perceptual and adaptive learning module on Python using CodeExercise-Python-27k dataset

**Independent Test**: Run PLM training pipeline with Python dataset and verify model produces Python-appropriate outputs

### Implementation for User Story 2

- [ ] T024 [P] [US2] Create Python class configuration in src/configs/python.yaml
- [ ] T025 [P] [US2] Create CodeExercise-Python-27k dataset adapter in src/datasets/code_exercise_python.py
- [ ] T026 [US2] Implement Python preprocessing rules in src/training/preprocessors/python.py
- [ ] T027 [US2] Implement Python evaluation metrics in src/training/metrics/python.py
- [ ] T028 [US2] Test Python class configuration loading
- [ ] T029 [US2] Test Python dataset loading (CodeExercise-Python-27k)
- [ ] T030 [US2] Test Python preprocessing pipeline
- [ ] T031 [US2] Run Python training pipeline with small dataset subset
- [ ] T032 [US2] Validate Python model outputs

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Chess PLM Training (Priority: P3)

**Goal**: Train a perceptual and adaptive learning module on Chess using Lichess/chess-puzzles dataset

**Independent Test**: Run PLM training pipeline with Chess dataset and verify model produces chess-appropriate outputs

### Implementation for User Story 3

- [ ] T033 [P] [US3] Create Chess class configuration in src/configs/chess.yaml
- [ ] T034 [P] [US3] Create Lichess/chess-puzzles dataset adapter in src/datasets/chess_puzzles.py
- [ ] T035 [US3] Implement Chess preprocessing rules in src/training/preprocessors/chess.py
- [ ] T036 [US3] Implement Chess evaluation metrics in src/training/metrics/chess.py
- [ ] T037 [US3] Test Chess class configuration loading
- [ ] T038 [US3] Test Chess dataset loading (Lichess/chess-puzzles)
- [ ] T039 [US3] Test Chess preprocessing pipeline
- [ ] T040 [US3] Run Chess training pipeline with small dataset subset
- [ ] T041 [US3] Validate Chess model outputs

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T042 [P] Implement class switching functionality in src/utils/class_switcher.py
- [ ] T043 [P] Add comprehensive error handling across all modules
- [ ] T044 [P] Add logging for training operations across all classes
- [ ] T045 Implement dataset validation before training in src/datasets/validator.py
- [ ] T046 Run quickstart.md validation scenarios
- [ ] T047 Create documentation for class configurations
- [ ] T048 Performance optimization across all classes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Geography class configuration in src/configs/geography.yaml"
Task: "Create GeoGPT-QA dataset adapter in src/datasets/geogpt_qa.py"
Task: "Create geochain dataset adapter in src/datasets/geochain.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
