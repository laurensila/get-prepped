"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Disaster(db.Model):
    """Disaster Declaration Summaries."""

    __tablename__ = "disasters"

    disaster_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    disasterNumber = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(5), nullable=False)
    declarationDate = db.Column(db.DateTime, nullable=False)
    disasterType = db.Column(db.String(100))
    incidentType = db.Column(db.String(100))
    title = db.Column(db.String(100), nullable=True)
    incidentBeginDate = db.Column(db.DateTime, nullable=True)
    incidentEndDate = db.Column(db.DateTime, nullable=True)
    placeCode = db.Column(db.String(100), nullable=True)
    declaredCountyArea = db.Column(db.String(100), nullable=True)

    def get_counties():
        county_query = db.session.query(Disaster.declaredCountyArea).distinct()
        counties = county_query.all()
    
        return counties

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Disaster state=%s incidentType=%s title=%s incidentBeginDate=%s placeCode=%s declaredCountyArea=%s>" % (self.state, self.incidentType, self.title, self.incidentBeginDate, self.placeCode, self.declaredCountyArea)

class Territory(db.Model):
    """States and Territories + Corresponding ABVs."""
    __tablename__ = "territories"

    territory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    territory_name = db.Column(db.String(50), nullable=False)
    territory_abv = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Territory territory_name=%s territory_abv=%s>" % (self.territory_name, self.territory_abv)
#
class User(db.Model):
    """User of Website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    territory = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)
#


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///disasters'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
