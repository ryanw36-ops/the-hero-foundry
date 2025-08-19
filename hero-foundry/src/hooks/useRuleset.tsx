import { useState, useEffect, useCallback } from 'react';
import { rulesetService, type Ruleset } from '../services/rulesetService';

export const useRuleset = () => {
  const [rulesets, setRulesets] = useState<Ruleset[]>([]);
  const [activeRuleset, setActiveRuleset] = useState<Ruleset | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load rulesets on mount
  useEffect(() => {
    loadRulesets();
  }, []);

  const loadRulesets = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      await rulesetService.loadRulesets();
      
      const allRulesets = rulesetService.getAllRulesets();
      const currentActive = rulesetService.getActiveRuleset();
      
      setRulesets(allRulesets);
      setActiveRuleset(currentActive);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load rulesets');
    } finally {
      setLoading(false);
    }
  }, []);

  const switchRuleset = useCallback((id: string) => {
    const success = rulesetService.setActiveRuleset(id);
    if (success) {
      const newActive = rulesetService.getActiveRuleset();
      setActiveRuleset(newActive);
    }
    return success;
  }, []);

  const reloadRulesets = useCallback(async () => {
    await loadRulesets();
  }, [loadRulesets]);

  const getRuleset = useCallback((id: string) => {
    return rulesetService.getRuleset(id);
  }, []);

  return {
    rulesets,
    activeRuleset,
    loading,
    error,
    switchRuleset,
    reloadRulesets,
    getRuleset,
    loadRulesets
  };
};

export default useRuleset;
