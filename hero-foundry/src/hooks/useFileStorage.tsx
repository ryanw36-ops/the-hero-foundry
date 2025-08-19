import { useState, useEffect, useCallback } from 'react';
import { fileStorageService, type FileInfo, type StorageStats } from '../services/fileStorageService';

export const useFileStorage = () => {
  const [initialized, setInitialized] = useState(false);
  const [characters, setCharacters] = useState<FileInfo[]>([]);
  const [backups, setBackups] = useState<FileInfo[]>([]);
  const [stats, setStats] = useState<StorageStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize the service on mount
  useEffect(() => {
    initializeService();
  }, []);

  const initializeService = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      await fileStorageService.initialize();
      setInitialized(true);
      
      // Load initial data
      await Promise.all([
        loadCharacters(),
        loadBackups(),
        loadStats()
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize file storage service');
    } finally {
      setLoading(false);
    }
  }, []);

  const loadCharacters = useCallback(async () => {
    try {
      const characterFiles = await fileStorageService.listCharacters();
      setCharacters(characterFiles);
    } catch (err) {
      console.error('Failed to load characters:', err);
    }
  }, []);

  const loadBackups = useCallback(async () => {
    try {
      const backupFiles = await fileStorageService.listBackups();
      setBackups(backupFiles);
    } catch (err) {
      console.error('Failed to load backups:', err);
    }
  }, []);

  const loadStats = useCallback(async () => {
    try {
      const storageStats = await fileStorageService.getStorageStats();
      setStats(storageStats);
    } catch (err) {
      console.error('Failed to load storage stats:', err);
    }
  }, []);

  const saveCharacter = useCallback(async (id: string, data: any) => {
    try {
      await fileStorageService.saveCharacter(id, data);
      await loadCharacters(); // Refresh the list
      await loadStats(); // Refresh stats
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save character');
      return false;
    }
  }, [loadCharacters, loadStats]);

  const loadCharacter = useCallback(async (id: string) => {
    try {
      return await fileStorageService.loadCharacter(id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load character');
      return null;
    }
  }, []);

  const deleteCharacter = useCallback(async (id: string) => {
    try {
      await fileStorageService.deleteCharacter(id);
      await loadCharacters(); // Refresh the list
      await loadStats(); // Refresh stats
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete character');
      return false;
    }
  }, [loadCharacters, loadStats]);

  const createBackup = useCallback(async (description?: string) => {
    try {
      const backupId = await fileStorageService.createBackup(description);
      await loadBackups(); // Refresh the list
      await loadStats(); // Refresh stats
      return backupId;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create backup');
      return null;
    }
  }, [loadBackups, loadStats]);

  const restoreBackup = useCallback(async (backupId: string) => {
    try {
      await fileStorageService.restoreBackup(backupId);
      // Refresh all data after restore
      await Promise.all([
        loadCharacters(),
        loadBackups(),
        loadStats()
      ]);
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to restore backup');
      return false;
    }
  }, [loadCharacters, loadBackups, loadStats]);

  const exportData = useCallback(async (path: string) => {
    try {
      await fileStorageService.exportData(path);
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export data');
      return false;
    }
  }, []);

  const importData = useCallback(async (path: string) => {
    try {
      await fileStorageService.importData(path);
      // Refresh all data after import
      await Promise.all([
        loadCharacters(),
        loadBackups(),
        loadStats()
      ]);
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to import data');
      return false;
    }
  }, [loadCharacters, loadBackups, loadStats]);

  const refreshAll = useCallback(async () => {
    try {
      setLoading(true);
      await Promise.all([
        loadCharacters(),
        loadBackups(),
        loadStats()
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh data');
    } finally {
      setLoading(false);
    }
  }, [loadCharacters, loadBackups, loadStats]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    // State
    initialized,
    characters,
    backups,
    stats,
    loading,
    error,
    
    // Actions
    saveCharacter,
    loadCharacter,
    deleteCharacter,
    createBackup,
    restoreBackup,
    exportData,
    importData,
    refreshAll,
    clearError,
    
    // Configuration
    config: fileStorageService.config
  };
};

export default useFileStorage;
