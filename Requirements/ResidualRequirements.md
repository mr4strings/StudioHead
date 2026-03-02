# Residual System Requirements & Logic

## Overview
This document outlines the architecture for the "Residuals" system within the movie production simulation. 

**Business Problem:** Film residuals are complex, conditional financial obligations that trigger based on market conditions (Streaming vs. DVD) and time (Year 1 vs. Year 10).
**Technical Solution:** A hybrid "Lazy Loading" approach. Instead of generating thousands of database rows for every future year, we store the *mathematical formula* for standard contracts and only generate specific rows for *custom exceptions*.

---

## 1. Database Schema

### Table: `ResidualAgreements`
This is the master rule definition. One Contract can have multiple agreements (e.g., one for Netflix, one for DVD).

| Column | Type | Description |
| :--- | :--- | :--- |
| `ResidualID` | PK | Unique Identifier |
| `ContractID` | FK | Link to the parent Contract |
| `MarketType` | Enum | The trigger medium (SVOD, AVOD, Theatrical, Linear TV, Physical Media) |
| `CalculationMode` | Enum | `LinearDecay`, `LinearToFixed`, `Custom` |
| `BasePercentage` | Decimal | The starting rate (e.g., `0.05` for 5%) |
| `DecayRate` | Decimal | The percentage of reduction per year (e.g., `0.10` for 10% drop) |
| `DecayYears` | Int | The duration of the decay logic (The "Z" variable) |
| `FloorPercentage` | Decimal | The minimum rate. If `LinearToFixed`, this is the permanent rate. If `LinearDecay`, this is usually 0. |

### Table: `ResidualOverrides`
This table is **only** populated if `CalculationMode == Custom`. It overrides the math for specific years.

| Column | Type | Description |
| :--- | :--- | :--- |
| `OverrideID` | PK | Unique Identifier |
| `ResidualID` | FK | Link to the parent Agreement |
| `YearIndex` | Int | The specific year (e.g., `3` for 3 years post-release) |
| `OverrideRate` | Decimal | The specific rate for this year (ignoring formulas) |

---

## 2. Calculation Modes (The Logic)

### Mode A: Linear Reduction (The "Sunset" Clause)
* **Logic:** The rate starts at `BasePercentage` and reduces by `DecayRate` every year.
* **End State:** Once it hits 0 (or `FloorPercentage`), payments stop.
* **Use Case:** Standard low-budget streaming deals that expire after 5 years.

### Mode B: Linear to Fixed (The "Perpetuity" Clause)
* **Logic:** The rate starts at `BasePercentage` and reduces by `DecayRate` for `DecayYears`.
* **End State:** Once it hits `FloorPercentage`, it pays that amount forever.
* **Use Case:** High-budget syndication or DVD sales (the "Long Tail").

### Mode C: Custom (The "Manual" Clause)
* **Logic:** The system ignores formulas and looks for a row in `ResidualOverrides` matching the current year.
* **End State:** Defined by the user manually entering data.
* **Use Case:** Weird negotiation tactics (e.g., "I want 0% in year 1 but 5% in year 2").

---

## 3. Implementation Logic (C#)

This method effectively "lazy loads" the rate. It calculates the owed percentage at the moment of processing rather than reading it from a pre-filled table.

```csharp
/// <summary>
/// Calculates the specific residual percentage owed for a specific year.
/// </summary>
/// <param name="agreement">The agreement object containing the formula rules.</param>
/// <param name="yearsSinceRelease">How many years have passed since the project was released.</param>
/// <returns>The decimal percentage to be applied to revenue.</returns>
public decimal GetResidualRate(ResidualAgreement agreement, int yearsSinceRelease)
{
    // 1. Handle Custom Manual Overrides
    // If the mode is Custom, we must query the Override table (or a loaded dictionary).
    if (agreement.CalculationMode == CalculationMode.Custom)
    {
        // Pseudo-code: Repository lookup for the specific year
        var overrideRecord = _residualRepository.GetOverride(agreement.ResidualID, yearsSinceRelease);
        
        // If an override exists return it, otherwise default to 0
        return overrideRecord != null ? overrideRecord.OverrideRate : 0m;
    }

    // 2. Handle Formulaic Calculations (Linear & LinearToFixed)
    
    // Start with the base negotiated rate
    decimal currentRate = agreement.BasePercentage;

    // We only decay for the duration specified in the contract (DecayYears).
    // If yearsSinceRelease > DecayYears, we stop decaying.
    int effectiveDecayYears = Math.Min(yearsSinceRelease, agreement.DecayYears);

    // Apply the decay logic iteratively
    // Note: We could use a power function (Math.Pow) for optimization, 
    // but a loop is clearer for debugging finance logic.
    for (int i = 0; i < effectiveDecayYears; i++)
    {
        // Reduce the current rate by the Decay Rate %
        // Example: 5% rate - (5% * 10% decay) = 4.5%
        currentRate = currentRate - (currentRate * agreement.DecayRate);
    }

    // 3. Apply the Floor (The Safety Net)
    // If the calculation drops below the negotiated floor, return the floor.
    // In "LinearToFixed", this ensures the perpetuity rate kicks in.
    if (currentRate < agreement.FloorPercentage)
    {
        return agreement.FloorPercentage;
    }

    return currentRate;
}