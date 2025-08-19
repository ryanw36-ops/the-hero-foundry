import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Card, 
  CardContent,
  Alert,
  AlertTitle
} from '@mui/material';
import { BugReport as BugReportIcon, Refresh as RefreshIcon } from '@mui/icons-material';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({
      error,
      errorInfo
    });

    // Log error to console and any external logging service
    console.error('Error caught by boundary:', error, errorInfo);
    
    // In a production app, you would send this to a logging service
    // this.logErrorToService(error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <Box sx={{ p: 3, maxWidth: 600, mx: 'auto' }}>
          <Card>
            <CardContent>
              <Alert severity="error" sx={{ mb: 2 }}>
                <AlertTitle>Something went wrong</AlertTitle>
                An unexpected error occurred in the application.
              </Alert>
              
              <Typography variant="h6" gutterBottom>
                Error Details
              </Typography>
              
              {this.state.error && (
                <Box sx={{ mb: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                  <Typography variant="body2" fontFamily="monospace">
                    {this.state.error.toString()}
                  </Typography>
                </Box>
              )}
              
              {this.state.errorInfo && (
                <Box sx={{ mb: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                  <Typography variant="body2" fontFamily="monospace">
                    {this.state.errorInfo.componentStack}
                  </Typography>
                </Box>
              )}
              
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button
                  variant="contained"
                  startIcon={<RefreshIcon />}
                  onClick={this.handleReset}
                >
                  Try Again
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<BugReportIcon />}
                  onClick={() => {
                    // In a production app, this would open a bug report form
                    console.log('Bug report requested');
                  }}
                >
                  Report Issue
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
