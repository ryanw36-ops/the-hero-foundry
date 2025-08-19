import React, { useState, useEffect } from 'react';
import {
  Typography,
  Card,
  CardContent,
  Button,
  Box,
  TextField,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  ExpandMore as ExpandMoreIcon,
  ContentCopy as CopyIcon,
  Refresh as RefreshIcon,
  Clear as ClearIcon
} from '@mui/icons-material';
import { useValidation } from '../hooks/useValidation';
import { useLogger } from '../hooks/useLogger';

const Validation: React.FC = () => {
  const {
    validate,
    validateMultiple,
    validationHistory,
    clearHistory,
    listSchemas,
    getSchema
  } = useValidation();
  
  const logger = useLogger();
  
  const [selectedSchema, setSelectedSchema] = useState<string>('character');
  const [jsonInput, setJsonInput] = useState<string>('');
  const [validationResult, setValidationResult] = useState<any>(null);

  useEffect(() => {
    logger.info('Validation page loaded', 'Validation');
    loadSampleData();
  }, [logger]);

  const loadSampleData = () => {
    const sampleCharacter = {
      id: "sample-character-1",
      name: "Thorin Ironfist",
      level: 5,
      class: "Fighter",
      race: "Dwarf",
      abilityScores: {
        strength: 16,
        dexterity: 14,
        constitution: 18,
        intelligence: 10,
        wisdom: 12,
        charisma: 8
      },
      hitPoints: {
        current: 45,
        maximum: 45
      },
      skills: [
        { name: "Athletics", proficiency: true, modifier: 3 },
        { name: "Perception", proficiency: true, modifier: 1 }
      ],
      equipment: [
        { name: "Battleaxe", quantity: 1, weight: 4.0 },
        { name: "Chain Mail", quantity: 1, weight: 55.0 }
      ],
      created: new Date().toISOString(),
      modified: new Date().toISOString()
    };

    setJsonInput(JSON.stringify(sampleCharacter, null, 2));
  };

  const handleValidate = () => {
    try {
      const data = JSON.parse(jsonInput);
      const result = validate(data, selectedSchema);
      setValidationResult(result);
      
      if (result.isValid) {
        logger.info(`Validation successful for ${selectedSchema}`, 'Validation', { schema: selectedSchema });
      } else {
        logger.warn(`Validation failed for ${selectedSchema}`, 'Validation', { 
          schema: selectedSchema, 
          errors: result.errors.length 
        });
      }
    } catch (error) {
      const errorResult = {
        isValid: false,
        errors: [{
          path: '',
          message: `Invalid JSON: ${error instanceof Error ? error.message : 'Unknown error'}`,
          code: 'INVALID_JSON'
        }],
        warnings: []
      };
      setValidationResult(errorResult);
      logger.error(`JSON parsing error`, 'Validation', { error });
    }
  };

  const handleValidateMultiple = () => {
    try {
      const data = JSON.parse(jsonInput);
      const items = Array.isArray(data) ? data : [data];
      const results = validateMultiple(items, selectedSchema);
      setValidationResult({
        isValid: results.every(r => r.isValid),
        errors: results.flatMap(r => r.errors),
        warnings: results.flatMap(r => r.warnings),
        results
      });
      
      logger.info(`Batch validation completed for ${selectedSchema}`, 'Validation', { 
        schema: selectedSchema, 
        itemCount: items.length 
      });
    } catch (error) {
      const errorResult = {
        isValid: false,
        errors: [{
          path: '',
          message: `Invalid JSON: ${error instanceof Error ? error.message : 'Unknown error'}`,
          code: 'INVALID_JSON'
        }],
        warnings: []
      };
      setValidationResult(errorResult);
      logger.error(`JSON parsing error in batch validation`, 'Validation', { error });
    }
  };

  const handleClearInput = () => {
    setJsonInput('');
    setValidationResult(null);
  };

  const handleCopyResult = () => {
    if (validationResult) {
      navigator.clipboard.writeText(JSON.stringify(validationResult, null, 2));
      logger.info('Validation result copied to clipboard', 'Validation');
    }
  };

  const getSchemaInfo = (schemaName: string) => {
    const schema = getSchema(schemaName);
    if (!schema) return null;
    
    return {
      name: schemaName,
      description: 'Schema definition',
      required: schema.required || [],
      properties: Object.keys(schema.properties || {})
    };
  };

  const availableSchemas = listSchemas();

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        JSON Schema Validation
      </Typography>
      
      <Typography variant="body1" paragraph>
        Test and validate your content against our predefined schemas for characters, rulesets, and homebrew content.
      </Typography>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {/* Schema Selection */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Select Schema
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              {availableSchemas.map((schema) => (
                <Chip
                  key={schema}
                  label={schema}
                  color={selectedSchema === schema ? 'primary' : 'default'}
                  onClick={() => setSelectedSchema(schema)}
                  variant={selectedSchema === schema ? 'filled' : 'outlined'}
                />
              ))}
            </Box>
            {selectedSchema && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  <strong>Schema:</strong> {getSchemaInfo(selectedSchema)?.name}<br />
                  <strong>Properties:</strong> {getSchemaInfo(selectedSchema)?.properties?.length || 0}<br />
                  <strong>Required:</strong> {getSchemaInfo(selectedSchema)?.required?.length || 0}
                </Typography>
              </Box>
            )}
          </CardContent>
        </Card>

        {/* JSON Input */}
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">
                JSON Input
              </Typography>
              <Box>
                <Tooltip title="Load sample data">
                  <IconButton onClick={loadSampleData} size="small">
                    <RefreshIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Clear input">
                  <IconButton onClick={handleClearInput} size="small">
                    <ClearIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </Box>
            <TextField
              multiline
              rows={12}
              fullWidth
              variant="outlined"
              value={jsonInput}
              onChange={(e) => setJsonInput(e.target.value)}
              placeholder="Enter JSON data to validate..."
              sx={{ fontFamily: 'monospace' }}
            />
          </CardContent>
        </Card>

        {/* Validation Actions */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Validation Actions
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                onClick={handleValidate}
                disabled={!jsonInput.trim()}
              >
                Validate Single
              </Button>
              <Button
                variant="outlined"
                onClick={handleValidateMultiple}
                disabled={!jsonInput.trim()}
              >
                Validate Multiple
              </Button>
              <Button
                variant="outlined"
                onClick={clearHistory}
                disabled={validationHistory.length === 0}
              >
                Clear History
              </Button>
            </Box>
          </CardContent>
        </Card>

        {/* Validation Results */}
        {validationResult && (
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Validation Results
                </Typography>
                <Tooltip title="Copy results">
                  <IconButton onClick={handleCopyResult} size="small">
                    <CopyIcon />
                  </IconButton>
                </Tooltip>
              </Box>

              {/* Overall Status */}
              <Alert 
                severity={validationResult.isValid ? 'success' : 'error'}
                sx={{ mb: 2 }}
              >
                {validationResult.isValid ? 'Validation Passed' : 'Validation Failed'}
              </Alert>

              {/* Errors */}
              {validationResult.errors && validationResult.errors.length > 0 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle1" color="error" gutterBottom>
                    Errors ({validationResult.errors.length})
                  </Typography>
                  <List dense>
                    {validationResult.errors.map((error: any, index: number) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <ErrorIcon color="error" />
                        </ListItemIcon>
                        <ListItemText
                          primary={error.message}
                          secondary={`Path: ${error.path || 'root'} | Code: ${error.code}`}
                        />
                        {error.value !== undefined && (
                          <Chip 
                            label={`Value: ${JSON.stringify(error.value)}`} 
                            size="small" 
                            variant="outlined" 
                          />
                        )}
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}

              {/* Warnings */}
              {validationResult.warnings && validationResult.warnings.length > 0 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle1" color="warning.main" gutterBottom>
                    Warnings ({validationResult.warnings.length})
                  </Typography>
                  <List dense>
                    {validationResult.warnings.map((warning: any, index: number) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <WarningIcon color="warning" />
                        </ListItemIcon>
                        <ListItemText
                          primary={warning.message}
                          secondary={`Path: ${warning.path || 'root'} | Code: ${warning.code}`}
                        />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}

              {/* Batch Results */}
              {validationResult.results && (
                <Box>
                  <Typography variant="subtitle1" gutterBottom>
                    Batch Validation Results
                  </Typography>
                  {validationResult.results.map((result: any, index: number) => (
                    <Accordion key={index}>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {result.isValid ? (
                            <CheckIcon color="success" />
                          ) : (
                            <ErrorIcon color="error" />
                          )}
                          <Typography>
                            Item {index + 1} - {result.isValid ? 'Valid' : 'Invalid'}
                          </Typography>
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        {result.errors.length > 0 && (
                          <Box sx={{ mb: 1 }}>
                            <Typography variant="body2" color="error">
                              Errors: {result.errors.length}
                            </Typography>
                            {result.errors.slice(0, 3).map((error: any, errorIndex: number) => (
                              <Typography key={errorIndex} variant="body2" sx={{ ml: 2 }}>
                                • {error.message}
                              </Typography>
                            ))}
                            {result.errors.length > 3 && (
                              <Typography variant="body2" sx={{ ml: 2, fontStyle: 'italic' }}>
                                ... and {result.errors.length - 3} more errors
                              </Typography>
                            )}
                          </Box>
                        )}
                        {result.warnings.length > 0 && (
                          <Box>
                            <Typography variant="body2" color="warning.main">
                              Warnings: {result.warnings.length}
                            </Typography>
                            {result.warnings.slice(0, 2).map((warning: any, warningIndex: number) => (
                              <Typography key={warningIndex} variant="body2" sx={{ ml: 2 }}>
                                • {warning.message}
                              </Typography>
                            ))}
                          </Box>
                        )}
                      </AccordionDetails>
                    </Accordion>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>
        )}

        {/* Validation History */}
        {validationHistory.length > 0 && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Validation History ({validationHistory.length})
              </Typography>
              <List dense>
                {validationHistory.slice(-5).reverse().map((result, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      {result.isValid ? (
                        <CheckIcon color="success" />
                      ) : (
                        <ErrorIcon color="error" />
                      )}
                    </ListItemIcon>
                    <ListItemText
                      primary={`${result.isValid ? 'Valid' : 'Invalid'} - ${result.errors.length} errors, ${result.warnings.length} warnings`}
                      secondary={new Date().toLocaleTimeString()}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        )}
      </Box>
    </Box>
  );
};

export default Validation;
