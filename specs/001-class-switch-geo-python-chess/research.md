# Research: Class Switch to Geography, Python, Chess

**Branch**: `001-class-switch-geo-python-chess` | **Date**: 2026-09-07

## Research Tasks Completed

### 1. Dataset Format Analysis

#### Chess: Lichess/chess-puzzles
- **Format**: Parquet files
- **Size**: 6.1M puzzles, ~876.5 MB
- **Schema**: PuzzleId, GameId, FEN, Moves, Rating, RatingDeviation, Popularity, NbPlays, Themes, OpeningTags
- **Data Types**: String identifiers, FEN notation, move sequences, numeric ratings
- **Key Fields**: FEN (board state), Moves (solution sequence), Rating (difficulty level)

#### Geography: GeoGPT-Research-Project/GeoGPT-QA
- **Format**: CSV (parquet available)
- **Size**: 41.4K QA pairs, ~18.8 MB
- **Schema**: index, question, answer, title, authors, doi, journal, volume, pages, license
- **Data Types**: Text QA pairs with academic metadata
- **Key Fields**: question, answer (text content)

#### Geography: sahitiy51/geochain
- **Format**: Parquet files
- **Size**: 1.4M rows, ~464 MB (test + mini_test)
- **Schema**: key, locatability_score, lat, lon, city, sub_folder, class_mapping, sequence_key, image
- **Data Types**: Geographic coordinates, image data, classification labels
- **Key Fields**: image (multimodal), lat/lon (location), class_mapping (classification)

#### Python: codefuse-ai/CodeExercise-Python-27k
- **Format**: Dataset viewer disabled (likely JSON/CSV)
- **Size**: 27K exercises
- **Schema**: Programming exercises with topics (basic syntax, data structures, algorithms, database, ML)
- **Data Types**: Code snippets, problem descriptions, solutions
- **Key Fields**: Exercise content, expected outputs

### 2. Configuration Pattern Analysis

**Current Classes**: MATH 223, CLAS 280, CHEM 251
**Target Classes**: Geography, Python, Chess

**Configuration Requirements**:
- Each class needs dataset source configuration
- Each class needs preprocessing rules (different data formats)
- Each class needs evaluation metrics (domain-specific)
- Each class needs output format specification

### 3. Training Pipeline Considerations

**Pipeline Stages**:
1. Dataset loading (HuggingFace Hub integration)
2. Data validation and format checking
3. Preprocessing (class-specific transformations)
4. Model training (core architecture)
5. Evaluation (domain-appropriate metrics)
6. Model artifact storage

**Architecture Constraints**:
- Core training logic MUST remain unchanged
- Class-specific behavior through configuration only
- No architectural modifications allowed

### 4. Multimodal Considerations

**Geography (geochain)**: Includes image data requiring multimodal processing
- Image loading and preprocessing
- Geographic coordinate handling
- Chain-of-thought question sequences

**Chess**: Text-based FEN and move notation
- FEN parsing and board representation
- Move sequence encoding

**Python**: Code-based exercises
- Code syntax handling
- Execution environment considerations

## Decisions Made

### Decision 1: Configuration-Driven Class System
- **Rationale**: Constitution requires domain-agnostic core architecture
- **Approach**: Define class configurations in separate files, loaded at runtime
- **Alternatives Considered**: Hardcoded class logic (rejected - violates constitution)

### Decision 2: Dataset Abstraction Layer
- **Rationale**: Different datasets have different formats (parquet, CSV, images)
- **Approach**: Create dataset adapters that normalize data for training pipeline
- **Alternatives Considered**: Single format conversion (rejected - inefficient for large datasets)

### Decision 3: Class-Specific Preprocessing
- **Rationale**: Each domain has unique data characteristics
- **Approach**: Preprocessing rules defined in class configuration
- **Alternatives Considered**: Universal preprocessing (rejected - insufficient for multimodal data)

## Open Questions

1. **Existing Codebase**: Need to examine current implementation to understand exact architecture
2. **Training Infrastructure**: Need to confirm computational requirements and environment
3. **Evaluation Metrics**: Need to define domain-specific metrics for each class

## Next Steps

1. Examine existing codebase to understand current architecture
2. Define detailed class configurations
3. Create dataset adapters for each format
4. Establish evaluation metrics for each domain
