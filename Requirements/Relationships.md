# Relationship System Requirements

## Overview
A system to track interpersonal relationships between all individuals (Cast and Crew) in the simulation.
- **Range**: -100 (Hatred) to 100 (Love/Best Friend).
- **Default**: 0 (Neutral/Strangers).
- **Scope**: Every individual can potentially have a relationship with every other individual.

## Data Scale & Performance
- **Optimization Strategy**: "Sparse Matrix". We only store non-zero interactions.
- **Assumption**: The vast majority of relationships in a large database will remain 0 (Strangers).
- **Volume**: Even with 50 individuals on a set (1,225 pairs), modern SQLite databases can query this dataset in milliseconds.

## Database Schema
**Table Name**: `Relationships`

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `IndividualID_A` | Integer | PK, FK | Must be the *smaller* of the two IDs. |
| `IndividualID_B` | Integer | PK, FK | Must be the *larger* of the two IDs. |
| `Score` | Integer | | Clamped between -100 and 100. |
| `LastUpdated` | DateTime | | Timestamp of the last interaction. |

## Technical Implementation Rules

### 1. ID Sorting (Directionality)
To prevent duplicate records (e.g., Row 1: `A=1, B=2` and Row 2: `A=2, B=1`), the system must strictly enforce ID order.
- **Rule**: `IndividualID_A` must always be less than `IndividualID_B`.
- **Logic**:
  ```python
  def get_relationship_key(id1, id2):
      return (min(id1, id2), max(id1, id2))
  ```

### 2. The "Default 0" Logic
- **Reading**: Query the table for the pair.
    - If a row is found -> Return `Score`.
    - If NO row is found -> Return `0`.
- **Writing**:
    - If the new score is `0` -> **Delete** the row (Garbage Collection). This keeps the database small.
    - If the new score is non-zero -> Insert or Update.

### 3. Clamping
All calculations must clamp the final result before saving.
```python
new_score = max(-100, min(100, calculated_score))
```
