FlexMoxie: Ecosystem & Versioning Guide (Blake's Guide)
* Classification: Directive (Operational Blueprint)
* Status: Active
* Official Rules SoT Website: https://bmobley333.github.io/MetaScape-VitePress-GitHub-Pages/player-guide/moxie/rules.html
________________
🏛️ 1. Workspace Taxonomy
To maintain S-Tier organization, all project documentation is categorized into three tiers: 1. Canonical Master (SoT): The official rules, mechanics, and numerical data. Contradictions in spreadsheets or code must be resolved to match the SoT. 2. System Specification (Spec / Blueprint): The layouts, tab indices, column/row tags, and Apps Script trigger maps that describe the system structure. 3. Operational Directives (Directives / Rules): Development guidelines, design standards, and coding constraints.
________________
⚙️ 2. The Design-First Pair Programming Model
Development of FlexMoxie is split between Blake (Designer) and Jodar (Coder):
  ┌─────────────────────────────────────────────────────────────┐
 │                    1. Blake (Designer)                      │
 │  • Designs sheet layouts, visuals, and formulas in Drive.   │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                    2. Jodar (Coder)                         │
 │  • Writes local Apps Script JavaScript code in Git.         │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                    3. Automated Audit & Push                │
 │  • Run local critic audit (local_critic.py)                 │
 │  • Push to Google Apps Script Editor via clasp              │
 │  • Verify repository documentation parity (validate_sot.py) │
 └─────────────────────────────────────────────────────────────┘

________________
🔄 3. SDLC Release & Upgrades Strategy
I. Code Updates (Logic Hotfixes)
* Logic bugs in Apps Script (FlexLib/) are pushed directly to the central FlexMoxie - Library. Because character sheets reference this library, all player sheets update automatically in place without requiring file changes.
II. Structural Layout Updates (Major Releases)
* Visual or structural changes (adding stats, altering rows/columns) require a new major version release (e.g. 2.0):
   1. Freeze: The active Version 1.0 templates are frozen.
   2. Clone: The entire developer folder is copied to a new version folder (FlexMoxie 2.0).
   3. Register: The new template IDs are logged in the Version Tracker under version 2.0 with the current release date.
III. Dynamic Version Coexistence
* The Version Tracker spreadsheet keeps a directory map of template IDs by version. This allows different RPG groups to run different versions (e.g. 1.0 vs. 2.0) concurrently on the same codebase. The setup script reads their version and pulls the matching file IDs dynamically.
IV. Safe Character Migration (Export/Import)
* Do not attempt to write scripts that dynamically restructure a player's active character sheet layout.
* Instead, to upgrade: clone a fresh, new version template and run a library script to read data from the old sheet and write it to the new one based on tag maps, swapping the file ID in the Codex. This is 100% stable and prevents data loss.
________________
📂 4. Sidecar Technical Specifications Index
All master sidecars are stored locally under SoT/projects/flex_moxie/docs/ and synced to the Google Drive folder:
* codex_spec.md: Details the Codex Roster Ledger, trigger dispatches, and character sheet copy routines.
* tables_spec.md: Maps Level progression charts, weapon databases, and bound skill validation dispatches (fVerifyIndividualSkills).
* cs_spec.md: Maps the combat dashboard, dynamic dropdown caches, skillset auto-placements, and the print-cleanup duplicator (fPrepGameForPaper).
* custom_abilities_spec.md: Outlines the two-tier homebrew validation and verified publishing rules.
* db_spec.md: Details the flat-table database compilation cache used as middleware between Tables and Character Sheets.
* version_tracker_spec.md: Documents the template registry, self-healing file copier, and rules hyperlink auto-repair.
* design_directives.md: Sets high-level coding constraints (GAS bulk reads/writes, dynamic coordinate scanning, local caches) and distributed custody rules.