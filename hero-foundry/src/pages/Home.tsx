import React, { useEffect } from 'react';
import { 
  Typography, 
  Card, 
  CardContent, 
  Button, 
  Box 
} from '@mui/material';
import { 
  Person as PersonIcon,
  Book as BookIcon,
  Help as HelpIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';
import { useLogger } from '../hooks/useLogger';

const Home: React.FC = () => {
  const logger = useLogger();

  useEffect(() => {
    logger.info('Home page loaded', 'Home');
  }, [logger]);

  const handleQuickStart = () => {
    logger.info('Quick start button clicked', 'Home', { action: 'quick_start' });
  };

  const handleBrowseRules = () => {
    logger.info('Browse rules button clicked', 'Home', { action: 'browse_rules' });
  };

  const handleAskForHelp = () => {
    logger.info('Ask for help button clicked', 'Home', { action: 'ask_for_help' });
  };

  const handleOpenSettings = () => {
    logger.info('Open settings button clicked', 'Home', { action: 'open_settings' });
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome to The Hero Foundry
      </Typography>
      <Typography variant="body1" paragraph>
        Create, manage, and level up your D&D characters with ease. 
        This application provides a comprehensive character creation and 
        management system with AI assistance.
      </Typography>
      
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mt: 2 }}>
        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Start
              </Typography>
              <Typography variant="body2" paragraph>
                Get started with character creation in just a few clicks.
              </Typography>
              <Button 
                variant="contained" 
                startIcon={<PersonIcon />}
                fullWidth
                onClick={handleQuickStart}
              >
                Create Your First Character
              </Button>
            </CardContent>
          </Card>
        </Box>
        
        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Learn the Rules
              </Typography>
              <Typography variant="body2" paragraph>
                Access comprehensive D&D rules and explanations.
              </Typography>
              <Button 
                variant="outlined" 
                startIcon={<BookIcon />}
                fullWidth
                onClick={handleBrowseRules}
              >
                Browse Rules
              </Button>
            </CardContent>
          </Card>
        </Box>
        
        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Need Help?
              </Typography>
              <Typography variant="body2" paragraph>
                Get AI-powered assistance for your character builds.
              </Typography>
              <Button 
                variant="outlined" 
                startIcon={<HelpIcon />}
                fullWidth
                onClick={handleAskForHelp}
              >
                Ask for Help
              </Button>
            </CardContent>
          </Card>
        </Box>
        
        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Customize
              </Typography>
              <Typography variant="body2" paragraph>
                Adjust settings and preferences for your experience.
              </Typography>
              <Button 
                variant="outlined" 
                startIcon={<SettingsIcon />}
                fullWidth
                onClick={handleOpenSettings}
              >
                Open Settings
              </Button>
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
};

export default Home;
