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

    payload = {'$inlinecount': 'allpages',
               '$filter': 'declarationDate ge \'1990-01-01T04:00:00.000z\'',
               '$select': 'hash,disasterNumber,declarationDate,state,incidentType,title,incidentBeginDate,incidentEndDate,placeCode,declaredCountyArea'}
    r = requests.get(
        "http://www.fema.gov/api/open/v1/DisasterDeclarationsSummaries",
        params=payload)

    disaster_info = r.json()
    metadata = disaster_info['metadata']
    record_count = metadata['count']
    # pprint(disaster_info)
    pprint(metadata)
    print record_count
    # import pdb; pdb.set_trace()
    #call once: get 1st k
    #call again: skip 1k, get 1k
    # while record_count > 36311:
    for incident_dict in disaster_info['DisasterDeclarationsSummaries']:
        hash = incident_dict.get('hash')
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
                            declaredCountyArea=declaredCountyArea,
                            hash=hash)

        db.session.add(disaster)

    db.session.commit()
    print "DB seeded successfully"


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_disasters()
