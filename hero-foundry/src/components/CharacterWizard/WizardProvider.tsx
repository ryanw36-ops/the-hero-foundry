import React, { createContext, useContext, useReducer, useCallback } from 'react';
import { useLogger } from '../../hooks/useLogger';
import type { ValidationResult } from '../../services/validationService';

// Wizard step definitions
export const WizardStep = {
  OVERVIEW: 'overview',
  RACE: 'race',
  CLASS: 'class',
  BACKGROUND: 'background',
  ABILITY_SCORES: 'ability-scores',
  SKILLS: 'skills',
  EQUIPMENT: 'equipment',
  SPELLS: 'spells',
  DETAILS: 'details',
  REVIEW: 'review'
} as const;

export type WizardStep = typeof WizardStep[keyof typeof WizardStep];

export const WIZARD_STEPS: WizardStep[] = [
  WizardStep.OVERVIEW,
  WizardStep.RACE,
  WizardStep.CLASS,
  WizardStep.BACKGROUND,
  WizardStep.ABILITY_SCORES,
  WizardStep.SKILLS,
  WizardStep.EQUIPMENT,
  WizardStep.SPELLS,
  WizardStep.DETAILS,
  WizardStep.REVIEW
];

export const STEP_TITLES: Record<WizardStep, string> = {
  [WizardStep.OVERVIEW]: 'Character Overview',
  [WizardStep.RACE]: 'Choose Race',
  [WizardStep.CLASS]: 'Choose Class',
  [WizardStep.BACKGROUND]: 'Choose Background',
  [WizardStep.ABILITY_SCORES]: 'Ability Scores',
  [WizardStep.SKILLS]: 'Skills & Proficiencies',
  [WizardStep.EQUIPMENT]: 'Starting Equipment',
  [WizardStep.SPELLS]: 'Spells & Cantrips',
  [WizardStep.DETAILS]: 'Character Details',
  [WizardStep.REVIEW]: 'Review & Finish'
};

export const STEP_DESCRIPTIONS: Record<WizardStep, string> = {
  [WizardStep.OVERVIEW]: 'Start by giving your character a name and choosing their level',
  [WizardStep.RACE]: 'Select your character\'s race and apply racial bonuses',
  [WizardStep.CLASS]: 'Choose your character\'s class and starting features',
  [WizardStep.BACKGROUND]: 'Pick a background for additional skills and personality',
  [WizardStep.ABILITY_SCORES]: 'Generate and assign your six ability scores',
  [WizardStep.SKILLS]: 'Choose skill proficiencies and expertise',
  [WizardStep.EQUIPMENT]: 'Select starting equipment and gear',
  [WizardStep.SPELLS]: 'Choose starting spells and cantrips (if applicable)',
  [WizardStep.DETAILS]: 'Add personality, appearance, and backstory details',
  [WizardStep.REVIEW]: 'Review your character and make final adjustments'
};

// Character data interfaces
export interface CharacterRace {
  id: string;
  name: string;
  abilityScoreIncrease: Record<string, number>;
  size: string;
  speed: number;
  traits: string[];
  languages: string[];
  proficiencies: string[];
}

export interface CharacterClass {
  id: string;
  name: string;
  hitDie: number;
  primaryAbility: string[];
  savingThrows: string[];
  skillChoices: number;
  availableSkills: string[];
  startingProficiencies: string[];
  startingEquipment: string[];
  features: Record<number, string[]>;
}

export interface CharacterBackground {
  id: string;
  name: string;
  skillProficiencies: string[];
  languageChoices: number;
  toolProficiencies: string[];
  startingEquipment: string[];
  feature: string;
  personalityTraits: string[];
  ideals: string[];
  bonds: string[];
  flaws: string[];
}

export interface AbilityScores {
  strength: number;
  dexterity: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
}

export interface WizardCharacterData {
  // Overview
  id: string;
  name: string;
  level: number;
  
  // Core choices
  race: CharacterRace | null;
  class: CharacterClass | null;
  background: CharacterBackground | null;
  
  // Ability scores
  abilityScores: AbilityScores;
  abilityScoreMethod: string;
  
  // Skills and proficiencies
  skillProficiencies: string[];
  skillExpertise: string[];
  languageProficiencies: string[];
  toolProficiencies: string[];
  otherProficiencies: string[];
  
