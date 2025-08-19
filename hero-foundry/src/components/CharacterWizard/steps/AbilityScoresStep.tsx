import React from 'react';
import { Box, Typography, Card, CardContent, Alert } from '@mui/material';
import { Casino as AbilityIcon } from '@mui/icons-material';

const AbilityScoresStep: React.FC = () => {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <AbilityIcon color="primary" />
          Ability Scores
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Generate and assign your character's six ability scores: Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma.
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Alert severity="info">
            Ability score generation component coming soon! This will include options for point buy, standard array, and rolling dice methods.
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );
};

export default AbilityScoresStep;
