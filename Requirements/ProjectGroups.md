# Project Groups: Series & Franchises

This document outlines the schema and logic for grouping Projects (Films) into Series and Franchises.

## Concept
- **Series**: A set of films that follow a sequential order (e.g., Iron Man 1-3).
- **Franchise**: A larger universe based on the same IP (e.g., Marvel Cinematic Universe).
- **Project**: The individual film unit.

## Schema Definition

### 1. ProjectGroup Table
Captures the definition of a group.

| Field | Type | Description |
|Ref | int | Primary Key |
| Name | string | Display name of the group |
| Description | string | |
| LogoURL | string | Path to logo asset |
| IsFranchise | boolean | True if this group represents a Franchise |
| IsSeries | boolean | True if this group represents a Series |

### 2. ProjectGrouping Table
Linking table making the Many-to-Many relationship between Projects and Groups.

| Field | Type | Description |
|Ref | int | Primary Key |
| ProjectID | int | Foreign Key to `Project` table |
| ProjectGroupID | int | Foreign Key to `ProjectGroup` table |
| ChronologicalOrder | int | The order of the film within this specific group |

## Logic Validation & Notes
- **Many-to-Many**: A Film can belong to multiple groups (e.g., *Iron Man* is in "Iron Man Series" AND "MCU Franchise").
- **Types**: A generic `ProjectGroup` table allows flexibility.
    - *Future Proofing*: If you later add "Phases" (e.g., MCU Phase 1), this structure supports it (just another Group type).
- **Ordering**: `ChronologicalOrder` allows sorting films within the specific context of the group.

### Potential Enhancements (For Consideration)
1. **Hierarchy**: Currently, there is no direct link between a Series and a Franchise (e.g., "Iron Man Series" belongs to "MCU"). You verify this relationship implicitly by checking if the films in the Series are also in the Franchise.
    - *Option*: Add `ParentGroupID` to `ProjectGroup` if you need to explicitly model "Series X is part of Franchise Y".
2. **Exclusivity**: Can a defined "Series" overlap with another "Series"? The current model allows it.
