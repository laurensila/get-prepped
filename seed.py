"""Utility file to seed getPrepped database from data in data/"""

from sqlalchemy import func

from model import Disaster, Territory, connect_to_db, db
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
    print "Disasters seeded"


def load_territories():
    """Load Territories into database."""

    print "Territories"

    for row in open("data/states_and_territories.txt"):
        row  = row.rstrip()
        piped_rows = row.split("\r")
        for i in piped_rows:
            state_info = i.split("|")
            territory_name = state_info[0]
            territory_abv = state_info[1]

            territory = Territory(territory_name=territory_name, territory_abv=territory_abv)

            print territory

            db.session.add(territory)

    db.session.commit()
    print "Territories seeded"


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_disasters()
    load_territories()
