export interface RulesetFeatures {
  races: string[];
  classes: string[];
  backgrounds: string[];
  ability_scores: string[];
  skills: string[];
  proficiencies: string[];
  spellcasting: string[];
}

export interface RulesetRules {
  ability_score_methods: string[];
  hit_die: string;
  proficiency_bonus: number[];
  multiclassing: boolean;
  feats: boolean;
  variant_rules: string[];
}

export interface RulesetValidation {
  max_level: number;
  ability_score_range: [number, number];
  skill_proficiency_limit: number;
  language_limit: number;
}

export interface Ruleset {
  id: string;
  name: string;
  version: string;
  description: string;
  author: string;
  license: string;
  srd: boolean;
  supported: boolean;
  features: RulesetFeatures;
  rules: RulesetRules;
  validation: RulesetValidation;
}

export interface RulesetManager {
  rulesets: Map<string, Ruleset>;
  activeRuleset: Ruleset | null;
  loadRulesets(): Promise<void>;
  getRuleset(id: string): Ruleset | undefined;
  getAllRulesets(): Ruleset[];
  setActiveRuleset(id: string): boolean;
  getActiveRuleset(): Ruleset | null;
  validateRuleset(ruleset: Ruleset): boolean;
  reloadRulesets(): Promise<void>;
}

class RulesetService implements RulesetManager {
  rulesets: Map<string, Ruleset> = new Map();
  activeRuleset: Ruleset | null = null;

  async loadRulesets(): Promise<void> {
    try {
      // In a real Tauri app, this would use the file system API
      // For now, we'll simulate loading the rulesets we created
      const rulesetData: Ruleset[] = [
        await this.loadRulesetFile('dnd5e'),
        await this.loadRulesetFile('pathfinder2e'),
        await this.loadRulesetFile('custom')
      ];

      // Clear existing rulesets
      this.rulesets.clear();

      // Load and validate each ruleset
      for (const ruleset of rulesetData) {
        if (this.validateRuleset(ruleset)) {
          this.rulesets.set(ruleset.id, ruleset);
        }
      }

      // Set default active ruleset
      if (this.rulesets.has('dnd5e')) {
        this.setActiveRuleset('dnd5e');
      }
    } catch (error) {
      console.error('Failed to load rulesets:', error);
      throw error;
    }
  }

