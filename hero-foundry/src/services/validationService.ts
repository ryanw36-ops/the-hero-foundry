import { logger } from './logger';

// Core validation interfaces
export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

export interface ValidationError {
  path: string;
  message: string;
  code: string;
  value?: any;
}

export interface ValidationWarning {
  path: string;
  message: string;
  code: string;
  value?: any;
}

export interface SchemaDefinition {
  $schema: string;
  $id: string;
  type: string;
  properties: Record<string, any>;
  required?: string[];
  additionalProperties?: boolean;
  definitions?: Record<string, any>;
}

// Content type schemas
export const CHARACTER_SCHEMA: SchemaDefinition = {
  $schema: "http://json-schema.org/draft-07/schema#",
  $id: "character-schema",
  type: "object",
  properties: {
    id: { type: "string", pattern: "^[a-z0-9-]+$" },
    name: { type: "string", minLength: 1, maxLength: 100 },
    level: { type: "integer", minimum: 1, maximum: 20 },
    class: { type: "string", minLength: 1, maxLength: 50 },
    race: { type: "string", minLength: 1, maxLength: 50 },
    abilityScores: {
      type: "object",
      properties: {
        strength: { type: "integer", minimum: 1, maximum: 30 },
        dexterity: { type: "integer", minimum: 1, maximum: 30 },
        constitution: { type: "integer", minimum: 1, maximum: 30 },
        intelligence: { type: "integer", minimum: 1, maximum: 30 },
        wisdom: { type: "integer", minimum: 1, maximum: 30 },
        charisma: { type: "integer", minimum: 1, maximum: 30 }
      },
      required: ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"],
      additionalProperties: false
    },
    hitPoints: {
      type: "object",
      properties: {
        current: { type: "integer", minimum: 0 },
        maximum: { type: "integer", minimum: 1 },
        temporary: { type: "integer", minimum: 0 }
      },
      required: ["current", "maximum"],
      additionalProperties: false
    },
    skills: {
      type: "array",
      items: {
        type: "object",
        properties: {
          name: { type: "string" },
          proficiency: { type: "boolean" },
          expertise: { type: "boolean" },
          modifier: { type: "integer" }
        },
        required: ["name", "proficiency"],
        additionalProperties: false
      }
    },
    equipment: {
      type: "array",
      items: {
        type: "object",
        properties: {
          name: { type: "string" },
          quantity: { type: "integer", minimum: 1 },
          weight: { type: "number", minimum: 0 },
          description: { type: "string" }
        },
        required: ["name", "quantity"],
        additionalProperties: false
      }
    },
    spells: {
      type: "array",
      items: {
        type: "object",
        properties: {
          name: { type: "string" },
          level: { type: "integer", minimum: 0, maximum: 9 },
          school: { type: "string" },
          prepared: { type: "boolean" }
        },
        required: ["name", "level"],
        additionalProperties: false
      }
    },
    created: { type: "string", format: "date-time" },
    modified: { type: "string", format: "date-time" }
  },
  required: ["id", "name", "level", "class", "race", "abilityScores", "hitPoints", "created", "modified"],
  additionalProperties: false
};

