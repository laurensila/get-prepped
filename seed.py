"""Utility file to seed getPrepped database from data in data/"""

from sqlalchemy import func

from model import Disaster, connect_to_db, db
from server import app

import datetime

import requests
from pprint import pprint

def load_disasters():
    """Load Disaster Declarations into database."""

    print "Disasters"

    Disaster.query.delete()

    payload = {'$select': 'disasterNumber,declarationDate,state,incidentType,title,incidentBeginDate,incidentEndDate,placeCode,declaredCountyArea', '$filter': 'declarationDate ge \'1990-01-01T04:00:00.000z\''}

    r = requests.get(
        "http://www.fema.gov/api/open/v1/DisasterDeclarationsSummaries",
        params=payload)

    disaster_info = r.json()
    pprint(disaster_info)
    # import pdb; pdb.set_trace()
    for incident_dict in disaster_info['DisasterDeclarationsSummaries']:
        disasterNumber = incident_dict.get('disasterNumber')
        declarationDate = incident_dict.get('declarationDate')
        state = incident_dict.get('state')
        incidentType = incident_dict.get('incidentType')
        title = incident_dict.get('title')
        incidentBeginDate = incident_dict.get('incidentBeginDate')
        incidentEndDate = incident_dict.get('incidentEndDate')
        placeCode = incident_dict.get('placeCode')
        declaredCountyArea = incident_dict.get('declaredCountyArea')

    disaster = Disaster(disasterNumber=disasterNumber,
                        state=state,
                        declarationDate=declarationDate,
                        incidentType=incidentType,
                        title=title,
                        incidentBeginDate=incidentBeginDate,
                        incidentEndDate=incidentEndDate,
                        placeCode=placeCode,
                        declaredCountyArea=declaredCountyArea)

    db.session.add(disaster)

    db.session.commit()

    print "DB seeded successfully"


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_disasters()
