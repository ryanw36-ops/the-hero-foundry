import React from 'react';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  LinearProgress,
  Typography,
  Card,
  CardContent,
  Chip,
  IconButton,
  Tooltip,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  NavigateBefore as PreviousIcon,
  NavigateNext as NextIcon,
  Check as CheckIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Save as SaveIcon,
  Refresh as ResetIcon
} from '@mui/icons-material';
import { useCharacterWizard, WizardStep, WIZARD_STEPS } from './WizardProvider';
import { useLogger } from '../../hooks/useLogger';

const WizardNavigation: React.FC = () => {
  const {
    state,
    goToStep,
    nextStep,
    previousStep,
    canGoNext,
    canGoPrevious,
    getStepProgress,
    getStepTitle,
    getStepDescription,
    isStepVisited,
    saveCharacter,
    resetWizard,
    validateCurrentStep
  } = useCharacterWizard();
  
  const logger = useLogger();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleStepClick = (step: WizardStep) => {
    if (isStepVisited(step) || step === state.currentStep) {
      goToStep(step);
    }
  };

  const handleNext = async () => {
    // Validate current step before proceeding
    const validation = await validateCurrentStep();
    if (validation.isValid) {
      nextStep();
    } else {
      logger.warn('Cannot proceed: current step has validation errors', 'WizardNavigation', {
        step: state.currentStep,
        errors: validation.errors.length
      });
    }
  };

  const handlePrevious = () => {
    previousStep();
  };

  const handleSave = async () => {
    const success = await saveCharacter();
    if (success) {
      logger.info('Character saved from wizard navigation', 'WizardNavigation');
    }
  };

  const handleReset = () => {
    if (confirm('Are you sure you want to reset the wizard? All progress will be lost.')) {
      resetWizard();
      logger.info('Wizard reset by user', 'WizardNavigation');
    }
  };

  const getStepIcon = (step: WizardStep) => {
    const validation = state.characterData.stepValidation[step];
    const isVisited = isStepVisited(step);
    const isCurrent = step === state.currentStep;

    if (validation) {
      if (validation.isValid) {
        return <CheckIcon color="success" />;
      } else if (validation.errors.length > 0) {
        return <ErrorIcon color="error" />;
      } else if (validation.warnings.length > 0) {
        return <WarningIcon color="warning" />;
      }
    }

    if (isCurrent) {
      return WIZARD_STEPS.indexOf(step) + 1;
    }

    if (isVisited) {
      return WIZARD_STEPS.indexOf(step) + 1;
    }

    return WIZARD_STEPS.indexOf(step) + 1;
  };

  const getStepStatus = (step: WizardStep) => {
    const validation = state.characterData.stepValidation[step];
    const isVisited = isStepVisited(step);
    const isCurrent = step === state.currentStep;

    if (isCurrent) return 'current';
    if (validation?.isValid) return 'completed';
    if (validation && validation.errors.length > 0) return 'error';
    if (validation && validation.warnings.length > 0) return 'warning';
    if (isVisited) return 'visited';
    return 'pending';
  };

  if (isMobile) {
    // Mobile layout - compact stepper
    return (
      <Box>
        {/* Progress bar */}
        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Step {WIZARD_STEPS.indexOf(state.currentStep) + 1} of {WIZARD_STEPS.length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {Math.round(getStepProgress())}%
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={getStepProgress()}
            sx={{ height: 8, borderRadius: 4 }}
          />
        </Box>

        {/* Current step info */}
        <Card sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {getStepTitle(state.currentStep)}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {getStepDescription(state.currentStep)}
            </Typography>
            
            {/* Step status */}
            <Box sx={{ mt: 2 }}>
              <Chip
                label={getStepStatus(state.currentStep)}
                color={
                  getStepStatus(state.currentStep) === 'completed' ? 'success' :
                  getStepStatus(state.currentStep) === 'error' ? 'error' :
                  getStepStatus(state.currentStep) === 'warning' ? 'warning' :
                  'primary'
                }
                size="small"
              />
            </Box>
          </CardContent>
        </Card>

        {/* Navigation buttons */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Button
            variant="outlined"
            startIcon={<PreviousIcon />}
            onClick={handlePrevious}
            disabled={!canGoPrevious()}
          >
            Previous
          </Button>

          <Box sx={{ display: 'flex', gap: 1 }}>
            <Tooltip title="Save progress">
              <IconButton onClick={handleSave} color="primary">
                <SaveIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Reset wizard">
              <IconButton onClick={handleReset} color="warning">
                <ResetIcon />
              </IconButton>
            </Tooltip>
          </Box>

          <Button
            variant="contained"
            endIcon={<NextIcon />}
            onClick={handleNext}
            disabled={!canGoNext()}
          >
            {state.currentStep === WizardStep.REVIEW ? 'Finish' : 'Next'}
          </Button>
        </Box>
      </Box>
    );
  }

  // Desktop layout - full stepper
  return (
    <Box>
      {/* Progress bar */}
      <Box sx={{ mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="h6">
            Character Creation Wizard
          </Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="outlined"
              startIcon={<SaveIcon />}
              onClick={handleSave}
              disabled={state.hasUnsavedChanges === false}
            >
              Save Progress
            </Button>
            <Button
              variant="outlined"
              startIcon={<ResetIcon />}
              onClick={handleReset}
              color="warning"
            >
              Reset
            </Button>
          </Box>
        </Box>
        <LinearProgress
          variant="determinate"
          value={getStepProgress()}
          sx={{ height: 6, borderRadius: 3 }}
        />
        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
          Progress: {Math.round(getStepProgress())}% ({WIZARD_STEPS.indexOf(state.currentStep) + 1}/{WIZARD_STEPS.length})
        </Typography>
      </Box>

      {/* Step navigation */}
      <Stepper
        activeStep={WIZARD_STEPS.indexOf(state.currentStep)}
        orientation="horizontal"
        sx={{ mb: 3 }}
      >
        {WIZARD_STEPS.map((step) => {
          const stepStatus = getStepStatus(step);
          const isClickable = isStepVisited(step) || step === state.currentStep;
          
          return (
            <Step key={step} completed={stepStatus === 'completed'}>
              <StepLabel
                icon={getStepIcon(step)}
                onClick={() => isClickable && handleStepClick(step)}
                sx={{
                  cursor: isClickable ? 'pointer' : 'default',
                  '& .MuiStepLabel-iconContainer': {
                    color: 
                      stepStatus === 'completed' ? theme.palette.success.main :
                      stepStatus === 'error' ? theme.palette.error.main :
                      stepStatus === 'warning' ? theme.palette.warning.main :
                      stepStatus === 'current' ? theme.palette.primary.main :
                      theme.palette.grey[400]
                  }
                }}
                error={stepStatus === 'error'}
              >
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: step === state.currentStep ? 'bold' : 'normal' }}>
                    {getStepTitle(step)}
                  </Typography>
                  {step === state.currentStep && (
                    <Typography variant="caption" color="text.secondary">
                      {getStepDescription(step)}
                    </Typography>
                  )}
                </Box>
              </StepLabel>
            </Step>
          );
        })}
      </Stepper>

      {/* Current step details */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <Box>
              <Typography variant="h5" gutterBottom>
                {getStepTitle(state.currentStep)}
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                {getStepDescription(state.currentStep)}
              </Typography>
            </Box>
            <Chip
              label={getStepStatus(state.currentStep)}
              color={
                getStepStatus(state.currentStep) === 'completed' ? 'success' :
                getStepStatus(state.currentStep) === 'error' ? 'error' :
                getStepStatus(state.currentStep) === 'warning' ? 'warning' :
                'primary'
              }
            />
          </Box>

          {/* Show validation errors/warnings if any */}
          {state.characterData.stepValidation[state.currentStep] && (
            <Box sx={{ mt: 2 }}>
              {state.characterData.stepValidation[state.currentStep]!.errors.length > 0 && (
                <Box sx={{ mb: 1 }}>
                  <Typography variant="body2" color="error" sx={{ fontWeight: 'bold' }}>
                    Errors:
                  </Typography>
                  {state.characterData.stepValidation[state.currentStep]!.errors.map((error, index) => (
                    <Typography key={index} variant="body2" color="error" sx={{ ml: 2 }}>
                      • {error.message}
                    </Typography>
                  ))}
                </Box>
              )}
              {state.characterData.stepValidation[state.currentStep]!.warnings.length > 0 && (
                <Box>
                  <Typography variant="body2" color="warning.main" sx={{ fontWeight: 'bold' }}>
                    Warnings:
                  </Typography>
                  {state.characterData.stepValidation[state.currentStep]!.warnings.map((warning, index) => (
                    <Typography key={index} variant="body2" color="warning.main" sx={{ ml: 2 }}>
                      • {warning.message}
                    </Typography>
                  ))}
                </Box>
              )}
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Navigation buttons */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Button
          variant="outlined"
          startIcon={<PreviousIcon />}
          onClick={handlePrevious}
          disabled={!canGoPrevious()}
          size="large"
        >
          Previous Step
        </Button>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {state.hasUnsavedChanges && (
            <Chip
              label="Unsaved changes"
              color="warning"
              size="small"
            />
          )}
          <Typography variant="body2" color="text.secondary">
            Step {WIZARD_STEPS.indexOf(state.currentStep) + 1} of {WIZARD_STEPS.length}
          </Typography>
        </Box>

        <Button
          variant="contained"
          endIcon={<NextIcon />}
          onClick={handleNext}
          disabled={!canGoNext()}
          size="large"
        >
          {state.currentStep === WizardStep.REVIEW ? 'Finish Character' : 'Next Step'}
        </Button>
      </Box>
    </Box>
  );
};

export default WizardNavigation;