  // Equipment
  equipment: Array<{
    name: string;
    quantity: number;
    weight?: number;
    description?: string;
    equipped?: boolean;
  }>;
  
  // Spells (if applicable)
  spells: Array<{
    name: string;
    level: number;
    school: string;
    prepared: boolean;
  }>;
  cantrips: string[];
  
  // Character details
  personalityTraits: string[];
  ideals: string[];
  bonds: string[];
  flaws: string[];
  appearance: string;
  backstory: string;
  
  // System data
  hitPoints: {
    current: number;
    maximum: number;
    temporary: number;
  };
  armorClass: number;
  initiative: number;
  speed: number;
  
  // Metadata
  created: string;
  modified: string;
  
  // Validation
  stepValidation: Record<WizardStep, ValidationResult | null>;
  isComplete: boolean;
}

// Wizard state
interface WizardState {
  currentStep: WizardStep;
  characterData: WizardCharacterData;
  stepHistory: WizardStep[];
  isNavigating: boolean;
  hasUnsavedChanges: boolean;
  ruleset: string;
}

// Wizard actions
type WizardAction =
  | { type: 'SET_STEP'; payload: WizardStep }
  | { type: 'NEXT_STEP' }
  | { type: 'PREVIOUS_STEP' }
  | { type: 'JUMP_TO_STEP'; payload: WizardStep }
  | { type: 'UPDATE_CHARACTER_DATA'; payload: Partial<WizardCharacterData> }
  | { type: 'VALIDATE_STEP'; payload: { step: WizardStep; result: ValidationResult } }
  | { type: 'RESET_WIZARD' }
  | { type: 'LOAD_CHARACTER'; payload: WizardCharacterData }
  | { type: 'SET_RULESET'; payload: string }
  | { type: 'MARK_SAVED' }
  | { type: 'MARK_UNSAVED' };

