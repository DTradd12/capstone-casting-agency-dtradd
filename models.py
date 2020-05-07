from flask_sqlalchemy import SQLAlchemy

# database_path = "postgres://ogaxpfjowkkyiu:00d1acf3b6ff4679db382818a93f7a56b2575ab7471e6d6d2ade4d006e98e37d" \
#                  "@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d9kp5t02bed3ge"
database_path = "postgresql://postgres:password@localhost:5432/castingagency"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    __table_name__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    release_date = db.Column(db.String, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def formatted(self):
        return {
            "id": self.id,
            "title": self.title,
            "release date": self.release_date
        }

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()


class Actor(db.Model):
    __table_name = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def formatted(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()
