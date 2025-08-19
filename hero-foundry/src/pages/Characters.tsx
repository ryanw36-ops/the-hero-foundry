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
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  AutoAwesome as WizardIcon
} from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { useFileStorage } from '../hooks/useFileStorage';
import { useLogger } from '../hooks/useLogger';

const Characters: React.FC = () => {
  const { 
    characters, 
    loading, 
    error,
    saveCharacter,
    deleteCharacter,
    clearError
  } = useFileStorage();
  
  const logger = useLogger();
  
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [selectedCharacter, setSelectedCharacter] = useState<any>(null);
  const [characterName, setCharacterName] = useState('');
  const [characterLevel, setCharacterLevel] = useState(1);
  const [characterClass, setCharacterClass] = useState('');
  const [characterRace, setCharacterRace] = useState('');

  const handleCreateCharacter = async () => {
    if (!characterName.trim() || !characterClass.trim() || !characterRace.trim()) return;
    
    const characterData = {
      name: characterName,
      level: characterLevel,
      class: characterClass,
      race: characterRace,
      created: new Date(),
      modified: new Date()
    };
    
    const characterId = `${characterName.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`;
    await saveCharacter(characterId, characterData);
    
    logger.info('Character created', 'Characters', characterData);
    setCreateDialogOpen(false);
    setCharacterName('');
    setCharacterLevel(1);
    setCharacterClass('');
    setCharacterRace('');
  };

  const handleEditCharacter = async () => {
    if (!selectedCharacter || !characterName.trim()) return;
    
    const updatedData = {
      ...selectedCharacter,
      name: characterName,
      level: characterLevel,
      class: characterClass,
      race: characterRace,
      modified: new Date()
    };
    
    await saveCharacter(selectedCharacter.id, updatedData);
    
    logger.info('Character updated', 'Characters', updatedData);
    setEditDialogOpen(false);
    setSelectedCharacter(null);
  };

  const handleDeleteCharacter = async (characterId: string) => {
    if (confirm('Are you sure you want to delete this character?')) {
      await deleteCharacter(characterId);
      logger.info('Character deleted', 'Characters', { characterId });
    }
  };

  const openEditDialog = (character: any) => {
    setSelectedCharacter(character);
    setCharacterName(character.name);
    setCharacterLevel(character.level);
    setCharacterClass(character.class);
    setCharacterRace(character.race);
    setEditDialogOpen(true);
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
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h4">
          Characters
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={<WizardIcon />}
            component={Link}
            to="/characters/create"
          >
            Character Wizard
          </Button>
          <Button
            variant="outlined"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
          >
            Quick Create
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={clearError}>
          {error}
        </Alert>
      )}
      
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        <Box sx={{ flex: 1 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Your Characters
              </Typography>
              {characters.length === 0 ? (
                <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
                  No characters found. Create your first character to get started!
                </Typography>
              ) : (
                <List>
                  {characters.map((character, index) => (
                    <ListItem key={character.name} divider={index < characters.length - 1}>
                      <ListItemText
                        primary={character.name.replace('.json', '')}
                        secondary={`Modified: ${character.modified.toLocaleString()} • ${formatFileSize(character.size)}`}
                      />
                      <ListItemSecondaryAction>
                        <IconButton 
                          edge="end" 
                          aria-label="edit" 
                          sx={{ mr: 1 }}
                          onClick={() => openEditDialog(character)}
                        >
                          <EditIcon />
                        </IconButton>
                        <IconButton 
                          edge="end" 
                          aria-label="delete"
                          onClick={() => handleDeleteCharacter(character.name)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Box>
        
        <Box sx={{ width: '100%', maxWidth: 400, alignSelf: 'flex-end' }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Storage Stats
              </Typography>
              <Typography variant="body2" paragraph>
                Total Characters: {characters.length}
              </Typography>
              <Typography variant="body2" paragraph>
                Total Size: {formatFileSize(characters.reduce((sum, c) => sum + c.size, 0))}
              </Typography>
              {characters.length > 0 && (
                <Typography variant="body2">
                  Last Modified: {new Date(Math.max(...characters.map(c => c.modified.getTime()))).toLocaleString()}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Create Character Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Character</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
            <TextField
              label="Character Name"
              fullWidth
              value={characterName}
              onChange={(e) => setCharacterName(e.target.value)}
              placeholder="e.g., Thorin Ironfist"
            />
            <TextField
              label="Level"
              type="number"
              fullWidth
              value={characterLevel}
              onChange={(e) => setCharacterLevel(parseInt(e.target.value) || 1)}
              inputProps={{ min: 1, max: 20 }}
            />
            <TextField
              label="Class"
              fullWidth
              value={characterClass}
              onChange={(e) => setCharacterClass(e.target.value)}
              placeholder="e.g., Fighter"
            />
            <TextField
              label="Race"
              fullWidth
              value={characterRace}
              onChange={(e) => setCharacterRace(e.target.value)}
              placeholder="e.g., Dwarf"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleCreateCharacter}
            disabled={!characterName.trim() || !characterClass.trim() || !characterRace.trim()}
            variant="contained"
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Character Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Character</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
            <TextField
              label="Character Name"
              fullWidth
              value={characterName}
              onChange={(e) => setCharacterName(e.target.value)}
            />
            <TextField
              label="Level"
              type="number"
              fullWidth
              value={characterLevel}
              onChange={(e) => setCharacterLevel(parseInt(e.target.value) || 1)}
              inputProps={{ min: 1, max: 20 }}
            />
            <TextField
              label="Class"
              fullWidth
              value={characterClass}
              onChange={(e) => setCharacterClass(e.target.value)}
            />
            <TextField
              label="Race"
              fullWidth
              value={characterRace}
              onChange={(e) => setCharacterRace(e.target.value)}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleEditCharacter}
            disabled={!characterName.trim()}
            variant="contained"
          >
            Save Changes
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Characters;