  private async loadRulesetFile(id: string): Promise<Ruleset> {
    try {
      // In a real Tauri app, this would read from the file system
      // For now, we'll return the ruleset data directly
      const rulesets: Record<string, Ruleset> = {
        dnd5e: {
          id: "dnd5e",
          name: "Dungeons & Dragons 5th Edition",
          version: "1.0.0",
          description: "Official D&D 5e ruleset with SRD content",
          author: "Wizards of the Coast",
          license: "OGL 1.0a",
          srd: true,
          supported: true,
          features: {
            races: ["human", "elf", "dwarf", "halfling", "dragonborn", "tiefling", "half-elf", "half-orc", "gnome"],
            classes: ["barbarian", "bard", "cleric", "druid", "fighter", "monk", "paladin", "ranger", "rogue", "sorcerer", "warlock", "wizard"],
            backgrounds: ["acolyte", "criminal", "folk-hero", "noble", "sage", "soldier"],
            ability_scores: ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"],
            skills: ["acrobatics", "animal-handling", "arcana", "athletics", "deception", "history", "insight", "intimidation", "investigation", "medicine", "nature", "perception", "performance", "persuasion", "religion", "sleight-of-hand", "stealth", "survival"],
            proficiencies: ["armor", "weapons", "tools", "languages"],
            spellcasting: ["arcane", "divine", "primal"]
          },
          rules: {
            ability_score_methods: ["standard_array", "point_buy", "roll_4d6_drop_lowest"],
            hit_die: "d6",
            proficiency_bonus: [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6],
            multiclassing: true,
            feats: true,
            variant_rules: ["feats", "multiclassing", "flanking", "inspiration"]
          },
          validation: {
            max_level: 20,
            ability_score_range: [1, 20],
            skill_proficiency_limit: 4,
            language_limit: 5
          }
        },
        pathfinder2e: {
          id: "pathfinder2e",
          name: "Pathfinder 2nd Edition",
          version: "1.0.0",
          description: "Official Pathfinder 2e ruleset with SRD content",
          author: "Paizo Publishing",
          license: "OGL 1.0a",
          srd: true,
          supported: true,
          features: {
            races: ["human", "elf", "dwarf", "halfling", "gnome", "goblin", "hobgoblin", "leshy", "lizardfolk", "catfolk", "kobold", "orc", "ratfolk", "tengu"],
            classes: ["alchemist", "barbarian", "bard", "champion", "cleric", "druid", "fighter", "gunslinger", "inventor", "investigator", "magus", "monk", "oracle", "psychic", "ranger", "rogue", "sorcerer", "summoner", "swashbuckler", "witch", "wizard"],
            backgrounds: ["acolyte", "acrobat", "animal-whisperer", "artisan", "barkeep", "barrister", "bounty-hunter", "charlatan", "criminal", "detective", "emissary", "entertainer", "farmhand", "field-medic", "fortune-teller", "gambler", "gladiator", "guard", "herbalist", "hunter", "laborer", "merchant", "miner", "noble", "nomad", "nurse", "pilot", "prisoner", "scholar", "scout", "sailor", "soldier", "street-urchin", "tattoo-artist", "teamster", "urchin"],
            ability_scores: ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"],
            skills: ["acrobatics", "arcana", "athletics", "crafting", "deception", "diplomacy", "intimidation", "lore", "medicine", "nature", "occultism", "performance", "religion", "society", "stealth", "survival", "thievery"],
            proficiencies: ["armor", "weapons", "tools", "languages"],
            spellcasting: ["arcane", "divine", "primal", "occult"]
          },
          rules: {
            ability_score_methods: ["voluntary_flaws", "point_buy", "ancestry_boost"],
            hit_die: "d8",
            proficiency_bonus: [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8],
            multiclassing: true,
            feats: true,
            variant_rules: ["feats", "multiclassing", "free-archetype", "gradual-ability-boosts"]
          },
          validation: {
            max_level: 20,
            ability_score_range: [1, 18],
            skill_proficiency_limit: 8,
            language_limit: 6
          }
        },
        custom: {
          id: "custom",
          name: "Custom Ruleset Template",
          version: "1.0.0",
          description: "Template for creating custom homebrew rulesets",
          author: "User Created",
          license: "Custom",
          srd: false,
          supported: true,
          features: {
            races: [],
            classes: [],
            backgrounds: [],
            ability_scores: ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"],
            skills: [],
            proficiencies: ["armor", "weapons", "tools", "languages"],
            spellcasting: []
          },
          rules: {
            ability_score_methods: ["standard_array", "point_buy", "roll_4d6_drop_lowest"],
            hit_die: "d6",
            proficiency_bonus: [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6],
            multiclassing: false,
            feats: false,
            variant_rules: []
          },
          validation: {
            max_level: 20,
            ability_score_range: [1, 20],
            skill_proficiency_limit: 4,
            language_limit: 5
          }
        }
      };

      return rulesets[id];
    } catch (error) {
      console.error(`Failed to load ruleset ${id}:`, error);
      throw error;
    }
  }

  getRuleset(id: string): Ruleset | undefined {
    return this.rulesets.get(id);
  }

  getAllRulesets(): Ruleset[] {
    return Array.from(this.rulesets.values());
  }

  setActiveRuleset(id: string): boolean {
    const ruleset = this.rulesets.get(id);
    if (ruleset && ruleset.supported) {
      this.activeRuleset = ruleset;
      return true;
    }
    return false;
  }

  getActiveRuleset(): Ruleset | null {
    return this.activeRuleset;
  }

  validateRuleset(ruleset: Ruleset): boolean {
    // Basic validation
    if (!ruleset.id || !ruleset.name || !ruleset.version) {
      return false;
    }

    if (!ruleset.features || !ruleset.rules || !ruleset.validation) {
      return false;
    }

    // Validate required fields exist
    if (!Array.isArray(ruleset.features.races) || !Array.isArray(ruleset.features.classes)) {
      return false;
    }

    if (!Array.isArray(ruleset.features.ability_scores) || ruleset.features.ability_scores.length !== 6) {
      return false;
    }

    return true;
  }

  async reloadRulesets(): Promise<void> {
    await this.loadRulesets();
  }
}

// Create and export singleton instance
export const rulesetService = new RulesetService();

export default RulesetService;
