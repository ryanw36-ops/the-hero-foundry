import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider, createTheme } from '@mui/material'
import Layout from './components/Layout'
import Home from './pages/Home'
import Characters from './pages/Characters'
import Rules from './pages/Rules'
import Settings from './pages/Settings'
import ErrorBoundary from './components/ErrorBoundary'
import { LoggerProvider } from './hooks/useLogger'

function App() {
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
      <ErrorBoundary>
        <LoggerProvider>
          <Router>
            <Layout>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/characters" element={<Characters />} />
                <Route path="/rules" element={<Rules />} />
                <Route path="/help" element={<div>Help Page - Coming Soon</div>} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </Layout>
          </Router>
        </LoggerProvider>
      </ErrorBoundary>
    </ThemeProvider>
  )
}

export default App
