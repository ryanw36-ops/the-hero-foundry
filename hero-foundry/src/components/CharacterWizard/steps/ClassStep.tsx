import React from 'react';
import { Box, Typography, Card, CardContent, Alert } from '@mui/material';
import { School as ClassIcon } from '@mui/icons-material';

const ClassStep: React.FC = () => {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <ClassIcon color="primary" />
          Choose Class
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Select your character's class, which defines their role in combat, special abilities, and how they gain power.
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Alert severity="info">
            Class selection component coming soon! This will include options for Fighter, Wizard, Rogue, Cleric, and other classes from your selected ruleset.
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ClassStep;