// Initial character data
const createInitialCharacterData = (): WizardCharacterData => ({
  id: `char-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
  name: '',
  level: 1,
  race: null,
  class: null,
  background: null,
  abilityScores: {
    strength: 10,
    dexterity: 10,
    constitution: 10,
    intelligence: 10,
    wisdom: 10,
    charisma: 10
  },
  abilityScoreMethod: 'point-buy',
  skillProficiencies: [],
  skillExpertise: [],
  languageProficiencies: [],
  toolProficiencies: [],
  otherProficiencies: [],
  equipment: [],
  spells: [],
  cantrips: [],
  personalityTraits: [],
  ideals: [],
  bonds: [],
  flaws: [],
  appearance: '',
  backstory: '',
  hitPoints: {
    current: 0,
    maximum: 0,
    temporary: 0
  },
  armorClass: 10,
  initiative: 0,
  speed: 30,
  created: new Date().toISOString(),
  modified: new Date().toISOString(),
  stepValidation: Object.fromEntries(
    WIZARD_STEPS.map(step => [step, null])
  ) as Record<WizardStep, ValidationResult | null>,
  isComplete: false
});

// Initial state
const initialState: WizardState = {
  currentStep: WizardStep.OVERVIEW,
  characterData: createInitialCharacterData(),
  stepHistory: [WizardStep.OVERVIEW],
  isNavigating: false,
  hasUnsavedChanges: false,
  ruleset: 'dnd5e'
};

// Wizard reducer
const wizardReducer = (state: WizardState, action: WizardAction): WizardState => {
  switch (action.type) {
    case 'SET_STEP':
      return {
        ...state,
        currentStep: action.payload,
        stepHistory: state.stepHistory.includes(action.payload)
          ? state.stepHistory
          : [...state.stepHistory, action.payload]
      };

    case 'NEXT_STEP': {
      const currentIndex = WIZARD_STEPS.indexOf(state.currentStep);
      const nextStep = WIZARD_STEPS[currentIndex + 1];
      if (nextStep) {
        return {
          ...state,
          currentStep: nextStep,
          stepHistory: state.stepHistory.includes(nextStep)
            ? state.stepHistory
            : [...state.stepHistory, nextStep]
        };
      }
      return state;
    }

    case 'PREVIOUS_STEP': {
      const currentIndex = WIZARD_STEPS.indexOf(state.currentStep);
      const previousStep = WIZARD_STEPS[currentIndex - 1];
      if (previousStep) {
        return {
          ...state,
          currentStep: previousStep
        };
      }
      return state;
    }

    case 'JUMP_TO_STEP':
      return {
        ...state,
        currentStep: action.payload,
        stepHistory: state.stepHistory.includes(action.payload)
          ? state.stepHistory
          : [...state.stepHistory, action.payload]
      };

    case 'UPDATE_CHARACTER_DATA':
      return {
        ...state,
        characterData: {
          ...state.characterData,
          ...action.payload,
          modified: new Date().toISOString()
        },
        hasUnsavedChanges: true
      };

    case 'VALIDATE_STEP':
      return {
        ...state,
        characterData: {
          ...state.characterData,
          stepValidation: {
            ...state.characterData.stepValidation,
            [action.payload.step]: action.payload.result
          }
        }
      };

    case 'RESET_WIZARD':
      return {
        ...initialState,
        ruleset: state.ruleset
      };

    case 'LOAD_CHARACTER':
      return {
        ...state,
        characterData: action.payload,
        hasUnsavedChanges: false
      };

    case 'SET_RULESET':
      return {
        ...state,
        ruleset: action.payload
      };

    case 'MARK_SAVED':
      return {
        ...state,
        hasUnsavedChanges: false
      };

    case 'MARK_UNSAVED':
      return {
        ...state,
        hasUnsavedChanges: true
      };

    default:
      return state;
  }
};

// Context
interface WizardContextValue {
  // State
  state: WizardState;
  
  // Navigation
  goToStep: (step: WizardStep) => void;
  nextStep: () => void;
  previousStep: () => void;
  canGoNext: () => boolean;
  canGoPrevious: () => boolean;
  getStepProgress: () => number;
  
  // Character data
  updateCharacterData: (data: Partial<WizardCharacterData>) => void;
  validateCurrentStep: () => Promise<ValidationResult>;
  validateStep: (step: WizardStep) => Promise<ValidationResult>;
  isStepValid: (step: WizardStep) => boolean;
  isStepVisited: (step: WizardStep) => boolean;
  
  // Persistence
  saveCharacter: () => Promise<boolean>;
  loadCharacter: (characterData: WizardCharacterData) => void;
  resetWizard: () => void;
  
  // Utility
  getStepTitle: (step: WizardStep) => string;
  getStepDescription: (step: WizardStep) => string;
  setRuleset: (ruleset: string) => void;
}

const WizardContext = createContext<WizardContextValue | null>(null);

// Provider component
export const WizardProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(wizardReducer, initialState);
  const logger = useLogger();

  // Navigation functions
  const goToStep = useCallback((step: WizardStep) => {
    logger.info(`Navigating to wizard step: ${step}`, 'WizardProvider', { step });
    dispatch({ type: 'JUMP_TO_STEP', payload: step });
  }, [logger]);

  const nextStep = useCallback(() => {
    const currentIndex = WIZARD_STEPS.indexOf(state.currentStep);
    const nextStep = WIZARD_STEPS[currentIndex + 1];
    if (nextStep) {
      logger.info(`Moving to next wizard step: ${nextStep}`, 'WizardProvider', { 
        from: state.currentStep, 
        to: nextStep 
      });
      dispatch({ type: 'NEXT_STEP' });
    }
  }, [state.currentStep, logger]);

  const previousStep = useCallback(() => {
    const currentIndex = WIZARD_STEPS.indexOf(state.currentStep);
    const prevStep = WIZARD_STEPS[currentIndex - 1];
    if (prevStep) {
      logger.info(`Moving to previous wizard step: ${prevStep}`, 'WizardProvider', { 
        from: state.currentStep, 
        to: prevStep 
      });
      dispatch({ type: 'PREVIOUS_STEP' });
    }
  }, [state.currentStep, logger]);

  const canGoNext = useCallback(() => {
    const currentIndex = WIZARD_STEPS.indexOf(state.currentStep);
    return currentIndex < WIZARD_STEPS.length - 1;
  }, [state.currentStep]);

  const canGoPrevious = useCallback(() => {
    const currentIndex = WIZARD_STEPS.indexOf(state.currentStep);
    return currentIndex > 0;
  }, [state.currentStep]);

  const getStepProgress = useCallback(() => {
    const currentIndex = WIZARD_STEPS.indexOf(state.currentStep);
    return ((currentIndex + 1) / WIZARD_STEPS.length) * 100;
  }, [state.currentStep]);

  // Character data functions
  const updateCharacterData = useCallback((data: Partial<WizardCharacterData>) => {
    logger.debug('Updating character data', 'WizardProvider', { updates: Object.keys(data) });
    dispatch({ type: 'UPDATE_CHARACTER_DATA', payload: data });
  }, [logger]);

  const validateCurrentStep = useCallback(async (): Promise<ValidationResult> => {
    return validateStep(state.currentStep);
  }, [state.currentStep]);

  const validateStep = useCallback(async (step: WizardStep): Promise<ValidationResult> => {
    logger.info(`Validating wizard step: ${step}`, 'WizardProvider', { step });
    
    // For now, use a simple validation - in the future this would use specific step schemas
    const result: ValidationResult = {
      isValid: true,
      errors: [],
      warnings: []
    };
    
    // Basic validation rules
    if (step === WizardStep.OVERVIEW) {
      if (!state.characterData.name.trim()) {
        result.isValid = false;
        result.errors.push({
          path: 'name',
          message: 'Character name is required',
          code: 'REQUIRED_FIELD'
        });
      }
      if (state.characterData.level < 1 || state.characterData.level > 20) {
        result.isValid = false;
        result.errors.push({
          path: 'level',
          message: 'Character level must be between 1 and 20',
          code: 'INVALID_RANGE'
        });
      }
    }
    
    dispatch({ type: 'VALIDATE_STEP', payload: { step, result } });
    return result;
  }, [state.characterData, logger]);

  const isStepValid = useCallback((step: WizardStep): boolean => {
    const validation = state.characterData.stepValidation[step];
    return validation ? validation.isValid : false;
  }, [state.characterData.stepValidation]);

  const isStepVisited = useCallback((step: WizardStep): boolean => {
    return state.stepHistory.includes(step);
  }, [state.stepHistory]);

  // Persistence functions
  const saveCharacter = useCallback(async (): Promise<boolean> => {
    try {
      logger.info('Saving character data', 'WizardProvider', { 
        characterId: state.characterData.id,
        characterName: state.characterData.name
      });
      
      // Here you would integrate with your file storage service
      // For now, just simulate a save
      await new Promise(resolve => setTimeout(resolve, 500));
      
      dispatch({ type: 'MARK_SAVED' });
      logger.info('Character saved successfully', 'WizardProvider');
      return true;
    } catch (error) {
      logger.error('Failed to save character', 'WizardProvider', { error });
      return false;
    }
  }, [state.characterData, logger]);

  const loadCharacter = useCallback((characterData: WizardCharacterData) => {
    logger.info('Loading character data', 'WizardProvider', { 
      characterId: characterData.id,
      characterName: characterData.name
    });
    dispatch({ type: 'LOAD_CHARACTER', payload: characterData });
  }, [logger]);

  const resetWizard = useCallback(() => {
    logger.info('Resetting wizard', 'WizardProvider');
    dispatch({ type: 'RESET_WIZARD' });
  }, [logger]);

  // Utility functions
  const getStepTitle = useCallback((step: WizardStep) => STEP_TITLES[step], []);
  const getStepDescription = useCallback((step: WizardStep) => STEP_DESCRIPTIONS[step], []);
  
  const setRuleset = useCallback((ruleset: string) => {
    logger.info(`Setting wizard ruleset: ${ruleset}`, 'WizardProvider', { ruleset });
    dispatch({ type: 'SET_RULESET', payload: ruleset });
  }, [logger]);

  const contextValue: WizardContextValue = {
    state,
    goToStep,
    nextStep,
    previousStep,
    canGoNext,
    canGoPrevious,
    getStepProgress,
    updateCharacterData,
    validateCurrentStep,
    validateStep,
    isStepValid,
    isStepVisited,
    saveCharacter,
    loadCharacter,
    resetWizard,
    getStepTitle,
    getStepDescription,
    setRuleset
  };

  return (
    <WizardContext.Provider value={contextValue}>
      {children}
    </WizardContext.Provider>
  );
};

// Hook for using wizard context
export const useCharacterWizard = (): WizardContextValue => {
  const context = useContext(WizardContext);
  if (!context) {
    throw new Error('useCharacterWizard must be used within a WizardProvider');
  }
  return context;
};
