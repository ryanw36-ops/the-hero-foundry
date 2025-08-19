import React from 'react';
import { Box, Container, Paper } from '@mui/material';
import { WizardProvider, WizardStep, useCharacterWizard } from './WizardProvider';
import WizardNavigation from './WizardNavigation';
import OverviewStep from './steps/OverviewStep';
import RaceStep from './steps/RaceStep';
import ClassStep from './steps/ClassStep';
import BackgroundStep from './steps/BackgroundStep';
import AbilityScoresStep from './steps/AbilityScoresStep';
import SkillsStep from './steps/SkillsStep';
import EquipmentStep from './steps/EquipmentStep';
import SpellsStep from './steps/SpellsStep';
import DetailsStep from './steps/DetailsStep';
import ReviewStep from './steps/ReviewStep';

// Step component renderer
const WizardStepRenderer: React.FC = () => {
  const { state } = useCharacterWizard();

  const renderCurrentStep = () => {
    switch (state.currentStep) {
      case WizardStep.OVERVIEW:
        return <OverviewStep />;
      case WizardStep.RACE:
        return <RaceStep />;
      case WizardStep.CLASS:
        return <ClassStep />;
      case WizardStep.BACKGROUND:
        return <BackgroundStep />;
      case WizardStep.ABILITY_SCORES:
        return <AbilityScoresStep />;
      case WizardStep.SKILLS:
        return <SkillsStep />;
      case WizardStep.EQUIPMENT:
        return <EquipmentStep />;
      case WizardStep.SPELLS:
        return <SpellsStep />;
      case WizardStep.DETAILS:
        return <DetailsStep />;
      case WizardStep.REVIEW:
        return <ReviewStep />;
      default:
        return <OverviewStep />;
    }
  };

  return (
    <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      {renderCurrentStep()}
    </Box>
  );
};

// Main wizard content (wrapped by provider)
const WizardContent: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 3 }}>
      <Paper elevation={1} sx={{ p: 3, minHeight: 'calc(100vh - 200px)' }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          {/* Navigation header */}
          <WizardNavigation />
          
          {/* Current step content */}
          <Box sx={{ flex: 1, mt: 3 }}>
            <WizardStepRenderer />
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

// Main wizard component with provider
const CharacterWizard: React.FC = () => {
  return (
    <WizardProvider>
      <WizardContent />
    </WizardProvider>
  );
};

export default CharacterWizard;
