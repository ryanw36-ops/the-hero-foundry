import React from 'react';
import { Box, Typography, Card, CardContent, Alert } from '@mui/material';
import { Preview as ReviewIcon } from '@mui/icons-material';

const ReviewStep: React.FC = () => {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <ReviewIcon color="primary" />
          Review & Finish
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Review your character's complete details and finalize your creation.
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Alert severity="info">
            Character review component coming soon! This will display a complete character summary, validation results, and final character creation options.
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ReviewStep;
