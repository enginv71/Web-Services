from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask import jsonify, Flask, request
from flask import abort
from flask import json  


import logging
import logger

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

log = logging.getLogger(__name__)

res = Flask(__name__)

res.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
res.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(res)
db = SQLAlchemy(res)
parser= reqparse.RequestParser()


logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/home/stajyer/.virtualenvs/rest/flaskk/deneme.log')
logger.addHandler(handler)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return'<user %r>' % self.username

    def save(self):
        db.session.add(self)
        db.session.commit()


@res.route("/api/eng/delet", methods = ['DELETE'])
def usr_delet():
    try:
        if request.method == 'DELETE':
            data = request.form
            yeni_kullanici=User.query.filter_by(username = data['username']).first()
            db.session.delete(yeni_kullanici)
            db.session.commit()
            logger.info("Silinen kullanici : {}".format(data['username']))
            return jsonify({
                'message':'Deletee',
                'username': data['username']
            }),202
    except Exception:
        logger.warning("Böyle kullanici yok -> {}".format(data["username"]))

#import ipdb; ipdb.set_trace()

@res.route("/api/eng/get/<user>", methods = ['GET'])
def usr_get(user):
    try:
        if request.method == 'GET':
            yeni_kullanici = User.query.filter_by(username = user).first()
            logger.info("Kullanici bilgileri -> {}".format(yeni_kullanici.username))
            logger.info("Kullanici bilgileri -> {}".format(yeni_kullanici.email))
            logger.info("Kullanici bilgileri -> {}".format(yeni_kullanici.password))
            return jsonify({
                'message' : 'GETTT',
                'username' : yeni_kullanici.username,
                'email' : yeni_kullanici.email,
                'password' : yeni_kullanici.password
            }),200
    except Exception:
        logger.error("Kullanici bilgileri bulunmamaktadır -> {}".format(user))

@res.route("/api/eng/kayit", methods = ['POST'])
def usr_kayit():
    try:
        if request.method == 'POST':
            data = request.form
            yeni_kullanici = User(username = data['username'],email = data['email'],password = data['password'])
            db.session.add(yeni_kullanici)
            db.session.commit()
            logger.info("Kayit basarili -> {}".format(data["username"]))
            logger.info("Kayit basarili -> {}".format(data["email"]))
            logger.info("Kayit basarili -> {}".format(int(data["password"])))
            return jsonify({
                'message':'Createdd',
                'username': data['username']
            }),201
    except Exception:
        logger.error("Kayit basarisiz sifre -> {}".format(yeni_kullanici.password))
        #logger.error("Kayit basarisiz kullanici -> {}".format(data["username"]))
        #logger.error("Kayit basarisiz email -> {}".format(data["email"]))
        
Session = sessionmaker()
Session.configure(bind = res)
session = Session()


@res.route("/api/eng/guncelle/", methods = ['PUT'])
def guncelle():
    #import ipdb; ipdb.set_trace()
    try:
        data = request.form
        _user = User.query.filter_by(id=int(data["id"])).first()
        _user.username = data["username"]
        _user.email = data["email"]
        _user.password = int(data["password"])
        _user.save()         
     
        logger.info(data["password"])
        
        return jsonify({
                'message':'Updated {}'.format(data["username"]),   
            }),201  
    except Exception as err:
        logger.error("Characters are not used -> {}".format(err))
        # print(err)
        #raise ValueError(str(err)+ ' Characters are not used. ')
        #print("hata olustu")
            
         
#api.add_resource(uRES, '/', '/update/<int:id>')

@res.before_first_request
def table():
    db.create_all()


if __name__ == '__main__':
    res.run('127.0.0.1',5000, debug = True)
