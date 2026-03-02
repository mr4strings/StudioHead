# Genre Schema & Logic Strategy

This document outlines the database schema strategy for matching Projects and Scripts to Genres.

## Core Recommendation
**Link Genres to BOTH Projects and Scripts.**

While it might seem redundant to have both `ProjectGenres` and `ScriptGenres`, this separation is critical for a deep simulation game.

### Why?
1. **Source vs. Execution**: A Script represents the *intent* (the blueprint). The Project represents the *execution* (the building).
    - *Example*: A script might be written as a "Serious Drama". However, during production, the Director might take it in a "Campy Horror" direction. The Project needs to reflect the finalized genre, but the Script should retain its original identity for future use.
2. **Projects without Scripts**: If the game allows starting a project from a "Concept" or "Improvisation" (without a script item), you need a place to attach genres to the Project directly.
3. **Data Integrity**: If you only link to Projects, you lose the definition of the Script asset itself. If you only link to Scripts, you force every Project to perfectly match its source material, removing gameplay possibilities (like botched adaptations).

## Schema Definition

### 1. Master Tables
Standard entity definitions.

| Table | Columns | Notes |
| :--- | :--- | :--- |
| **Genres** | `Ref` (PK), `Name` | "Action", "Horror", "Comedy" |
| **Scripts** | `Ref` (PK), `Title`, ... | The source material. |
| **Projects** | `Ref` (PK), `Title`, `ScriptID` (FK), ... | The film being produced. `ScriptID` matches the source script (nullable). |

### 2. Link Tables (Many-to-Many)

#### `ScriptGenres`
Defines the innate genre(s) of the written work.
- `ScriptID` (FK to Scripts)
- `GenreID` (FK to Genres)
- `Weight` (Optional: int, 1-100) - *Could be used to define "Primary" vs "Secondary" genres (e.g., 80% Action, 20% Comedy).*

#### `ProjectGenres`
Defines the final categorization of the film product.
- `ProjectID` (FK to Projects)
- `GenreID` (FK to Genres)
- `Weight` (Optional)

## Operational Logic

### 1. Initialization (New Project)
When a user starts a Project using a Script:
1.  **Fetch** all entries from `ScriptGenres` for the selected `ScriptID`.
2.  **Copy** these entries into `ProjectGenres` linked to the new `ProjectID`.
    - *Result*: The Project starts with the Script's genres by default.

### 2. Genre Drift (During Development)
Gameplay events can modify `ProjectGenres` without touching `ScriptGenres`.
- *Event*: "Director clashes with writer!"
- *Effect*: Remove "Drama" from `ProjectGenres`, add "Action".
- *Result*: The specific movie has changed, but the Script asset in the database remains a "Drama".

### 3. Matching & Scores
- **Penalties**: If `ProjectGenres` differs significantly from `ScriptGenres`, calculate a "Coherence Penalty" (unless the Director has a high "Adaptation" skill).
- **Success**: Fans of the Script's original genre might be disappointed if the Project's genre shifted too much.

## Alternative Considered: "Link to Scripts Only"
- **Approach**: `Project` -> `Script` -> `Genre`.
- **Pros**: Less data duplication.
- **Cons**: 
    - Cannot represent a "Bad Adaptation" where the genre feels wrong.
    - Cannot handle projects that don't have a backing script item.
    - Rigid gameplay (Input always equals Output).
- **Verdict**: Rejected. Too limiting for a simulation game.
