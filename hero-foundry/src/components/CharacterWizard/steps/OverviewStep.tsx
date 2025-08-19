import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  TextField,
  FormControl,
  Card,
  CardContent,
  Chip,
  Alert,
  Slider,
  FormHelperText
} from '@mui/material';
import {
  Person as PersonIcon,
  Star as StarIcon
} from '@mui/icons-material';
import { useCharacterWizard } from '../WizardProvider';
import { useLogger } from '../../../hooks/useLogger';

const OverviewStep: React.FC = () => {
  const { state, updateCharacterData } = useCharacterWizard();
  const logger = useLogger();
  
  const [localName, setLocalName] = useState(state.characterData.name || '');
  const [localLevel, setLocalLevel] = useState(state.characterData.level || 1);
  const [nameError, setNameError] = useState('');
  const [levelError, setLevelError] = useState('');

  useEffect(() => {
    logger.info('Overview step loaded', 'OverviewStep');
  }, [logger]);

  useEffect(() => {
    // Validate inputs when they change
    validateInputs();
  }, [localName, localLevel]);

  const validateInputs = () => {
    let hasError = false;

    // Validate name
    if (!localName.trim()) {
      setNameError('Character name is required');
      hasError = true;
    } else if (localName.length < 2) {
      setNameError('Character name must be at least 2 characters');
      hasError = true;
    } else if (localName.length > 50) {
      setNameError('Character name must be less than 50 characters');
      hasError = true;
    } else {
      setNameError('');
    }

    // Validate level
    if (localLevel < 1 || localLevel > 20) {
      setLevelError('Character level must be between 1 and 20');
      hasError = true;
    } else {
      setLevelError('');
    }

    return !hasError;
  };

  const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newName = event.target.value;
    setLocalName(newName);
    
    // Update character data immediately for valid names
    if (newName.trim() && newName.length >= 2 && newName.length <= 50) {
      updateCharacterData({ name: newName });
      logger.debug('Character name updated', 'OverviewStep', { name: newName });
    }
  };

  const handleLevelChange = (_event: Event, newValue: number | number[]) => {
    const level = Array.isArray(newValue) ? newValue[0] : newValue;
    setLocalLevel(level);
    updateCharacterData({ level });
    logger.debug('Character level updated', 'OverviewStep', { level });
  };

  const handleNameBlur = () => {
    // Final validation and update on blur
    if (localName.trim() && !nameError) {
      updateCharacterData({ name: localName.trim() });
    }
  };

  const getLevelDescription = (level: number): string => {
    if (level === 1) return 'Starting character - new to adventure';
    if (level <= 4) return 'Local hero - gaining experience';
    if (level <= 10) return 'Regional champion - well-known adventurer';
    if (level <= 16) return 'Master adventurer - legendary deeds';
    return 'Epic hero - shaper of worlds';
  };

  const getLevelFeatures = (level: number): string[] => {
    const features = [];
    
    if (level >= 1) features.push('Basic class features');
    if (level >= 2) features.push('Additional class abilities');
    if (level >= 3) features.push('Subclass choice');
    if (level >= 4) features.push('Ability Score Improvement');
    if (level >= 5) features.push('Proficiency bonus increases');
    if (level >= 6) features.push('Enhanced class features');
    if (level >= 8) features.push('Another Ability Score Improvement');
    if (level >= 10) features.push('Major class milestones');
    if (level >= 11) features.push('Powerful abilities unlock');
    if (level >= 12) features.push('Third Ability Score Improvement');
    if (level >= 15) features.push('High-level features');
    if (level >= 17) features.push('Near-legendary abilities');
    if (level >= 20) features.push('Capstone abilities');
    
    return features.slice(0, Math.min(4, Math.floor(level / 2) + 1));
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <PersonIcon color="primary" />
          Character Overview
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Let's start with the basics. Give your character a name and choose their starting level.
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
        {/* Character Name */}
        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Character Name
              </Typography>
              <TextField
                fullWidth
                label="Character Name"
                value={localName}
                onChange={handleNameChange}
                onBlur={handleNameBlur}
                error={!!nameError}
                helperText={nameError || 'Choose a memorable name for your character'}
                placeholder="e.g., Thorin Ironfist, Aria Moonwhisper"
                variant="outlined"
                InputProps={{
                  startAdornment: <PersonIcon sx={{ mr: 1, color: 'text.secondary' }} />
                }}
              />
              
              {localName && !nameError && (
                <Box sx={{ mt: 2 }}>
                  <Alert severity="success" variant="outlined">
                    Great choice! "{localName}" sounds like a legendary hero.
                  </Alert>
                </Box>
              )}
            </CardContent>
          </Card>
        </Box>

        {/* Character Level */}
        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <StarIcon color="primary" />
                Character Level
              </Typography>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <Typography id="level-slider" gutterBottom>
                  Level: {localLevel}
                </Typography>
                <Slider
                  value={localLevel}
                  onChange={handleLevelChange}
                  aria-labelledby="level-slider"
                  valueLabelDisplay="auto"
                  step={1}
                  marks
                  min={1}
                  max={20}
                  sx={{ mb: 2 }}
                />
                <FormHelperText>
                  {levelError || 'Choose your starting character level (1-20)'}
                </FormHelperText>
              </FormControl>

              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {getLevelDescription(localLevel)}
                </Typography>
                
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                  {getLevelFeatures(localLevel).map((feature, index) => (
                    <Chip
                      key={index}
                      label={feature}
                      size="small"
                      variant="outlined"
                      color="primary"
                    />
                  ))}
                </Box>
              </Box>

              {localLevel > 1 && (
                <Alert severity="info" variant="outlined">
                  Starting at level {localLevel} means your character already has some experience and abilities.
                </Alert>
              )}
            </CardContent>
          </Card>
        </Box>

        {/* Preview */}
        <Box sx={{ width: '100%' }}>
          <Card sx={{ bgcolor: 'primary.main', color: 'primary.contrastText' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Character Preview
              </Typography>
              <Typography variant="h4" sx={{ mb: 1 }}>
                {localName || 'Unnamed Character'}
              </Typography>
              <Typography variant="h6">
                Level {localLevel} Adventurer
              </Typography>
              <Typography variant="body2" sx={{ mt: 1, opacity: 0.9 }}>
                {getLevelDescription(localLevel)}
              </Typography>
            </CardContent>
          </Card>
        </Box>

        {/* Character ID Info */}
        <Box sx={{ width: '100%' }}>
          <Box sx={{ mt: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Character ID: {state.characterData.id}
            </Typography>
            <br />
            <Typography variant="caption" color="text.secondary">
              Created: {new Date(state.characterData.created).toLocaleString()}
            </Typography>
            {state.characterData.modified !== state.characterData.created && (
              <>
                <br />
                <Typography variant="caption" color="text.secondary">
                  Last Modified: {new Date(state.characterData.modified).toLocaleString()}
                </Typography>
              </>
            )}
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default OverviewStep;
