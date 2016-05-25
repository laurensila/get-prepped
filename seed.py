"""Utility file to seed getPrepped database from data in data/"""

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from model import Disaster, State, County, connect_to_db, db
from server import app

import datetime

import requests
from pprint import pprint

def load_disasters():
    """Load Disaster Declarations into database."""

    print "Disasters"

    Disaster.query.delete()

    # put comment here
    result_count = 1000
    iteration = 0
    records_returned = 1000

    while records_returned == 1000:
        payload = {'$top': result_count,
                   '$skip': result_count * iteration,
                   '$inlinecount': 'allpages',
                   '$filter': 'declarationDate ge \'1990-01-01T04:00:00.000z\'',
                   '$select': 'disasterNumber,declarationDate,state,incidentType,title,incidentBeginDate,incidentEndDate,placeCode,declaredCountyArea'}
        r = requests.get(
            "http://www.fema.gov/api/open/v1/DisasterDeclarationsSummaries",
            params=payload)

        # for next time
        iteration += 1

        disaster_info = r.json()
        metadata = disaster_info['metadata']
        record_count = metadata['count']
        records_returned = len(disaster_info['DisasterDeclarationsSummaries'])
        # pprint(disaster_info)
        # pprint(metadata)
        # print record_count
        # import pdb; pdb.set_trace()
        #call once: get 1st k
        #call again: skip 1k, get 1k
        # while record_count > 36311:
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

            # print "******************", declaredCountyArea, state

            try:
                #variable county set to "answer" of query
                county_check = County.query.filter(County.county_name==declaredCountyArea, County.state_code==state).one()

                countyArea_id = county_check.county_id

            except NoResultFound:
            #if statement -> if county is an empty list, add county to db

                county = County(state_code=state,
                                county_name=declaredCountyArea)

                db.session.add(county)
                db.session.flush()

                countyArea_id = county.county_id

            county = County.query.filter(County.county_name==declaredCountyArea, County.state_code==state).one()
            countyArea_id = county.county_id

            disaster = Disaster(disasterNumber=disasterNumber,
                                state=state,
                                declarationDate=declarationDate,
                                incidentType=incidentType,
                                title=title,
                                incidentBeginDate=incidentBeginDate,
                                incidentEndDate=incidentEndDate,
                                placeCode=placeCode,
                                declaredCountyArea=declaredCountyArea,
                                countyArea_id=countyArea_id)

            db.session.add(disaster)

    db.session.commit()
    print "Disasters seeded"

# def load_counties():
#     """Loads Counties from FEMA API into database"""
#
#     print "Counties"
#
#     County.query.delete()
#
#     payload = {'$inlinecount': 'allpages',
#                '$filter': 'declarationDate ge \'1990-01-01T04:00:00.000z\'',
#                '$select': 'state,declaredCountyArea'}
#     r = requests.get(
#         "http://www.fema.gov/api/open/v1/DisasterDeclarationsSummaries",
#         params=payload)
#
#     county_info = r.json()
#     metadata = county_info['metadata']
#     record_count = metadata['count']
#     # pprint(disaster_info)
#     pprint(metadata)
#     print record_count
#     # import pdb; pdb.set_trace()
#
#     #information coming form the API about the counties
#     for county_dict in county_info['DisasterDeclarationsSummaries']:
#         state_code = county_dict.get('state')
#         county_name = county_dict.get('declaredCountyArea')
#
#         #variable county set to "answer" of query
#         county_check = County.query.filter(county_name==county_name, state_code==state_code).all()
#         #if statement -> if county is an empty list, add county to db
#         if len(county_check) == 0:
#
#             county = County(state_code=state_code,
#                             county_name=county_name)
#
#             db.session.add(county)
#
#     db.session.commit()
#     print "Counties seeded"


def load_states():
    """Load States into database."""

    print "States and Territories"

    # State.query.delete()

    for row in open("data/states_and_territories.txt"):
        row  = row.rstrip()
        # import pdb; pdb.set_trace()
        piped_rows = row.split("\r")
        for i in piped_rows:
            state_info = i.split("|")
            state_name = state_info[0]
            state_code = state_info[1]

            state = State(state_name=state_name, state_code=state_code)

            db.session.add(state)

            db.session.commit()
    print "States seeded"


if __name__ == "__main__":
    connect_to_db(app)

    db.drop_all()
    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_states()
    # load_counties()
    load_disasters()
