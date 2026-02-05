from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class User(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    folders = db.relationship('Folder', backref='owner', lazy=True)
    files = db.relationship('File', backref='owner', lazy=True)
    # shares = db.relationship('Share', backref='owner', lazy=True)
    # profile_picture = db.Column(db.String(150), nullable=True, default='default.jpg') 
    # subscription_type = db.Column(db.String(50), nullable=True, default='free_tier')
    def __repr__(self):
        return f"<User {self.username}>"

    def is_active(self):
        return True 

    def is_authenticated(self):
        return True if self.username else False 

    def is_anonymous(self):
        return False  

    def get_id(self):
        return str(self.id)
class subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active') 

    def __repr__(self):
        return f"<Subscription {self.plan_name} for User {self.user_id}>"
    
class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=True)  #self_reference_for_subfolders
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    files = db.relationship('File', backref='folder', lazy=True , cascade="all, delete-orphan")
    subfolders = db.relationship('Folder', backref=db.backref('parent_folder', remote_side=[id]), lazy=True , cascade="all, delete-orphan")

    def _repr_(self):
        return f"<Folder {self.name} (User {self.user_id})>"
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    path = db.Column(db.String(255), nullable=False)  
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id' , ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_metadata = db.Column(db.JSON)  

    def __repr__(self):
        return f"<File {self.filename}>"

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"<Share {self.token}>"