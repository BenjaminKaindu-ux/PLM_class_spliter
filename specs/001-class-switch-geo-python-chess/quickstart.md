# Quickstart Validation Guide: Class Switch to Geography, Python, Chess

**Branch**: `001-class-switch-geo-python-chess` | **Date**: 2026-09-07

## Overview

This guide provides validation scenarios to verify the class switch feature works end-to-end. Each scenario tests a specific aspect of the implementation.

## Prerequisites

- System installed and configured
- Network access to HuggingFace Hub (or cached datasets)
- Sufficient compute resources for model training
- Python environment with required dependencies

## Validation Scenario 1: Geography Class Configuration

**Objective**: Verify Geography class loads correctly

**Steps**:
1. Start the system
2. List available classes
3. Select Geography class
4. Verify configuration loads

**Expected Outcome**:
- Geography class appears in available classes
- Configuration loads without errors
- Datasets (GeoGPT-QA and geochain) are referenced correctly

**Validation Command**:
```bash
# Example validation (actual commands depend on implementation)
plm-cli class list
plm-cli class select geography
plm-cli config show geography
```

## Validation Scenario 2: Python Class Configuration

**Objective**: Verify Python class loads correctly

**Steps**:
1. Start the system
2. List available classes
3. Select Python class
4. Verify configuration loads

**Expected Outcome**:
- Python class appears in available classes
- Configuration loads without errors
- Dataset (CodeExercise-Python-27k) is referenced correctly

**Validation Command**:
```bash
plm-cli class list
plm-cli class select python
plm-cli config show python
```

## Validation Scenario 3: Chess Class Configuration

**Objective**: Verify Chess class loads correctly

**Steps**:
1. Start the system
2. List available classes
3. Select Chess class
4. Verify configuration loads

**Expected Outcome**:
- Chess class appears in available classes
- Configuration loads without errors
- Dataset (Lichess/chess-puzzles) is referenced correctly

**Validation Command**:
```bash
plm-cli class list
plm-cli class select chess
plm-cli config show chess
```

## Validation Scenario 4: Dataset Loading (Geography)

**Objective**: Verify Geography datasets load successfully

**Steps**:
1. Select Geography class
2. Initiate dataset loading
3. Verify datasets are accessible
4. Check data format compatibility

**Expected Outcome**:
- GeoGPT-QA dataset loads (41.4K QA pairs)
- Geochain dataset loads (1.4M rows)
- Data formats match expected schemas
- No loading errors

**Validation Command**:
```bash
plm-cli dataset load geography --validate
plm-cli dataset info geography
```

## Validation Scenario 5: Dataset Loading (Python)

**Objective**: Verify Python dataset loads successfully

**Steps**:
1. Select Python class
2. Initiate dataset loading
3. Verify dataset is accessible
4. Check data format compatibility

**Expected Outcome**:
- CodeExercise-Python-27k dataset loads (27K exercises)
- Data format matches expected schema
- No loading errors

**Validation Command**:
```bash
plm-cli dataset load python --validate
plm-cli dataset info python
```

## Validation Scenario 6: Dataset Loading (Chess)

**Objective**: Verify Chess dataset loads successfully

**Steps**:
1. Select Chess class
2. Initiate dataset loading
3. Verify dataset is accessible
4. Check data format compatibility

**Expected Outcome**:
- Lichess/chess-puzzles dataset loads (6.1M puzzles)
- Data format matches expected schema (FEN, Moves, Rating)
- No loading errors

**Validation Command**:
```bash
plm-cli dataset load chess --validate
plm-cli dataset info chess
```

## Validation Scenario 7: Class Switching

**Objective**: Verify system can switch between classes without restart

**Steps**:
1. Start system with Geography class
2. Switch to Python class
3. Switch to Chess class
4. Switch back to Geography class

**Expected Outcome**:
- All switches complete without restart
- Configuration reloads correctly for each class
- No state leakage between classes
- System remains stable throughout

**Validation Command**:
```bash
plm-cli class select geography
plm-cli class select python
plm-cli class select chess
plm-cli class select geography
plm-cli status
```

## Validation Scenario 8: Training Pipeline (Quick Test)

**Objective**: Verify training pipeline works with new classes

**Steps**:
1. Select a class (e.g., Python)
2. Load dataset
3. Run abbreviated training (small subset)
4. Verify model artifact created

**Expected Outcome**:
- Training starts without errors
- Model artifact generated
- Metrics computed and logged
- No core architecture modifications

**Validation Command**:
```bash
plm-cli class select python
plm-cli dataset load python --limit 1000
plm-cli train --quick-test
plm-cli model list
```

## Validation Scenario 9: Model Evaluation

**Objective**: Verify trained models can be evaluated

**Steps**:
1. Train a model (from Scenario 8)
2. Run evaluation with class-specific metrics
3. Verify metrics are computed correctly

**Expected Outcome**:
- Evaluation completes successfully
- Domain-appropriate metrics reported
- Results stored with model artifact

**Validation Command**:
```bash
plm-cli model evaluate <model-id>
plm-cli metrics show <model-id>
```

## Validation Scenario 10: Regression Testing

**Objective**: Verify core architecture unchanged

**Steps**:
1. Run existing test suite (if available)
2. Verify all tests pass
3. Check for any architectural changes

**Expected Outcome**:
- All existing tests pass
- No modifications to core training logic
- Class-specific behavior through configuration only

**Validation Command**:
```bash
# If test suite exists
python -m pytest tests/
# Check for core architecture changes
git diff src/core/
```

## Success Criteria Checklist

- [ ] All three classes load correctly
- [ ] All datasets load successfully
- [ ] Class switching works without restart
- [ ] Training pipeline produces models for each class
- [ ] Model evaluation works with domain-specific metrics
- [ ] No regression in core architecture
- [ ] Constitution requirements satisfied

## Troubleshooting

### Common Issues

1. **Dataset loading fails**
   - Check network connectivity
   - Verify HuggingFace Hub access
   - Check dataset cache

2. **Configuration not found**
   - Verify class_id matches configuration filename
   - Check configuration file syntax
   - Ensure configuration directory is in path

3. **Training fails**
   - Check compute resources
   - Verify dataset is loaded
   - Check preprocessing rules

4. **Class switching fails**
   - Ensure no training jobs are running
   - Check system state
   - Restart system if needed

## Next Steps

After completing all validation scenarios:
1. Document any issues found
2. Create detailed tasks for implementation
3. Begin development following the plan
