from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class User(UserMixin, db.Model):  # Inherit from UserMixin for Flask-Login
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    files = db.relationship('File', backref='owner', lazy=True)

    def _repr_(self):
        return f"<User {self.username}>"

    # Flask-Login required methods:
    def is_active(self):
        """Returns True if the user is active (can be customized)."""
        return True  # Assuming all users are active in this example.

    def is_authenticated(self):
        """Returns True if the user is authenticated (logged in)."""
        return True if self.username else False  # Basic check for this example.

    def is_anonymous(self):
        """Returns False if the user is authenticated (logged in)."""
        return False  # Only authenticated users are considered (you can modify for anonymous use).

    def get_id(self):
        """Returns the unique ID for the user."""
        return str(self.id)  # Flask-Login needs this to manage user sessions.


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    path = db.Column(db.String(255), nullable=False)  # File storage path on NAS
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_metadata = db.Column(db.JSON)  # Stores file metadata

    def __repr__(self):
        return f"<File {self.filename}>"

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"<Share {self.token}>"