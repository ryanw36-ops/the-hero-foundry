import { useCallback, useContext, createContext } from 'react';
import { logger, LogLevel } from '../services/logger';
import type { LogEntry } from '../services/logger';

interface LoggerContextValue {
  debug: (message: string, context?: string, data?: any) => void;
  info: (message: string, context?: string, data?: any) => void;
  warn: (message: string, context?: string, data?: any) => void;
  error: (message: string, context?: string, data?: any, error?: Error) => void;
  fatal: (message: string, context?: string, data?: any, error?: Error) => void;
  getLogs: (level?: LogLevel, context?: string, limit?: number) => LogEntry[];
  clearLogs: () => void;
  exportLogs: () => string;
}

const LoggerContext = createContext<LoggerContextValue | null>(null);

export const LoggerProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const loggerValue: LoggerContextValue = {
    debug: useCallback((message: string, context?: string, data?: any) => {
      logger.debug(message, context, data);
    }, []),
    
    info: useCallback((message: string, context?: string, data?: any) => {
      logger.info(message, context, data);
    }, []),
    
    warn: useCallback((message: string, context?: string, data?: any) => {
      logger.warn(message, context, data);
    }, []),
    
    error: useCallback((message: string, context?: string, data?: any, error?: Error) => {
      logger.error(message, context, data, error);
    }, []),
    
    fatal: useCallback((message: string, context?: string, data?: any, error?: Error) => {
      logger.fatal(message, context, data, error);
    }, []),
    
    getLogs: useCallback((level?: LogLevel, context?: string, limit?: number) => {
      return logger.getLogs(level, context, limit);
    }, []),
    
    clearLogs: useCallback(() => {
      logger.clearLogs();
    }, []),
    
    exportLogs: useCallback(() => {
      return logger.exportLogs();
    }, [])
  };

  return (
    <LoggerContext.Provider value={loggerValue}>
      {children}
    </LoggerContext.Provider>
  );
};

export const useLogger = (): LoggerContextValue => {
  const context = useContext(LoggerContext);
  
  if (!context) {
    throw new Error('useLogger must be used within a LoggerProvider');
  }
  
  return context;
};

export default useLogger;
