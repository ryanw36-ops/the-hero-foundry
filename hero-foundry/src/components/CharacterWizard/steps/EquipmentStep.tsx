import React from 'react';
import { Box, Typography, Card, CardContent, Alert } from '@mui/material';
import { Inventory as EquipmentIcon } from '@mui/icons-material';

const EquipmentStep: React.FC = () => {
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <EquipmentIcon color="primary" />
          Starting Equipment
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Select your character's starting equipment, weapons, armor, and gear based on their class and background.
        </Typography>
      </Box>

      <Card>
        <CardContent>
          <Alert severity="info">
            Equipment selection component coming soon! This will include starting equipment packages, individual item selection, and gear customization.
          </Alert>
        </CardContent>
      </Card>
    </Box>
  );
};

export default EquipmentStep;
