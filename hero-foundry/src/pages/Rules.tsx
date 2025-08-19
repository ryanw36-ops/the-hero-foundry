import React from 'react';
import { 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
  Alert,
  CircularProgress,
  Divider
} from '@mui/material';
import { 
  Refresh as RefreshIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import { useRuleset } from '../hooks/useRuleset';
import { useLogger } from '../hooks/useLogger';

const Rules: React.FC = () => {
  const { rulesets, activeRuleset, loading, error, switchRuleset, reloadRulesets } = useRuleset();
  const logger = useLogger();

  const handleRulesetSwitch = (id: string) => {
    const success = switchRuleset(id);
    if (success) {
      logger.info(`Switched to ruleset: ${id}`, 'Rules');
    } else {
      logger.warn(`Failed to switch to ruleset: ${id}`, 'Rules');
    }
  };

  const handleReload = async () => {
    logger.info('Reloading rulesets', 'Rules');
    await reloadRulesets();
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        Error loading rulesets: {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Rules & Rulesets
        </Typography>
        <Button 
          variant="outlined" 
          startIcon={<RefreshIcon />}
          onClick={handleReload}
        >
          Reload Rulesets
        </Button>
      </Box>

      {activeRuleset && (
        <Alert severity="info" sx={{ mb: 3 }}>
          <strong>Active Ruleset:</strong> {activeRuleset.name} v{activeRuleset.version}
          {activeRuleset.srd && <Chip label="SRD" size="small" sx={{ ml: 1 }} />}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Available Rulesets
              </Typography>
              <List>
                {rulesets.map((ruleset, index) => (
                  <React.Fragment key={ruleset.id}>
                    <ListItem>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            {ruleset.name}
                            {ruleset.id === activeRuleset?.id && (
                              <CheckCircleIcon color="success" />
                            )}
                            {ruleset.srd && <Chip label="SRD" size="small" />}
                          </Box>
                        }
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {ruleset.description}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              Version {ruleset.version} • By {ruleset.author} • License: {ruleset.license}
                            </Typography>
                            <Box sx={{ mt: 1 }}>
                              <Typography variant="caption" color="text.secondary">
                                Features: {ruleset.features.races.length} races, {ruleset.features.classes.length} classes, {ruleset.features.skills.length} skills
                              </Typography>
                            </Box>
                          </Box>
                        }
                      />
                      <ListItemSecondaryAction>
                        {ruleset.id !== activeRuleset?.id ? (
                          <Button
                            variant="outlined"
                            size="small"
                            onClick={() => handleRulesetSwitch(ruleset.id)}
                            disabled={!ruleset.supported}
                          >
                            Activate
                          </Button>
                        ) : (
                          <Chip label="Active" color="success" size="small" />
                        )}
                      </ListItemSecondaryAction>
                    </ListItem>
                    {index < rulesets.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Ruleset Information
              </Typography>
              {activeRuleset ? (
                <Box>
                  <Typography variant="body2" paragraph>
                    <strong>Name:</strong> {activeRuleset.name}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Version:</strong> {activeRuleset.version}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Author:</strong> {activeRuleset.author}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>License:</strong> {activeRuleset.license}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Max Level:</strong> {activeRuleset.validation.max_level}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Hit Die:</strong> {activeRuleset.rules.hit_die}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Multiclassing:</strong> {activeRuleset.rules.multiclassing ? 'Yes' : 'No'}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Feats:</strong> {activeRuleset.rules.feats ? 'Yes' : 'No'}
                  </Typography>
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No ruleset selected
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Rules;
