from flask_sqlalchemy import SQLAlchemy

user = "postgres"
password = "123"
host = "localhost"
database_name = "dbplants"

database_path = "postgresql://{}:{}@{}/{}".format(
    user, password, host, database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


PLANTS_PER_PAGE = 8


def paginate_plants(request, plants):
    # adding pagination
    # if arg object page not found assign default to 1
    page = request.args.get('page', 1, type=int)
    start = (page-1)*PLANTS_PER_PAGE
    end = start + PLANTS_PER_PAGE

    formatted_plants = [plant.format() for plant in plants]
    return formatted_plants[start:end]


class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    scientific_name = db.Column(db.String(), nullable=False)
    is_poisonous = db.Column(db.Boolean, nullable=False)
    primary_color = db.Column(db.String(), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'is_poisonous': self.is_poisonous,
            'primary_color': self.primary_color
        }