export const RULESET_SCHEMA: SchemaDefinition = {
  $schema: "http://json-schema.org/draft-07/schema#",
  $id: "ruleset-schema",
  type: "object",
  properties: {
    id: { type: "string", pattern: "^[a-z0-9-]+$" },
    name: { type: "string", minLength: 1, maxLength: 100 },
    version: { type: "string", pattern: "^\\d+\\.\\d+(\\.\\d+)?(-[a-zA-Z0-9.-]+)?(\\+[a-zA-Z0-9.-]+)?$" },
    description: { type: "string", maxLength: 1000 },
    author: { type: "string", minLength: 1, maxLength: 100 },
    license: { type: "string", minLength: 1, maxLength: 100 },
    srd: { type: "boolean" },
    supported: { type: "boolean" },
    features: {
      type: "object",
      properties: {
        races: { type: "array", items: { type: "string" } },
        classes: { type: "array", items: { type: "string" } },
        backgrounds: { type: "array", items: { type: "string" } },
        abilityScores: { type: "array", items: { type: "string" } },
        skills: { type: "array", items: { type: "string" } },
        proficiencies: { type: "array", items: { type: "string" } },
        spellcasting: { type: "array", items: { type: "string" } }
      },
      required: ["races", "classes", "abilityScores", "skills"],
      additionalProperties: false
    },
    rules: {
      type: "object",
      properties: {
        abilityScoreMethods: { type: "array", items: { type: "string" } },
        hitDie: { type: "string", pattern: "^d[0-9]+$" },
        proficiencyBonus: { type: "array", items: { type: "integer", minimum: 0 } },
        multiclassing: { type: "boolean" },
        feats: { type: "boolean" },
        variantRules: { type: "array", items: { type: "string" } }
      },
      required: ["abilityScoreMethods", "hitDie", "proficiencyBonus"],
      additionalProperties: false
    },
    validation: {
      type: "object",
      properties: {
        maxLevel: { type: "integer", minimum: 1, maximum: 30 },
        abilityScoreRange: { type: "array", items: { type: "integer" }, minItems: 2, maxItems: 2 },
        skillProficiencyLimit: { type: "integer", minimum: 0 },
        languageLimit: { type: "integer", minimum: 0 }
      },
      required: ["maxLevel", "abilityScoreRange"],
      additionalProperties: false
    }
  },
  required: ["id", "name", "version", "description", "author", "license", "features", "rules", "validation"],
  additionalProperties: false
};

export const HOMEBREW_SCHEMA: SchemaDefinition = {
  $schema: "http://json-schema.org/draft-07/schema#",
  $id: "homebrew-schema",
  type: "object",
  properties: {
    id: { type: "string", pattern: "^[a-z0-9-]+$" },
    name: { type: "string", minLength: 1, maxLength: 100 },
    type: { type: "string", enum: ["race", "class", "background", "feat", "spell", "item", "monster"] },
    version: { type: "string", pattern: "^\\d+\\.\\d+(\\.\\d+)?(-[a-zA-Z0-9.-]+)?(\\+[a-zA-Z0-9.-]+)?$" },
    description: { type: "string", maxLength: 2000 },
    author: { type: "string", minLength: 1, maxLength: 100 },
    ruleset: { type: "string", pattern: "^[a-z0-9-]+$" },
    balance: {
      type: "object",
      properties: {
        powerLevel: { type: "string", enum: ["underpowered", "balanced", "overpowered"] },
        complexity: { type: "string", enum: ["simple", "moderate", "complex"] },
        playtested: { type: "boolean" },
        notes: { type: "string", maxLength: 1000 }
      },
      required: ["powerLevel", "complexity"],
      additionalProperties: false
    },
    content: { type: "object" },
    created: { type: "string", format: "date-time" },
    modified: { type: "string", format: "date-time" }
  },
  required: ["id", "name", "type", "version", "description", "author", "ruleset", "balance", "content", "created", "modified"],
  additionalProperties: false
};

// Schema registry
export const SCHEMA_REGISTRY: Record<string, SchemaDefinition> = {
  character: CHARACTER_SCHEMA,
  ruleset: RULESET_SCHEMA,
  homebrew: HOMEBREW_SCHEMA
};

// Validation service class
export class ValidationService {
  private schemas: Map<string, SchemaDefinition> = new Map();
  private customValidators: Map<string, (data: any) => ValidationResult> = new Map();

  constructor() {
    this.initializeSchemas();
  }

  private initializeSchemas(): void {
    Object.entries(SCHEMA_REGISTRY).forEach(([key, schema]) => {
      this.schemas.set(key, schema);
    });
    
    logger.info('Validation service initialized with schemas', 'ValidationService', {
      schemas: Array.from(this.schemas.keys())
    });
  }

  // Register a custom schema
  registerSchema(name: string, schema: SchemaDefinition): void {
    this.schemas.set(name, schema);
    logger.info(`Schema registered: ${name}`, 'ValidationService', { schemaName: name });
  }

