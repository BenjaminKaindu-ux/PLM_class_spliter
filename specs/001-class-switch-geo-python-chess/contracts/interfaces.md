# Interface Contracts: Class Switch to Geography, Python, Chess

**Branch**: `001-class-switch-geo-python-chess` | **Date**: 2026-09-07

## Overview

This document defines the interfaces between system components for the PLM class switch feature. These contracts ensure the core architecture remains unchanged while supporting new domain classes.

## Contract 1: Class Configuration Interface

**Purpose**: How class configurations are loaded and interpreted

**Input**: Class identifier string
**Output**: Class Configuration object

### Interface Definition

```
load_class_config(class_id: string) → ClassConfiguration
```

**Preconditions**:
- class_id must reference a valid, registered class
- Configuration file must exist and be parseable

**Postconditions**:
- Returns complete ClassConfiguration object
- All required fields are populated
- Dataset references are validated

**Error Conditions**:
- Invalid class_id → ClassNotFoundException
- Malformed configuration → ConfigurationParseException
- Missing required fields → ValidationException

### Implementation Notes

- Configurations stored in `src/configs/` directory
- Each class has its own configuration file (e.g., `geography.yaml`)
- Configuration loaded at system startup or class switch

## Contract 2: Dataset Loading Interface

**Purpose**: How datasets are fetched from HuggingFace Hub

**Input**: Dataset Reference object
**Output**: Loaded dataset in standardized format

### Interface Definition

```
load_dataset(dataset_ref: DatasetReference) → Dataset
```

**Preconditions**:
- dataset_id must be accessible on HuggingFace Hub
- User must have network access (or cached data available)
- Dataset format must be supported

**Postconditions**:
- Returns dataset in memory or as lazy iterator
- Data conforms to expected schema
- Metadata preserved (row count, column types)

**Error Conditions**:
- Network unavailable → DatasetUnavailableException
- Invalid dataset_id → DatasetNotFoundException
- Format mismatch → FormatException
- Schema validation failure → SchemaException

### Implementation Notes

- Use HuggingFace `datasets` library for loading
- Cache downloaded data locally for reuse
- Validate schema against class configuration

## Contract 3: Preprocessing Interface

**Purpose**: How raw data is transformed for training

**Input**: Raw dataset + preprocessing rules
**Output**: Preprocessed data ready for training

### Interface Definition

```
preprocess(dataset: Dataset, rules: PreprocessingRules) → PreprocessedData
```

**Preconditions**:
- Dataset must be loaded successfully
- Preprocessing rules must be valid for dataset type
- Required dependencies must be installed

**Postconditions**:
- Data transformed according to rules
- Output format compatible with training pipeline
- No data loss without explicit rule

**Error Conditions**:
- Incompatible rules → PreprocessingException
- Data type mismatch → TypeException
- Memory exceeded → ResourceException

### Implementation Notes

- Preprocessing rules defined in Class Configuration
- Class-specific transforms (e.g., FEN parsing for Chess, image processing for Geography)
- Pipeline stages: validation → transformation → normalization

## Contract 4: Training Pipeline Interface

**Purpose**: How preprocessed data becomes a trained model

**Input**: Preprocessed data + training configuration
**Output**: Trained model artifact

### Interface Definition

```
train(preprocessed_data: PreprocessedData, config: TrainingConfig) → ModelArtifact
```

**Preconditions**:
- Data must be preprocessed successfully
- Training configuration must be valid
- Sufficient compute resources available

**Postconditions**:
- Model trained to convergence
- Metrics meet minimum thresholds
- Model artifact stored securely
- Training job logged with full details

**Error Conditions**:
- Training diverges → TrainingException
- Resource exhaustion → ResourceException
- Metric threshold not met → QualityException

### Implementation Notes

- Core training architecture unchanged (constitution requirement)
- Class-specific behavior through configuration only
- Support for resuming interrupted training

## Contract 5: Model Evaluation Interface

**Purpose**: How trained models are assessed

**Input**: Trained model + evaluation dataset
**Output**: Evaluation metrics

### Interface Definition

```
evaluate(model: ModelArtifact, eval_data: Dataset) → EvaluationResults
```

**Preconditions**:
- Model must be trained successfully
- Evaluation dataset must be available
- Evaluation metrics defined in class configuration

**Postconditions**:
- All required metrics computed
- Results stored with model artifact
- Performance meets minimum standards

**Error Conditions**:
- Model loading failure → ModelException
- Evaluation data unavailable → DataException
- Metric computation failure → EvaluationException

### Implementation Notes

- Domain-specific metrics for each class
- Chess: puzzle solution accuracy, rating prediction
- Geography: QA accuracy, geographic reasoning score
- Python: code correctness, exercise completion rate

## Contract 6: System Startup Interface

**Purpose**: How the system initializes with class configurations

**Input**: System configuration + available classes
**Output**: Initialized system ready for operation

### Interface Definition

```
initialize(system_config: SystemConfig, available_classes: List[string]) → SystemState
```

**Preconditions**:
- System configuration valid
- At least one class configuration available
- Dependencies installed

**Postconditions**:
- All class configurations loaded
- Datasets validated (not necessarily loaded)
- System ready for training or inference

**Error Conditions**:
- No valid classes → InitializationException
- Configuration errors → ConfigurationException

### Implementation Notes

- Lazy loading: datasets loaded on-demand, not at startup
- Configuration validation happens at startup
- System state persisted for quick restart

## Contract Versioning

All contracts follow semantic versioning:
- MAJOR: Breaking changes to interface
- MINOR: New optional parameters or return fields
- PATCH: Bug fixes, documentation updates

Current contract version: 1.0.0
