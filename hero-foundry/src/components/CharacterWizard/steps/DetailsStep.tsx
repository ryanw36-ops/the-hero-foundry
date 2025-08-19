import React from 'react';
import { Box, Typography, Card, CardContent, Alert } from '@mui/material';
import { Face as DetailsIcon } from '@mui/icons-material';

const DetailsStep: React.FC = () => {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <DetailsIcon color="primary" />
          Character Details
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Add personality traits, ideals, bonds, flaws, appearance, and backstory to bring your character to life.
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Alert severity="info">
            Character details component coming soon! This will include personality traits, ideals, bonds, flaws, appearance description, and backstory creation.
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DetailsStep;
