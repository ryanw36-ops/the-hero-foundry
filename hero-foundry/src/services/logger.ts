export const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
  FATAL: 4
} as const;

export type LogLevel = typeof LogLevel[keyof typeof LogLevel];

export interface LogEntry {
  timestamp: Date;
  level: LogLevel;
  message: string;
  context?: string;
  data?: any;
  error?: Error;
}

export interface LoggerConfig {
  minLevel: LogLevel;
  enableConsole: boolean;
  enableFile: boolean;
  maxEntries: number;
}

class Logger {
  private config: LoggerConfig;
  private logs: LogEntry[] = [];
  private subscribers: ((entry: LogEntry) => void)[] = [];

  constructor(config: Partial<LoggerConfig> = {}) {
    this.config = {
      minLevel: LogLevel.INFO,
      enableConsole: true,
      enableFile: false,
      maxEntries: 1000,
      ...config
    };
  }

  private shouldLog(level: LogLevel): boolean {
    return level >= this.config.minLevel;
  }

  private addLogEntry(entry: LogEntry) {
    this.logs.push(entry);
    
    // Keep only the last maxEntries
    if (this.logs.length > this.config.maxEntries) {
      this.logs = this.logs.slice(-this.config.maxEntries);
    }

    // Notify subscribers
    this.subscribers.forEach(subscriber => subscriber(entry));
  }

  private formatMessage(entry: LogEntry): string {
    const timestamp = entry.timestamp.toISOString();
    const levelName = Object.keys(LogLevel).find(key => LogLevel[key as keyof typeof LogLevel] === entry.level) || 'UNKNOWN';
    const context = entry.context ? `[${entry.context}]` : '';
    const data = entry.data ? ` | ${JSON.stringify(entry.data)}` : '';
    const error = entry.error ? ` | Error: ${entry.error.message}` : '';
    
    return `${timestamp} ${levelName} ${context} ${entry.message}${data}${error}`;
  }

  debug(message: string, context?: string, data?: any) {
    this.log(LogLevel.DEBUG, message, context, data);
  }

  info(message: string, context?: string, data?: any) {
    this.log(LogLevel.INFO, message, context, data);
  }

  warn(message: string, context?: string, data?: any) {
    this.log(LogLevel.WARN, message, context, data);
  }

  error(message: string, context?: string, data?: any, error?: Error) {
    this.log(LogLevel.ERROR, message, context, data, error);
  }

  fatal(message: string, context?: string, data?: any, error?: Error) {
    this.log(LogLevel.FATAL, message, context, data, error);
  }

  private log(level: LogLevel, message: string, context?: string, data?: any, error?: Error) {
    if (!this.shouldLog(level)) return;

    const entry: LogEntry = {
      timestamp: new Date(),
      level,
      message,
      context,
      data,
      error
    };

    this.addLogEntry(entry);

    if (this.config.enableConsole) {
      const formattedMessage = this.formatMessage(entry);
      
      switch (level) {
        case LogLevel.DEBUG:
          console.debug(formattedMessage);
          break;
        case LogLevel.INFO:
          console.info(formattedMessage);
          break;
        case LogLevel.WARN:
          console.warn(formattedMessage);
          break;
        case LogLevel.ERROR:
        case LogLevel.FATAL:
          console.error(formattedMessage);
          break;
      }
    }
  }

  // Get logs with optional filtering
  getLogs(level?: LogLevel, context?: string, limit?: number): LogEntry[] {
    let filtered = this.logs;

    if (level !== undefined) {
      filtered = filtered.filter(entry => entry.level >= level);
    }

    if (context) {
      filtered = filtered.filter(entry => entry.context === context);
    }

    if (limit) {
      filtered = filtered.slice(-limit);
    }

    return filtered;
  }

  // Clear logs
  clearLogs() {
    this.logs = [];
  }

  // Subscribe to log entries
  subscribe(callback: (entry: LogEntry) => void): () => void {
    this.subscribers.push(callback);
    
    // Return unsubscribe function
    return () => {
      const index = this.subscribers.indexOf(callback);
      if (index > -1) {
        this.subscribers.splice(index, 1);
      }
    };
  }

  // Update configuration
  updateConfig(newConfig: Partial<LoggerConfig>) {
    this.config = { ...this.config, ...newConfig };
  }

  // Export logs for debugging
  exportLogs(): string {
    return this.logs
      .map(entry => this.formatMessage(entry))
      .join('\n');
  }
}

// Create and export default logger instance
export const logger = new Logger();

// Export the class for custom instances
export default Logger;
