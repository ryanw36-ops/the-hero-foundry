# The Hero Foundry - D&D Character Creator PRD

## Project Overview
**Project Name:** The Hero Foundry - D&D Character Creator  
**Version:** 2.0  
**Date:** 2025-08-18  
**Status:** Engineering Ready  
**Target Platforms:** Desktop & Laptop (Windows/macOS/Linux)  
**Primary Rulebase:** D&D 5e/2024 rules via SRD 5.1/5.2 (licensed content only)  

## Vision Statement
The Hero Foundry D&D Character Creator delivers a clean, desktop-first character creation and management platform that creates rules-compliant D&D characters fast, explains choices via context-aware AI assistance, allows balanced homebrew creation, and provides a modular, expandable architecture for future game systems.

## Business Objectives
- **Primary Goal:** Deliver a fast, accurate D&D character creator with AI-powered assistance
- **Target Market:** D&D players (new and experienced), homebrew content creators, game designers
- **Success Metrics:** Character creation speed, rule compliance, user satisfaction, homebrew adoption

## Core Features

### 1. Modular Ruleset Framework
- **Hot-loadable Rulesets:** Drop-in support for different game systems (D&D 5e, Kids on Bikes, etc.)
- **File-driven Architecture:** Everything (rules, content, homebrew) stored as structured JSON files
- **Schema Validation:** JSON Schema enforcement for all content types
- **Conflict Resolution:** Priority system for core < third-party < homebrew content

### 2. Character Creation & Management
- **Wizard Flow:** Step-by-step character creation (Concept → Abilities → Race → Class → Background → Proficiencies → Equipment → Spells → Review)
- **Autosave & Recovery:** Automatic saving at each step with draft recovery
- **Multiclass Support:** Ruleset-dependent multiclassing with validation
- **Version Snapshots:** Automatic character snapshots at each level-up

### 3. "Help Me" Mode (AI Assistant)
- **Context-Aware Chat:** Always-visible chat panel with current build state context
- **AI Actions:** Explain rules, recommend choices, validate builds, summarize characters
- **Tool Integration:** Direct access to validation, balance checking, and rule lookup
- **Safety Rails:** Rule citations and constraint enforcement in Balanced Mode

### 4. Homebrew Builder
- **Form + JSON Editor:** User-friendly forms with advanced JSON editing capabilities
- **Live Validation:** Real-time schema and balance checking
- **Balance Heuristics:** Power budget analysis with suggested nerfs
- **Compatibility Badging:** Clear indication of Balanced vs Free-for-All compatibility

### 5. Balance System & Modes
- **Balanced Mode:** Strict rule enforcement with power budget validation
- **Free-for-All Mode:** Anything goes with permanent mode flagging
- **Power Budgets:** Racial trait costs, class feature curves, spell access caps
- **Drawback System:** Refunds for character weaknesses to prevent overcompensation

### 6. Level-Up Assistant
- **Guided Progression:** Step-by-step level-up with rule validation
- **Change Detection:** Automatic identification of eligible improvements
- **Diff Viewing:** Clear summary of what changed at each level
- **Snapshot Creation:** Read-only character versions for each level

### 7. Export System
- **Multiple Formats:** PDF (classic character sheet), PNG (rendered image), JSON (full data)
- **Template-driven:** Ruleset-specific export templates
- **Attribution:** Automatic SRD attribution and licensing information
- **Mode Flagging:** Clear indication of Balanced vs Free-for-All characters

### 8. Local-First Storage
- **File-based Storage:** All data stored locally in user documents folder
- **No Cloud Dependencies:** Complete offline functionality
- **Backup via Export:** Export/import for data portability
- **Configurable Project Root:** User-defined storage location

## User Stories

### As a New D&D Player
- I want to create a legal level 1 character in under 5 minutes with AI assistance
- I need clear explanations of rules and character choices
- I want to avoid making rule-breaking mistakes during character creation

### As an Experienced D&D Player
- I want to quickly create and level up characters without rule confusion
- I need full control over character customization while maintaining balance
- I want to manage multiple characters with automatic version tracking

### As a Homebrew Content Creator
- I want to design new races, classes, and items that integrate seamlessly
- I need validation that my content is balanced and rule-compliant
- I want to share my homebrew content as easily distributable files

### As a Game Master
- I want to quickly generate NPCs using the same system
- I need to validate that homebrew content won't break game balance
- I want to export character sheets in familiar formats

## Technical Requirements

### Platform Requirements
- **Desktop Application:** Cross-platform compatibility (Windows, macOS, Linux)
- **No Mobile Support:** Desktop-optimized interface and workflows
- **Offline Functionality:** Complete operation without internet connection

### Performance Requirements
- **Character Creation:** < 5 minutes for level 1 character with Help Me mode
- **Level-up Process:** < 2 minutes with zero rule errors in Balanced Mode
- **Homebrew Import:** < 30 seconds with clear validation feedback
- **App Startup:** < 3 seconds to scan rulesets and load content

