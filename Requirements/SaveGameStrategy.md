# Save Game Strategy: SQLite-based State Management

## Description regarding "Database as a File"

For *StudioHead*, we will utilize a **"One Save = One Database File"** architecture using **SQLite**.

Instead of storing all save games in a single centralized database server (like PostgreSQL) or serializing objects to JSON/Pickle files, each individual user saved game will be a standalone `.db` file on the disk (e.g., `MyCampaign.db`).

### Justification

1.  **Complexity Management**: Simulation games involve thousands of interconnected entities (history, stats, relationships). Relational databases are designed to handle this complexity better than flat files (JSON/XML).
2.  **Simplified Logic**: By having one database per save, the code does not need complex filtering (e.g., `WHERE SaveID = 101`) in every single query. The game engine simply connects to the active file.
3.  **Robustness (ACID)**: SQLite is transaction-safe. If the game crashes during a "Save", the database file is far less likely to be corrupted compared to writing a massive JSON string.
4.  **Portability**: A `.db` file is a single file. Users can easily copy, backup, or share their saved games by just moving one file.
5.  **Zero Configuration**: Unlike PostgreSQL, the player does not need to install or configure a database server service. SQLite is built into Python and runs in-process.

## Implementation Steps

The implementation will follow this high-level workflow:

### 1. Schema Definition
*   Define the data models using **SQLAlchemy** (Core & ORM).
*   These models define the "Shape" of the game world (Players, Teams, Matches, History).

### 2. The "Initial World" Template
*   We will generate a "Master" database file (`initial_world.db`) during development or the first game launch.
*   This file contains all the starting data: the static universe, default rosters, and game configurations.
*   This file is treated as **Read-Only** by the runtime engine.

### 3. New Game Workflow
1.  User clicks "New Game".
2.  System allows user to name the save (e.g., "Season 1").
3.  **Action**: System copies `initial_world.db` -> `saves/Season 1.db`.
4.  System initializes the `SQLAlchemy Engine` pointing specifically to `saves/Season 1.db`.

### 4. Load Game Workflow
1.  System scans the designated user saves directory (e.g., `~/Documents/StudioHead/Saves/`).
2.  UI lists all valid `.db` files found.
3.  User selects a file.
4.  System initializes the `SQLAlchemy Engine` pointing to the selected file.
5.  Game state is hydrated from this connection.

### 5. Saving the Game
*   **Concept**: In this architecture, the "Game State" *is* the database.
*   **Runtime**: Changes are committed to the database during turn processing (e.g., after a week of simulation passes).
*   **"Save" Action**: Explicit "Saving" by the user effectively forces a `COMMIT` of any pending in-memory transaction objects and potentially creates a backup copy (e.g., `Season 1.db.bak`) to prevent data loss.
