# Credit & Role Strategy

## Overview

This strategy outlines how `Credits` track the intersection of **Projects** and **Roles**. 
A key requirement is the ability to manage the "staffing up" phase of a production, where a project has defined needs (e.g., 1 Director, 3 Camera Operators) but specific individuals have not yet been hired.

## The "Vacancy Record" Pattern

We will use a **single table approach** where the `Credits` table represents both filled positions and open vacancies.

### Core Concept: Pre-allocation

When a project enters the pre-production/staffing phase:
1.  The game logic calculates the required role composition (e.g., "Script requires 1 Lead Actor, 2 Supporting Actors").
2.  The system **immediately inserts rows** into the `Credits` table for *every* required position.
3.  These rows effectively act as "Job Openings".

### Database Schema

#### Table: `Credits`
This table links a Project to a specific Role definition.

| Column | Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `CreditID` | PK | No | Unique identifier for this specific job slot. |
| `ProjectID` | FK | No | The production this role belongs to. |
| `RoleID` | FK | No | The type of job (e.g., "Director", "Key Grip"). |
| `IndividualID` | FK | **Yes** | **NULL** indicates the role is Vacant. A value indicates the role is Filled. |
| `Status` | Enum | No | Tracks the hiring lifecycle (see below). |
| `Notes` | Text | Yes | Specifics for this slot (e.g., "Requires Stunt Certification"). |

### hiring Lifecycle (Status Column)

The `Status` column drives the gameplay loop for staffing.

1.  **Open**: Default state for a new vacancy. `IndividualID` is NULL.
2.  **Offer Pending**: An offer has been sent to an Individual. `IndividualID` might be temporarily set (pending acceptance) or kept NULL depending on implementation preference (keeping NULL is safer until confirmed).
3.  **Signed**: The individual has accepted. `IndividualID` is set to the Actor/Crew member's ID.
4.  **Completed**: production is wrapped, credit is finalized.
5.  **Terminated**: Individual was fired/quit. The record is either updated to `Open` (clearing `IndividualID`) or marked as historical if we track credit history.

### Use Cases

#### 1. "I need to see who I still need to hire."
Query all credits for the project where `IndividualID` is NULL.

```sql
SELECT R.Name 
FROM Credits C
JOIN Roles R ON C.RoleID = R.RoleID
WHERE C.ProjectID = ? AND C.IndividualID IS NULL
```

#### 2. "I hired Jane Doe as the Director."
Update the specific vacancy row.

```sql
UPDATE Credits 
SET IndividualID = ?, Status = 'Signed' 
WHERE CreditID = ?
```

#### 3. "The Director quit."
Reset the slot to vacant.

```sql
UPDATE Credits 
SET IndividualID = NULL, Status = 'Open' 
WHERE CreditID = ?
```

### Advantages
*   **Unified Data**: No separate "Job Openings" table to sync with a "Credits" table.
*   **Simple Logic**: A project is "fully staffed" when `Count(Credits WHERE IndividualID IS NULL) == 0`.
*   **Flexible Requirements**: If a specific project needs an extra "Camera Operator", we simply INSERT another row for that RoleID.
