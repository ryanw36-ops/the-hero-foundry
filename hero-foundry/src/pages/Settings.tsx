import React, { useState } from 'react';
import { 
  Typography, 
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
  Divider,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  LinearProgress
} from '@mui/material';
import { 
  Refresh as RefreshIcon,
  Backup as BackupIcon,
  Restore as RestoreIcon,
  Download as DownloadIcon,
  Upload as UploadIcon
} from '@mui/icons-material';
import { useFileStorage } from '../hooks/useFileStorage';
import { useLogger } from '../hooks/useLogger';

const Settings: React.FC = () => {
  const { 
    characters, 
    backups, 
    stats, 
    loading, 
    error,
    createBackup,
    restoreBackup,
    exportData,
    importData,
    refreshAll,
    clearError,
    config
  } = useFileStorage();
  
  const logger = useLogger();
  
  const [backupDialogOpen, setBackupDialogOpen] = useState(false);
  const [backupDescription, setBackupDescription] = useState('');
  const [backupLoading, setBackupLoading] = useState(false);
  const [restoreDialogOpen, setRestoreDialogOpen] = useState(false);
  const [selectedBackup, setSelectedBackup] = useState<string>('');
  const [restoreLoading, setRestoreLoading] = useState(false);

  const handleCreateBackup = async () => {
    if (!backupDescription.trim()) return;
    
    setBackupLoading(true);
    try {
      const backupId = await createBackup(backupDescription);
      if (backupId) {
        logger.info(`Created backup: ${backupId}`, 'Settings', { description: backupDescription });
        setBackupDialogOpen(false);
        setBackupDescription('');
      }
    } finally {
      setBackupLoading(false);
    }
  };

  const handleRestoreBackup = async () => {
    if (!selectedBackup) return;
    
    setRestoreLoading(true);
    try {
      const success = await restoreBackup(selectedBackup);
      if (success) {
        logger.info(`Restored backup: ${selectedBackup}`, 'Settings');
        setRestoreDialogOpen(false);
        setSelectedBackup('');
      }
    } finally {
      setRestoreLoading(false);
    }
  };

  const handleExportData = async () => {
    const path = prompt('Enter export path:');
    if (path) {
      const success = await exportData(path);
      if (success) {
        logger.info('Data exported successfully', 'Settings', { path });
      }
    }
  };

  const handleImportData = async () => {
    const path = prompt('Enter import path:');
    if (path) {
      const success = await importData(path);
      if (success) {
        logger.info('Data imported successfully', 'Settings', { path });
      }
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings & Storage
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={clearError}>
          {error}
        </Alert>
      )}

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        <Box sx={{ flex: 1 }}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Storage Information
                </Typography>
                <Button 
                  variant="outlined" 
                  startIcon={<RefreshIcon />}
                  onClick={refreshAll}
                >
                  Refresh
                </Button>
              </Box>

              {stats && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="body2" paragraph>
                    <strong>Total Files:</strong> {stats.totalFiles}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Total Size:</strong> {formatFileSize(stats.totalSize)}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Characters:</strong> {stats.characters}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Backups:</strong> {stats.backups}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Rulesets:</strong> {stats.rulesets}
                  </Typography>
                  <Typography variant="body2" paragraph>
                    <strong>Homebrew:</strong> {stats.homebrew}
                  </Typography>
                  {stats.lastBackup && (
                    <Typography variant="body2">
                      <strong>Last Backup:</strong> {stats.lastBackup.toLocaleString()}
                    </Typography>
                  )}
                </Box>
              )}

              <Typography variant="h6" gutterBottom>
                Character Files
              </Typography>
              <List>
                {characters.map((character, index) => (
                  <React.Fragment key={character.name}>
                    <ListItem>
                      <ListItemText
                        primary={character.name.replace('.json', '')}
                        secondary={`${formatFileSize(character.size)} • Modified: ${character.modified.toLocaleString()}`}
                      />
                      <ListItemSecondaryAction>
                        <Chip label="Character" size="small" color="primary" />
                      </ListItemSecondaryAction>
                    </ListItem>
                    {index < characters.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Box>

        <Box sx={{ width: '100%', maxWidth: 400, alignSelf: 'flex-end' }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Storage Actions
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Button
                  variant="contained"
                  startIcon={<BackupIcon />}
                  onClick={() => setBackupDialogOpen(true)}
                  fullWidth
                >
                  Create Backup
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<RestoreIcon />}
                  onClick={() => setRestoreDialogOpen(true)}
                  fullWidth
                >
                  Restore Backup
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={handleExportData}
                  fullWidth
                >
                  Export Data
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<UploadIcon />}
                  onClick={handleImportData}
                  fullWidth
                >
                  Import Data
                </Button>
              </Box>

              <Divider sx={{ my: 2 }} />
              
              <Typography variant="h6" gutterBottom>
                Configuration
              </Typography>
              
              <Typography variant="body2" paragraph>
                <strong>Base Path:</strong> {config.basePath}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Max Backups:</strong> {config.maxBackups}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Auto Backup:</strong> {config.autoBackup ? 'Enabled' : 'Disabled'}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Create Backup Dialog */}
      <Dialog open={backupDialogOpen} onClose={() => setBackupDialogOpen(false)}>
        <DialogTitle>Create Backup</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Backup Description"
            fullWidth
            variant="outlined"
            value={backupDescription}
            onChange={(e) => setBackupDescription(e.target.value)}
            placeholder="e.g., Before major update"
          />
          {backupLoading && (
            <Box sx={{ mt: 2 }}>
              <LinearProgress />
              <Typography variant="body2" sx={{ mt: 1 }}>
                Creating backup...
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBackupDialogOpen(false)} disabled={backupLoading}>
            Cancel
          </Button>
          <Button 
            onClick={handleCreateBackup} 
            disabled={!backupDescription.trim() || backupLoading}
            variant="contained"
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Restore Backup Dialog */}
      <Dialog open={restoreDialogOpen} onClose={() => setRestoreDialogOpen(false)}>
        <DialogTitle>Restore Backup</DialogTitle>
        <DialogContent>
          <Typography variant="body2" paragraph>
            Select a backup to restore from:
          </Typography>
                        <List>
                {backups.map((backup) => (
                  <ListItem 
                    key={backup.name}
                    onClick={() => setSelectedBackup(backup.name)}
                    sx={{ 
                      cursor: 'pointer',
                      backgroundColor: selectedBackup === backup.name ? 'action.selected' : 'transparent'
                    }}
                  >
                    <ListItemText
                      primary={backup.name}
                      secondary={`${formatFileSize(backup.size)} • ${backup.modified.toLocaleString()}`}
                    />
                  </ListItem>
                ))}
              </List>
          {restoreLoading && (
            <Box sx={{ mt: 2 }}>
              <LinearProgress />
              <Typography variant="body2" sx={{ mt: 1 }}>
                Restoring backup...
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRestoreDialogOpen(false)} disabled={restoreLoading}>
            Cancel
          </Button>
          <Button 
            onClick={handleRestoreBackup} 
            disabled={!selectedBackup || restoreLoading}
            variant="contained"
            color="warning"
          >
            Restore
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Settings;
