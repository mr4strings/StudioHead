#Strategy for Guild & Membership Management
This document outlines the architectural strategy for managing Guilds and their Memberships within our system. This design prioritizes scalability (to handle global expansion) and flexibility (to support "hyphenate" professionals who belong to multiple organizations).

1. Architectural Principles
Normalization Over Breadth: We will avoid a "wide table" approach (one column per guild). Instead, we use a many-to-many relationship to ensure that adding a new guild (e.g., a South Korean Actors Guild) is a data update, not a schema change.

Encapsulation of Labor Rules: Guild-specific logic (like "Global Rule One" or "DGC Election Forms") will be handled via a Rule Engine or Strategy Pattern in the code, rather than hardcoding business rules directly into the database fields.

Global-Ready Design: Every guild is assigned a RegionID and CraftType to allow for regional filtering and automated jurisdiction checks.

2. Database Schema Design
We implement a Junction Table (Membership) to link Individuals to Guilds. This allows an individual to hold multiple cards (e.g., SAG + DGA) while tracking unique metadata for each.

A. Table: Guilds (Lookup)
Stores the master list of all available organizations.

GuildID (PK): Unique Identifier.

Name: e.g., "SAG-AFTRA".

Region: e.g., "US", "Canada", "Europe".

CraftType: e.g., "Actor", "Director", "Writer", "Crew".

IsSignatoryRequired: Boolean. Determines if a production must sign with them to hire this member.

B. Table: Individuals
Stores the professional's core data.

IndividualID (PK): Unique Identifier.

LegalName: Primary name for contracts.

PrimaryCraft: The main role they are known for.

C. Table: Membership (Junction)
The bridge that connects people to guilds and stores relationship-specific data.

IndividualID (FK): Link to Individuals.

GuildID (FK): Link to Guilds.

Status: e.g., "Active", "Suspended", "Fi-Core", "Honored".

JoinDate: When the membership began.

MemberNumber: The actual ID issued by the guild.

3. Business Logic & Constraints
To handle the "clusterfuck" of real-world industry rules, our application logic must enforce the following:

I. The "Global Rule One" Check
If an individual is a member of a guild where GlobalRuleOne = True, any production they are assigned to must be checked against the Signatory status of that production.

Logic: if (individual.HasGuild(SAG) && !production.IsSignatory(SAG)) { flag_violation(); }

II. The "Hyphenate" Conflict Resolver
When a member holds two cards (e.g., DGA and WGA) and a strike occurs, the system must flag potential conflicts based on the assigned Role for that specific project.

Rule: If a project role is "Director" and the DGA is active, but the WGA is striking, the member can work only if they perform zero "writer-y" tasks.

III. Regional Election Logic (The "John Smith" Scenario)
For dual-members (e.g., DGA + DGC), our logic will prioritize the Signatory Agreement of the production.

If a production is Canadian-based (DGC), the logic will default to DGC rules unless a "DGA Election" flag is present in the Membership metadata.

4. Implementation Example (C# / Entity Framework)
For our Junior Devs, here is how you define the relationship so you can easily query a person's guilds.

C#

// The Bridge Entity
public class Membership 
{
    public int IndividualId { get; set; }
    public Individual Individual { get; set; }

    public int GuildId { get; set; }
    public Guild Guild { get; set; }

    // Membership metadata
    public string Status { get; set; } // "Active", "Fi-Core", etc.
    public DateTime JoinDate { get; set; }
}

// Logic to check if an actor is "Safe" to work
public bool IsWorkLegal(Individual person, Production movie) 
{
    foreach(var member in person.Memberships) 
    {
        // If SAG member and movie isn't a signatory, it's a strike/violation risk
        if(member.Guild.Name == "SAG-AFTRA" && !movie.IsSignatory)
            return false;
    }
    return true;
}
Next Steps: Would you like me to generate a Python script that populates the Guilds table with the global list we discussed earlier?