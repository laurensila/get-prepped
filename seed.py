"""Utility file to seed getPrepped database from data in data/"""

from sqlalchemy import func

from model import Disaster, connect_to_db, db
from server import app

import datetime

def load_disasters():
    """Load Disaster Declarations into database."""

    print "Disasters"

    Disaster.query.delete()

    for row in open("data/DisasterDeclarationsSummaries.csv"):
        row = row.rstrip()
        print row
        print len(row.split(","))
        print row.split(",")
        disaster_id, ihProgramDeclared, iaProgramDeclared, paProgramDeclared, hmProgramDeclared, state, declarationDate, disasterType, incidentType, title, incidentBeginDate, incidentEndDate, disasterCloseOutDate, placeCode, declaredCountyArea, lastRefresh, md5_hash = row.split(",")

        disaster = Disaster(disaster_id=disaster_id, ihProgramDeclared=ihProgramDeclared, iaProgramDeclared=iaProgramDeclared, paProgramDeclared=paProgramDeclared, hmProgramDeclared=hmProgramDeclared,
        state=state,
        declarationDate=declarationDate,
        disasterType=disasterType,
        incidentType=incidentType,
        title=title,
        incidentBeginDate=incidentBeginDate,
        incidentEndDate=incidentEndDate,
        disasterCloseOutDate=disasterCloseOutDate,
        placeCode=placeCode,
        declaredCountyArea=declaredCountyArea,
        lastRefresh=lastRefresh,
        md5_hash=md5_hash)

        db.session.add(disaster)

    db.session.commit()

# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""
#
#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])
#
#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_disasters()
    # Import different types of data
    # load_users()
    # load_movies()
    # load_ratings()
    # set_val_user_id()