### Technical Architecture
- **Frontend:** React + TypeScript with Material-UI components
- **Desktop Shell:** Tauri (Rust) for native performance and small binaries
- **Core Engine:** Rust modules for validation, balance checking, and schema enforcement
- **Data Storage:** File-system based with JSON schemas
- **AI Integration:** ChatGPT API with structured tool calling and fallback mechanisms

### Security & Privacy
- **Local-First:** All data stored on user's machine
- **No Telemetry:** Zero data collection by default
- **Licensing Compliance:** SRD-only content with proper attribution
- **Content Validation:** Schema enforcement for all imported content

## Success Criteria
- [ ] Create legal level 1 character in < 5 minutes with Help Me mode
- [ ] Complete level-up in < 2 minutes with zero rule errors in Balanced Mode
- [ ] Homebrew import with validation < 30 seconds
- [ ] 90% of testers report UI is "clean and easy to understand"
- [ ] Platform handles 100+ concurrent character creation sessions
- [ ] User satisfaction score above 4.5/5.0
- [ ] 90% of users complete their first character creation within 24 hours

## Data Architecture

### Directory Structure
```
DnDCharacterCreator/
├─ rulesets/          # Game system definitions
├─ homebrew/          # User-created content
├─ characters/        # Saved character data
└─ exports/           # Generated outputs
```

### Core Schemas
- **Ruleset Manifest:** System configuration and dependencies
- **Character:** Complete character representation with metadata
- **Race/Class:** Game entity definitions with balance information
- **Feature/Spell/Item:** Detailed game mechanics and properties

### Balance Heuristics
- **Racial Power Budget:** Point-based system for racial traits
- **Class Feature Curves:** Per-level power progression validation
- **Spell Access Caps:** Hard limits on spell progression
- **Equipment Proficiency:** Weighted proficiency category system

## Development Phases

### Phase 1: Core Foundation (Weeks 1-3)
- Tauri + React application shell
- Basic file system and ruleset loading
- JSON schema validation framework
- Character data model and storage

### Phase 2: Character Creation (Weeks 4-6)
- Step-by-step character creation wizard
- Race, class, and background selection
- Ability score generation and management
- Basic validation and error handling

### Phase 3: Advanced Features (Weeks 7-9)
- Level-up system with snapshots
- Homebrew content creation and validation
- Balance checking and power budget analysis
- Export system (PDF, PNG, JSON)

### Phase 4: AI Integration (Weeks 10-12)
- Help Me mode with ChatGPT integration
- Context-aware assistance and recommendations
- Tool calling for validation and balance checking
- Fallback mechanisms for offline operation

## Risk Assessment

### High Risk
- **AI Integration Complexity:** LLM integration may introduce unpredictability
- **Balance System Accuracy:** Power budget heuristics require extensive testing
- **Schema Evolution:** JSON schema changes may break existing content

### Medium Risk
- **Cross-platform Compatibility:** Tauri deployment across different OS versions
- **Performance with Large Content:** Handling extensive homebrew libraries
- **User Experience Complexity:** Balancing power with simplicity

### Low Risk
- **Basic Character Creation:** Core D&D rules are well-established
- **File-based Storage:** Local file system operations are reliable
- **Export Functionality:** HTML/CSS to PDF conversion is mature technology

## Testing Strategy

### Automated Testing
- **Schema Validation:** JSON schema compliance for all content types
- **Balance Checking:** Power budget validation across different character builds
- **Export Rendering:** PDF/PNG generation with content verification
- **AI Tool Integration:** Structured output validation for all AI responses

### User Acceptance Testing
- **Character Creation Speed:** Time trials for various character types
- **Rule Compliance:** Validation that all generated characters follow D&D rules
- **Homebrew Integration:** Testing custom content creation and validation
- **Export Quality:** Verification of generated character sheets

## Constraints & Assumptions

### Technical Constraints
- **Desktop Only:** No mobile or web deployment in v1
- **Local Storage:** No cloud synchronization or account systems
- **SRD Content Only:** Licensed content restrictions for base rulesets
- **Offline Operation:** Must function without internet connection

### Business Constraints
- **Development Timeline:** 12-week development cycle for MVP
- **Team Size:** Small development team with AI assistance
- **Licensing:** Must respect D&D SRD and third-party content licenses
- **Budget:** Development costs within allocated project budget

## Next Steps
1. **Immediate:** Engineering team setup and development environment preparation
2. **Week 1:** Tauri application shell and basic file system operations
3. **Week 2:** JSON schema framework and ruleset loading
4. **Week 3:** Character data model and basic storage
5. **Week 4-6:** Character creation wizard implementation
6. **Week 7-9:** Advanced features and validation systems
7. **Week 10-12:** AI integration and final testing

---

*This PRD is a living document that will be updated as development progresses and requirements are refined. All specifications align with the D&D Character Creator Product Brief v1.0.*