  // Register a custom validator function
  registerValidator(name: string, validator: (data: any) => ValidationResult): void {
    this.customValidators.set(name, validator);
    logger.info(`Custom validator registered: ${name}`, 'ValidationService', { validatorName: name });
  }

  // Validate data against a schema
  validate(data: any, schemaName: string): ValidationResult {
    const schema = this.schemas.get(schemaName);
    if (!schema) {
      return {
        isValid: false,
        errors: [{
          path: '',
          message: `Schema '${schemaName}' not found`,
          code: 'SCHEMA_NOT_FOUND'
        }],
        warnings: []
      };
    }

    try {
      const result = this.validateAgainstSchema(data, schema);
      logger.info(`Validation completed for ${schemaName}`, 'ValidationService', {
        schemaName,
        isValid: result.isValid,
        errorCount: result.errors.length,
        warningCount: result.warnings.length
      });
      return result;
    } catch (error) {
      logger.error(`Validation error for ${schemaName}`, 'ValidationService', { schemaName, error });
      return {
        isValid: false,
        errors: [{
          path: '',
          message: `Validation error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          code: 'VALIDATION_ERROR'
        }],
        warnings: []
      };
    }
  }

  // Core validation logic
  private validateAgainstSchema(data: any, schema: SchemaDefinition): ValidationResult {
    const errors: ValidationError[] = [];
    const warnings: ValidationWarning[] = [];

    // Basic type validation
    if (schema.type === 'object' && typeof data !== 'object') {
      errors.push({
        path: '',
        message: `Expected object, got ${typeof data}`,
        code: 'TYPE_MISMATCH',
        value: data
      });
      return { isValid: false, errors, warnings };
    }

    if (schema.type === 'array' && !Array.isArray(data)) {
      errors.push({
        path: '',
        message: `Expected array, got ${typeof data}`,
        code: 'TYPE_MISMATCH',
        value: data
      });
      return { isValid: false, errors, warnings };
    }

    // Required properties validation
    if (schema.required && schema.type === 'object') {
      schema.required.forEach(prop => {
        if (!(prop in data)) {
          errors.push({
            path: prop,
            message: `Required property '${prop}' is missing`,
            code: 'REQUIRED_PROPERTY_MISSING'
          });
        }
      });
    }

    // Properties validation
    if (schema.properties && schema.type === 'object') {
      Object.entries(schema.properties).forEach(([propName, propSchema]) => {
        if (propName in data) {
          const propResult = this.validateProperty(data[propName], propSchema, propName);
          errors.push(...propResult.errors.map(err => ({
            ...err,
            path: err.path ? `${propName}.${err.path}` : propName
          })));
          warnings.push(...propResult.warnings.map(warn => ({
            ...warn,
            path: warn.path ? `${propName}.${warn.path}` : propName
          })));
        }
      });

      // Check for additional properties
      if (schema.additionalProperties === false) {
        Object.keys(data).forEach(prop => {
          if (!schema.properties![prop] && !schema.required?.includes(prop)) {
            errors.push({
              path: prop,
              message: `Additional property '${prop}' not allowed`,
              code: 'ADDITIONAL_PROPERTY_NOT_ALLOWED',
              value: data[prop]
            });
          }
        });
      }
    }

    // Array validation
    if (schema.type === 'array' && Array.isArray(data)) {
      if ('items' in schema && schema.items) {
        data.forEach((item, index) => {
          const itemResult = this.validateProperty(item, schema.items, index.toString());
          errors.push(...itemResult.errors.map(err => ({
            ...err,
            path: err.path ? `${index}.${err.path}` : index.toString()
          })));
          warnings.push(...itemResult.warnings.map(warn => ({
            ...warn,
            path: warn.path ? `${index}.${warn.path}` : index.toString()
          })));
        });
      }
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  // Validate individual properties
  private validateProperty(value: any, schema: any, path: string): ValidationResult {
    const errors: ValidationError[] = [];
    const warnings: ValidationWarning[] = [];

    // Type validation
    if (schema.type && !this.checkType(value, schema.type)) {
      errors.push({
        path,
        message: `Expected ${schema.type}, got ${typeof value}`,
        code: 'TYPE_MISMATCH',
        value
      });
    }

    // String validation
    if (schema.type === 'string') {
      if (typeof value === 'string') {
        if (schema.minLength && value.length < schema.minLength) {
          errors.push({
            path,
            message: `String too short. Minimum length: ${schema.minLength}`,
            code: 'STRING_TOO_SHORT',
            value
          });
        }
        if (schema.maxLength && value.length > schema.maxLength) {
          errors.push({
            path,
            message: `String too long. Maximum length: ${schema.maxLength}`,
            code: 'STRING_TOO_LONG',
            value
          });
        }
        if (schema.pattern && !new RegExp(schema.pattern).test(value)) {
          errors.push({
            path,
            message: `String does not match pattern: ${schema.pattern}`,
            code: 'PATTERN_MISMATCH',
            value
          });
        }
        if (schema.enum && !schema.enum.includes(value)) {
          errors.push({
            path,
            message: `Value must be one of: ${schema.enum.join(', ')}`,
            code: 'ENUM_MISMATCH',
            value
          });
        }
      }
    }

    // Number validation
    if (schema.type === 'integer' || schema.type === 'number') {
      if (typeof value === 'number') {
        if (schema.minimum !== undefined && value < schema.minimum) {
          errors.push({
            path,
            message: `Value too small. Minimum: ${schema.minimum}`,
            code: 'VALUE_TOO_SMALL',
            value
          });
        }
        if (schema.maximum !== undefined && value > schema.maximum) {
          errors.push({
            path,
            message: `Value too large. Maximum: ${schema.maximum}`,
            code: 'VALUE_TOO_LARGE',
            value
          });
        }
      }
    }

    // Array validation
    if (schema.type === 'array' && Array.isArray(value)) {
      if (schema.minItems && value.length < schema.minItems) {
        errors.push({
          path,
          message: `Array too short. Minimum items: ${schema.minItems}`,
          code: 'ARRAY_TOO_SHORT',
          value
        });
      }
      if (schema.maxItems && value.length > schema.maxItems) {
        errors.push({
          path,
          message: `Array too long. Maximum items: ${schema.maxItems}`,
          code: 'ARRAY_TOO_LONG',
          value
        });
      }
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  // Check if value matches expected type
  private checkType(value: any, expectedType: string): boolean {
    switch (expectedType) {
      case 'string':
        return typeof value === 'string';
      case 'number':
        return typeof value === 'number';
      case 'integer':
        return typeof value === 'number' && Number.isInteger(value);
      case 'boolean':
        return typeof value === 'boolean';
      case 'object':
        return typeof value === 'object' && value !== null && !Array.isArray(value);
      case 'array':
        return Array.isArray(value);
      case 'null':
        return value === null;
      default:
        return true; // Unknown type, assume valid
    }
  }

  // Validate multiple items
  validateMultiple(items: any[], schemaName: string): ValidationResult[] {
    return items.map(item => this.validate(item, schemaName));
  }

  // Get validation summary
  getValidationSummary(results: ValidationResult[]): {
    total: number;
    valid: number;
    invalid: number;
    totalErrors: number;
    totalWarnings: number;
  } {
    const total = results.length;
    const valid = results.filter(r => r.isValid).length;
    const invalid = total - valid;
    const totalErrors = results.reduce((sum, r) => sum + r.errors.length, 0);
    const totalWarnings = results.reduce((sum, r) => sum + r.warnings.length, 0);

    return {
      total,
      valid,
      invalid,
      totalErrors,
      totalWarnings
    };
  }

  // Export schemas
  exportSchemas(): Record<string, SchemaDefinition> {
    return Object.fromEntries(this.schemas);
  }

  // Import schemas
  importSchemas(schemas: Record<string, SchemaDefinition>): void {
    Object.entries(schemas).forEach(([name, schema]) => {
      this.registerSchema(name, schema);
    });
  }
}

// Create and export default instance
export const validationService = new ValidationService();
export default ValidationService;
