"""Utility file to seed getPrepped database from data in data/"""

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from model import Disaster, State, County, connect_to_db, db
from server import app

import datetime

import requests
from pprint import pprint

def load_disasters():
    """Load Disaster Declarations and County information into database, as two separate tables that are being created simultaneously.

    Database information being pulled from FEMA API - Disasters Declaration Summaries Data set. Data populates both disastesr and counties tables.

    API returns 1k records max ($top set to variable result_count in payload), while loop continues to make the API call until records_returned is a number less than 1k (which signals no further API calls need to be made).

    To avoid making a call that returns duplicate records, a skip is made ($skip, set to the result_count * iteration)."""

    print "Disasters"

    #deletes any data within the table before seeding
    Disaster.query.delete()


    result_count = 1000
    iteration = 0
    records_returned = 1000

    # makes payload requests from FEMA API
    while records_returned == 1000:
        payload = {'$top': result_count,
                   '$skip': result_count * iteration,
                   '$inlinecount': 'allpages',
                   '$filter': 'declarationDate ge \'1990-01-01T04:00:00.000z\'',
                   '$select': 'disasterNumber,declarationDate,state,incidentType,title,incidentBeginDate,incidentEndDate,placeCode,declaredCountyArea'}
        r = requests.get(
            "http://www.fema.gov/api/open/v1/DisasterDeclarationsSummaries",
            params=payload)

        # iteration counter, starts at zero, for every iteration add 1
        iteration += 1

        disaster_info = r.json()
        metadata = disaster_info['metadata']
        record_count = metadata['count']
        records_returned = len(disaster_info['DisasterDeclarationsSummaries'])

        # parsing through the information returned from API
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

            """Try/Except does two things: the try is doing a check to see if the county is already in the counties tables and if it is, then setting the Disaster.countyArea_id in the disasters table. The except is occuring only when the NoResultFound occurs and is creating the county and adding it to the counties table."""
            try:
                #variable county set to "answer" of query
                county_check = County.query.filter(County.county_name==declaredCountyArea, County.state_code==state).one()

                countyArea_id = county_check.county_id

            # creating a county when NoResultFound error occurs
            except NoResultFound:

                county = County(state_code=state,
                                county_name=declaredCountyArea)

                db.session.add(county)
                #!!!!!!!!! ask bonnie about this again !!!!!!!!!!#
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
    print "Disasters and Counties seeded"


def load_states():
    """Load States into database from a text file."""

    print "States and Territories"

    State.query.delete()

    for row in open("data/states_and_territories.txt"):
        row  = row.rstrip()
        # can't seem to get rid of "\r" character other than doing a .split
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

    # Drop all tables if re-seeding
    db.drop_all()
    # In case tables haven't been created, create them
    db.create_all()

    # Run functions to seed data into database
    load_states()
    load_disasters()
