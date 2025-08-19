import React from 'react';
import { Box, Typography, Card, CardContent, Alert } from '@mui/material';
import { Psychology as SkillsIcon } from '@mui/icons-material';

const SkillsStep: React.FC = () => {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <SkillsIcon color="primary" />
          Skills & Proficiencies
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Choose your character's skill proficiencies, expertise, and other proficiencies based on their race, class, and background.
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Alert severity="info">
            Skills and proficiencies selection component coming soon! This will include skill choices, expertise options, and language/tool proficiencies.
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );
};

export default SkillsStep;
