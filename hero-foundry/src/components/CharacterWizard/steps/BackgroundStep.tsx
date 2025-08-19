import React from 'react';
import { Box, Typography, Card, CardContent, Alert } from '@mui/material';
import { MenuBook as BackgroundIcon } from '@mui/icons-material';

const BackgroundStep: React.FC = () => {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <BackgroundIcon color="primary" />
          Choose Background
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Select your character's background, which represents their life before becoming an adventurer and provides additional skills and equipment.
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Alert severity="info">
            Background selection component coming soon! This will include options for Acolyte, Criminal, Folk Hero, Noble, and other backgrounds from your selected ruleset.
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );
};

export default BackgroundStep;
