import { useState } from 'react'
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Container, 
  Box, 
  Button, 
  Card, 
  CardContent,
  Grid,
  ThemeProvider,
  createTheme
} from '@mui/material'
import { 
  Person as PersonIcon,
  Book as BookIcon,
  Settings as SettingsIcon,
  Help as HelpIcon
} from '@mui/icons-material'

function App() {
  const [activeTab, setActiveTab] = useState('characters')

  const theme = createTheme({
    palette: {
      mode: 'dark',
      primary: {
        main: '#7c3aed',
      },
      secondary: {
        main: '#f59e0b',
      },
    },
  })

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              The Hero Foundry
            </Typography>
            <Typography variant="subtitle2" sx={{ mr: 2 }}>
              D&D Character Creator
            </Typography>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Quick Actions
                  </Typography>
                  <Button 
                    variant="contained" 
                    fullWidth 
                    startIcon={<PersonIcon />}
                    sx={{ mb: 1 }}
                  >
                    Create Character
                  </Button>
                  <Button 
                    variant="outlined" 
                    fullWidth 
                    startIcon={<BookIcon />}
                    sx={{ mb: 1 }}
                  >
                    View Characters
                  </Button>
                  <Button 
                    variant="outlined" 
                    fullWidth 
                    startIcon={<HelpIcon />}
                    sx={{ mb: 1 }}
                  >
                    Help Me
                  </Button>
                  <Button 
                    variant="outlined" 
                    fullWidth 
                    startIcon={<SettingsIcon />}
                  >
                    Settings
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={9}>
              <Card>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    Welcome to The Hero Foundry
                  </Typography>
                  <Typography variant="body1" paragraph>
                    Create, manage, and level up your D&D characters with ease. 
                    This application provides a comprehensive character creation and 
                    management system with AI assistance.
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Start by creating your first character or explore the available features.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  )
}

export default App
