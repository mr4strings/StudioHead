# Architecture Decisions

## Tech Stack

### Core Language
*   **Python**: Selected for ease of logic implementation and rapid prototyping of simulation engines. The user prioritized logic handling over UI builder tools.
    *   **Version**: Latest stable (3.12+)

### User Interface
*   **TBD**: (Likely textual/terminal based or simple GUI libraries like Tkinter, PyQt, or textual textual-web as the project evolves).

### Data Storage
*   **SQLite**: Selected as the database engine.
    *   **Reasoning**: Ideal for local simulation games distributed on Steam. Allows the entire game state (save file) to be a single `.db` file, which is easy to distribute, copy, and backup. Zero-configuration for the end user (no server installation required), while still offering full SQL power for complex simulation queries.
    *   **Library**: `SQLAlchemy` (ORM). Uses Python's built-in SQLite support.
