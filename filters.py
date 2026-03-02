# This file is for reusable filter functions
from sqlalchemy import or_

#
# Filter to be used when displaying users who can be used as Studioheads
#  
def studio_head(session, Individual):
    """
    Returns a list of the Name column from the Individuals table.
    Filtered for:
    - DateOfDeath is empty
    - Status is Active
    - StudioHead is 1
    Sorted Alphabetically.
    """
    query = session.query(Individual.Name).filter(
        or_(Individual.DateOfDeath == None, Individual.DateOfDeath == ''),
        Individual.Status == 'Active',
        Individual.StudioHead == 1
    ).order_by(Individual.Name.asc())
    
    return [row[0] for row in query.all()]
