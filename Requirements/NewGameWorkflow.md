# New Game Workflow Requirements

This document outlines the workflow initiated when the user selects "New Game" from the Landing Page.

## Global UI Elements
- **Back Button**: Must be present on all pages.
  - Action: Returns the user to the previous step.
  - If on Step 1: Returns the user to the Landing Page.

## Step 1: Game Setup

### UI Elements
- **Save Name Field**: A free text entry field labeled "Save name".
- **Database Selection**: A label "Database" with a dropdown menu for selecting the database.
- **Next Button**: Triggers validation and moves to the next step if successful.

### Validation
- **Save File**:
  - Must be unique (no existing save with the same name).
  - Must not contain special characters (this should be in-line validation)
- **Database**:
  - Must pass logical error checks (e.g., exclusive contracts with multiple companies).
  - **Note**: Detailed rules are documented in `Requirements/DatabaseValidationStep.md`.
- **Loading State**:
  - Display an overlay with text: "Database validation in progress. This may take several minutes." while validation is running.

### Actions
- **Next Button**: Creates the user's saved game and moves on to Step 2.

## Step 2: Select Character

### Left Sidebar: Candidate List
Loads a list of characters from the `Individuals` table meeting the following criteria:
1. `CanBeStudioHead` is `true`.
2. `DateOfBirth` < (CurrentDate - 18 years).
3. `DateOfDeath` is NOT < CurrentDate.
4. `DateofDebut` is NOT > CurrentDate.
5. `Status` is 'Active'.

The top of the list contains a search bar that allows the user to search for a character by name. The list should filter as the user types. Next to the search bar is a filter icon which opens up the individual filter view. (see IndividualFilter.md for requirements)

Above the search bar are two buttons: "Studio Heads" (default state) and "All Staff" If the user selects all staff we load a list of characters from the `Individuals` table meeting the following criteria:
1. `DateOfBirth` < (CurrentDate - 18 years).
2. `DateOfDeath` is NOT < CurrentDate.
3. `DateofDebut` is NOT > CurrentDate.
4. `Status` is 'Active'.

At the bottom of this list is a button titled "New Character" If the user clicks this button we load the NewCharacter view.

Instead of saving the character to the database we save it to the saved game file. 

### Character Header
A section of the page that displays the character's name, description, and portrait, and current employment. This displays regardless of which tab is selected..
Data is pulled from the Individuals table from the columns name, description, and portrait
Employment is pulled from the Contracts table where the IndividualID matches the selected character. Use the companyID to determine the Company name and companyLogo from the Companies table. 

### Main Content: Character Summary
Displays details for the selected character in tabs.

#### Tab 1: Biography
Default selected tab
Fetched from Individuals table
- Name
- Portrait
- Biography
- Age (Calculated: `CurrentDate` - `DateOfBirth`)
- GenderID
- Pronouns
- Sexuality
- Relationship
- Race
- Nationality

#### Tab 2: Fame
- **Regional Popularity Grid**: Displays `FlagImage` and popularity value from `RegionalPopularity` table for:
  - Canada, US, Mexico, China, Japan, United Kingdom, South Korea, France, India, Latin America, South America, Australia, Africa, Europe, Asia.
- **Reputation**: Display `Reputation` value from `Individuals` table.

#### Tab 3: Skills
- **Production Skills**: Load fields from `ProductionSkills` table for the selected `IndividualID`.
- **Genre Skills**: Load fields from `GenreSkills` table for the selected `IndividualID`.
- **SubGenre Skills**: Load fields from `SubGenreSkills` table for the selected `IndividualID`.

### Actions
- **Select Character Button**: Proceeds to Step 3.

## Step 3: Select Company

### Left Sidebar: Company List
Loads a list from the `Companies` table meeting the following criteria:
1. `State` equals 'active'.
2. `OpenDate` < CurrentDate.
3. `CloseDate` > CurrentDate.

### Main Content
- *TODO: Define data to be loaded for this page.*

### Actions
- **Select Company Button**:
  - Creates a contract record for the selected `IndividualID`:
    - `CompanyID`: Selected Company's ID.
    - `Duration`: NULL.
    - `Salary`: NULL.
    - `SalaryTerm`: NULL.
  - **TODO**: Confirm parameters after creating `Company` table schema.
  - Ends workflow and redirects to the Main Page.
- **Unemployed Button**:
  - Ends workflow and redirects to the Main Page.
