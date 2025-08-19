import { useState, useCallback, useMemo } from 'react';
import { validationService } from '../services/validationService';
import type { ValidationResult, SchemaDefinition } from '../services/validationService';
import { useLogger } from './useLogger';

export interface UseValidationReturn {
  // Validation functions
  validate: (data: any, schemaName: string) => ValidationResult;
  validateMultiple: (items: any[], schemaName: string) => ValidationResult[];
  
  // Schema management
  registerSchema: (name: string, schema: SchemaDefinition) => void;
  getSchema: (name: string) => SchemaDefinition | undefined;
  listSchemas: () => string[];
  
  // Validation state
  lastValidation: ValidationResult | null;
  validationHistory: ValidationResult[];
  
  // Utility functions
  clearHistory: () => void;
  exportSchemas: () => Record<string, SchemaDefinition>;
  importSchemas: (schemas: Record<string, SchemaDefinition>) => void;
  
  // Validation summary
  getSummary: (results: ValidationResult[]) => {
    total: number;
    valid: number;
    invalid: number;
    totalErrors: number;
    totalWarnings: number;
  };
}

export const useValidation = (): UseValidationReturn => {
  const [lastValidation, setLastValidation] = useState<ValidationResult | null>(null);
  const [validationHistory, setValidationHistory] = useState<ValidationResult[]>([]);
  const logger = useLogger();

  // Validate single item
  const validate = useCallback((data: any, schemaName: string): ValidationResult => {
    logger.info(`Validating data against schema: ${schemaName}`, 'useValidation', { schemaName });
    
    const result = validationService.validate(data, schemaName);
    
    setLastValidation(result);
    setValidationHistory(prev => [...prev, result]);
    
    if (result.isValid) {
      logger.info(`Validation successful for ${schemaName}`, 'useValidation', { schemaName });
    } else {
      logger.warn(`Validation failed for ${schemaName}`, 'useValidation', { 
        schemaName, 
        errorCount: result.errors.length,
        warningCount: result.warnings.length 
      });
    }
    
    return result;
  }, [logger]);

  // Validate multiple items
  const validateMultiple = useCallback((items: any[], schemaName: string): ValidationResult[] => {
    logger.info(`Validating ${items.length} items against schema: ${schemaName}`, 'useValidation', { 
      schemaName, 
      itemCount: items.length 
    });
    
    const results = validationService.validateMultiple(items, schemaName);
    
    // Add all results to history
    setValidationHistory(prev => [...prev, ...results]);
    
    // Set last validation to summary of all results
    const summary = validationService.getValidationSummary(results);
    const summaryResult: ValidationResult = {
      isValid: summary.invalid === 0,
      errors: results.flatMap(r => r.errors),
      warnings: results.flatMap(r => r.warnings)
    };
    
    setLastValidation(summaryResult);
    
    logger.info(`Batch validation completed for ${schemaName}`, 'useValidation', { 
      schemaName, 
      total: summary.total,
      valid: summary.valid,
      invalid: summary.invalid,
      totalErrors: summary.totalErrors,
      totalWarnings: summary.totalWarnings
    });
    
    return results;
  }, [logger]);

  // Schema management
  const registerSchema = useCallback((name: string, schema: SchemaDefinition): void => {
    validationService.registerSchema(name, schema);
    logger.info(`Schema registered: ${name}`, 'useValidation', { schemaName: name });
  }, [logger]);

  const getSchema = useCallback((name: string): SchemaDefinition | undefined => {
    return validationService.exportSchemas()[name];
  }, []);

  const listSchemas = useCallback((): string[] => {
    return Object.keys(validationService.exportSchemas());
  }, []);

  // Utility functions
  const clearHistory = useCallback((): void => {
    setValidationHistory([]);
    setLastValidation(null);
    logger.info('Validation history cleared', 'useValidation');
  }, [logger]);

  const exportSchemas = useCallback((): Record<string, SchemaDefinition> => {
    return validationService.exportSchemas();
  }, []);

  const importSchemas = useCallback((schemas: Record<string, SchemaDefinition>): void => {
    validationService.importSchemas(schemas);
    logger.info(`Imported ${Object.keys(schemas).length} schemas`, 'useValidation', { 
      schemaNames: Object.keys(schemas) 
    });
  }, [logger]);

  // Validation summary
  const getSummary = useCallback((results: ValidationResult[]) => {
    return validationService.getValidationSummary(results);
  }, []);

  // Memoized return value
  const returnValue = useMemo<UseValidationReturn>(() => ({
    validate,
    validateMultiple,
    registerSchema,
    getSchema,
    listSchemas,
    lastValidation,
    validationHistory,
    clearHistory,
    exportSchemas,
    importSchemas,
    getSummary
  }), [
    validate,
    validateMultiple,
    registerSchema,
    getSchema,
    listSchemas,
    lastValidation,
    validationHistory,
    clearHistory,
    exportSchemas,
    importSchemas,
    getSummary
  ]);

  return returnValue;
};

export default useValidation;
