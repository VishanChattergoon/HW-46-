from flask import Flask, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from logs import log_setup
from loguru import logger

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://localhost/TutorialDB?Driver=ODBC+Driver+17+for+SQL+Server&Server=localhost&Database=TutorialDB&Trusted_Connection=yes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

handlers = log_setup.setup_logging(logger)
class Heros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(26))

    def __init__(self, id, name):
        self.name = name
        self.id = id



@app.route("/")
def mainView():
    return render_template("index.html")

@app.route("/heroes")
def getHeroes():
    try:
        allHeroes = []
        heroes = Heros.query.all()
        for hero in heroes:
            print(hero.name)
            allHeroes.insert(0,{"name":hero.name, "id": hero.id})
    except:
        logger.debug('hi it worked')
    return allHeroes

@app.route("/getHero/<id>")
def getHero(id):
    find_user = Heros.query.filter_by(id=id).first()
    return {"Name":find_user.name, "Id":find_user.id}

@app.route("/delHero", methods=['POST'])
def delHero():
    if request.method == 'POST':
        deletedHero = request.data
        deletedHero = deletedHero.decode('UTF-8')
        print(type(deletedHero))
        find_user = Heros.query.filter_by(name=deletedHero).first()
        db.session.delete(find_user) 
        db.session.commit()
    return  deletedHero + "was deleted."

@app.route("/addHero", methods= ['POST'])
def addHero():
    try:
        if request.method == 'POST':
            data = request.data
            data = data.decode('UTF-8')
            newHero = Heros(11, data)
            db.session.add(newHero)
            db.session.commit()
            logger.debug("something work ")
    except:
            logger.debug("something not work ")
    return data

@app.route("/updHero", methods = ['POST'])
def updHero():
    if request.method == 'POST':
        user2change = request.data
        user2change = user2change.decode('UTF-8')
        find_user = Heros.query.filter_by(name=user2change).first()
        find_user.name = 'testChanged'
        db.session.commit()
    return user2change + " was changed to testChanged."


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    logger.debug("hellow world")
    app.run(debug=True)
