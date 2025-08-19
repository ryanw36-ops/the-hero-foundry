import React from 'react';
import { Box, Typography, Card, CardContent, Alert } from '@mui/material';
import { Diversity3 as RaceIcon } from '@mui/icons-material';

const RaceStep: React.FC = () => {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <RaceIcon color="primary" />
          Choose Race
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Select your character's race, which determines their physical traits, special abilities, and cultural background.
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Alert severity="info">
            Race selection component coming soon! This will include options for Human, Elf, Dwarf, Halfling, and other races from your selected ruleset.
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );
};

export default RaceStep;
