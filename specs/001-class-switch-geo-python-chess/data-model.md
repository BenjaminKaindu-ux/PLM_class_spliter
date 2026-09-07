# Data Model: Class Switch to Geography, Python, Chess

**Branch**: `001-class-switch-geo-python-chess` | **Date**: 2026-09-07

## Entity Definitions

### Class Configuration

**Purpose**: Defines how the system operates for a specific domain class

| Field | Type | Description | Validation Rules |
|-------|------|-------------|------------------|
| class_id | String | Unique identifier (e.g., "geography", "python", "chess") | Required, lowercase, no spaces |
| class_name | String | Human-readable name | Required |
| datasets | List | Dataset sources for this class | At least one dataset required |
| preprocessing | Object | Class-specific preprocessing rules | Must define transforms |
| evaluation_metrics | List | Metrics for model quality assessment | At least one metric required |
| output_format | String | Format for model outputs | Must be valid format type |

**State Transitions**: None (configuration is static)

### Dataset Reference

**Purpose**: Points to a specific dataset on HuggingFace Hub

| Field | Type | Description | Validation Rules |
|-------|------|-------------|------------------|
| dataset_id | String | HuggingFace dataset identifier | Required, format: "org/dataset-name" |
| dataset_type | Enum | Type of data (parquet, csv, json, image) | Required |
| split | String | Dataset split to use (train, test, validation) | Default: "train" |
| config | String | Dataset configuration name | Optional |
| limit | Integer | Maximum rows to load | Optional, must be positive |

**Relationships**: Belongs to one Class Configuration

### Training Job

**Purpose**: Represents a single training run for a class

| Field | Type | Description | Validation Rules |
|-------|------|-------------|------------------|
| job_id | String | Unique identifier for this run | Required, auto-generated |
| class_id | String | Which class this job trains | Required, must exist in Class Configuration |
| dataset_versions | Object | Versions of datasets used | Required |
| status | Enum | Current status (pending, running, completed, failed) | Required |
| started_at | Timestamp | When training began | Required when status != pending |
| completed_at | Timestamp | When training finished | Required when status = completed |
| metrics | Object | Training results | Required when status = completed |

**State Transitions**: pending → running → completed | failed

### Model Artifact

**Purpose**: Stores trained model information

| Field | Type | Description | Validation Rules |
|-------|------|-------------|------------------|
| model_id | String | Unique model identifier | Required |
| class_id | String | Which class this model was trained on | Required |
| version | String | Semantic version (e.g., "1.0.0") | Required, must follow semver |
| training_job_id | String | Reference to training job | Required |
| artifact_path | String | Path to model files | Required |
| created_at | Timestamp | When model was created | Required |
| metrics | Object | Model performance metrics | Required |

**Relationships**: Created from one Training Job, belongs to one Class Configuration

## Entity Relationships

```
Class Configuration (1) ←→ (Many) Dataset Reference
Class Configuration (1) ←→ (Many) Training Job
Training Job (1) ←→ (One) Model Artifact
```

## Validation Rules

### Class Configuration Validation
- class_id must be unique across all configurations
- datasets list must reference valid Dataset Reference objects
- preprocessing rules must be compatible with dataset types
- evaluation_metrics must be applicable to the domain

### Dataset Reference Validation
- dataset_id must be accessible on HuggingFace Hub
- dataset_type must match actual file format
- config must exist within the dataset if specified
- limit must not exceed dataset size

### Training Job Validation
- class_id must reference existing Class Configuration
- dataset_versions must match current dataset states
- status transitions must follow defined flow
- metrics must include all required evaluation metrics for the class

### Model Artifact Validation
- version must be greater than previous version for same class
- training_job_id must reference completed job
- artifact_path must point to valid model files
- metrics must meet minimum thresholds for the class

## Data Flow

1. **Configuration Loading**: System loads Class Configuration for target class
2. **Dataset Resolution**: Dataset References are resolved to actual HuggingFace datasets
3. **Training Execution**: Training Job processes datasets according to configuration
4. **Model Storage**: Completed training produces Model Artifact
5. **Inference**: Model Artifact is used for predictions in its domain
