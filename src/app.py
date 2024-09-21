"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Email_template, Management


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



# @app.route('/employee/login/', methods=['post'])
# def post_employee_login():
#     request_body=request.json
#     print(request_body)
#     response_body =True
#     return jsonify(response_body), 200



@app.route('/employee/login', methods=['POST'])
def login_test():
        request_body=request.json
        
        test_user= Management.query.filter_by(email=request_body['username']).first()
        test=False 
        if test_user is None:
           return jsonify(test)
           
        
        test_password= Management.query.filter_by(email=request_body['username']).first().password
        #test_name= User.query.filter_by(email=request_body[0]).first().fullname
    
        if str(test_password)==request_body['password']:  
                test=True          
                return jsonify(test)


# @app.route('/email/new', methods=['POST'])
# def add_newEmail():
#         request_body=request.json  
#         test_email= Exam_session.query.filter_by(id=request_body['id']).first()
#         test=False 
#         if test_email is None:
#             newExam=Exam_session (name= request_body['name'], content= request_body['content'], Category=request_body['1'])
#             db.session.add(newExam)
#             db.session.commit()
#             return jsonify(f"Success"), 200 
#         else:     
#              return jsonify(test), 450 #it exist already



# @app.route('/exam/new', methods=['POST'])
# def add_newExam():
#         request_body=request.json  
#         test_user= User.query.filter_by(id=request_body['id']).first()
#         if(test_user):
#             newExam=Exam_session ( date=request_body['date'], score=request_body['score'],employee_id= request_body['employee_id'])
#             db.session.add(newExam)
#             db.session.commit()
#             return jsonify(f"Success"), 200      


# to list every record in our database

# @app.route('/exam/all', methods=['GET'])
# def get_all_exam():

#     all_exam= Exam_session.query.all()
#     final= list(map(lambda x: x.serialize(), all_exam))
   
#     return  jsonify(final)
        
@app.route('/email/all', methods=['GET'])
def get_all_email():

    all_email= Email_template.query.all()
    final= list(map(lambda x: x.serialize(), all_email))
   
    return  jsonify(final)

@app.route('/email/edit/id', methods=['post'])
def update_email():
    request_body=request.json 
    db.session.query(Email_template).filter_by(id=request_body['templateId']).update({"content":request_body['content']})
    db.session.commit()  

    all_email= Email_template.query.all()
    final= list(map(lambda x: x.serialize(), all_email))
   
    return  jsonify(final)

        
@app.route('/user/all/', methods=['GET'])
def get_all_user(): 
    all_user= User.query.filter_by(is_active=True).all()
    final= list(map(lambda x: x.serialize(), all_user))
   
    return  jsonify(final)


# @app.route('/user/get/id', methods=['GET'])
# def get_this_user():
#     print('hey! someone click on that linkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
#     all_user= User.query.filter_by(is_active=True).all()
#     final= list(map(lambda x: x.serialize(), all_user))
   
#     return  jsonify(final)

@app.route('/user/delete/id', methods=['post'])
def update_user():
    request_body=request.json 
    db.session.query(User).filter_by(email=request_body['email']).update({"is_active":False})
    db.session.commit()      

    get_User= User.query.filter_by(is_active=True).all()
    final= list(map(lambda x: x.serialize(), get_User))
   
    return  jsonify(final),200


@app.route('/user/add/new', methods=['post'])
def add_user():
     request_body=request.json 
     test_user= User.query.filter_by(email=request_body['email']).first()
     if(test_user):
        db.session.query(User).filter_by(email=request_body['email']).update({"is_active":True})
        db.session.commit()  
    
     else:
        newU=User(email=request_body['email'])
        db.session.add(newU)
        db.session.commit()
     all_user= User.query.filter_by(is_active=True).all()
     final= list(map(lambda x: x.serialize(), all_user))
     return  jsonify(final)
       
  

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
