### Character Header
A section of the page that displays the character's name, description, and portrait, current employer name, current style of contract, and duration of current employment. This displays regardless of which tab is selected.
Data is pulled from the Individuals table from the columns name, description, and portrait.
Employment details are pulled from the Contracts table where the IndividualID matches the selected character. Use the companyID to determine the Company name and companyLogo from the Companies table, type of employment from the Contract table ContractType and Exclusivity columns and the duration is a calculated value based on the current date minus the ContractStartDate. 

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
- Years active (Calculated: `CurrentDate` - `DebutDate`)



#### Tab 2: Fame
Content area shows all values from the RegionalPopularity table for the selected character (found using the IndividualID)
The corresponding flag images are pulled from the assets folder in the Flags subfolder. Image names will match the names in the table (ex: Canada.png)
If a flag image is not found a placeholder image will be displayed.
- **Regional Popularity Grid**: Displays `FlagImage` and popularity value from `RegionalPopularity` table for:
  - Canada, US, Mexico, China, Japan, United Kingdom, South Korea, France, India, Latin America, South America, Australia, Africa, Europe, Asia.
- **Reputation**: Display `Reputation` value from `Individuals` table.

#### Tab 3: Skills
- **Production Skills**: Load fields from `ProductionSkills` table for the selected `IndividualID`.
- **Genre Skills**: Load fields from `GenreSkills` table for the selected `IndividualID`.
- **SubGenre Skills**: Load fields from `SubGenreSkills` table for the selected `IndividualID`.