import React from 'react';
import { Box, Typography, Card, CardContent, Alert } from '@mui/material';
import { AutoFixHigh as SpellsIcon } from '@mui/icons-material';

const SpellsStep: React.FC = () => {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <SpellsIcon color="primary" />
          Spells & Cantrips
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Choose your character's starting spells and cantrips (if your class can cast spells).
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Alert severity="info">
            Spell selection component coming soon! This will include spell choices for spellcasting classes, cantrip selection, and spell preparation options.
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );
};

export default SpellsStep;
