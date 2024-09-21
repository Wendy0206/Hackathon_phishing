from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    role = db.Column(db.String(40), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.fullname

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
             "fullname": self.fullname,
                 "role": self.role
            # do not serialize the password, its a security breach
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return self.Name
    def serialize(self):
        return {
            "id": self.id,
            "Name": self.Name
            # do not serialize the password, its a security breach
        }


class Email_template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), unique=True, nullable=False)
    name= db.Column(db.String(120), unique=True, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)    
    category_link = db.relationship('Category')
    def __repr__(self):
        return self.template

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "name": self.name,
             "category_id": self.category_id
            # do not serialize the password, its a security breach
        }
    

class Exam_session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, unique=True, nullable=False)
    date = db.Column(db.String(120), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    
    employee_link = db.relationship('User')
    def __repr__(self):
        return self.id

    def serialize(self):
        return {
            "id": self.id,
            "score": self.score,
             "date": self.date,
             "employee_id": self.employee_id
            # do not serialize the password, its a security breach
        }