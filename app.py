from flask import Flask, request, redirect, url_for, render_template, jsonify, session , send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
from werkzeug.utils import secure_filename
import os
import uuid
from models import db, User, File, Share
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

#allowed_extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf', 'doc', 'docx', 'zip', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

#user_Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #if_user_already_exists
        if User.query.filter_by(username=username).first():
            return 'User already exists!', 400

        #create_a_new_user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        #new_folder_for_user
        user_folder_path = os.path.join(Config.NAS_DIRECTORY, username)
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', files=files)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_folder = os.path.join(Config.NAS_DIRECTORY, current_user.username)
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)

        #file_metadata_save  
        new_file = File(filename=filename, path=file_path, user_id=current_user.id, file_metadata={})
        db.session.add(new_file)
        db.session.commit()

        return redirect(url_for('dashboard'))

@app.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id:
        directory = os.path.dirname(file.path)  #directory ka name extract krne ke liye
        filename = os.path.basename(file.path)  #filename extract krne ke liye
        try:
            return send_from_directory(directory, filename, as_attachment=True)
        except FileNotFoundError:
            return 'File not found', 404
    return 'Unauthorized access', 403

@app.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id:
        os.remove(file.path)
        db.session.delete(file)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return 'File not found', 404

@app.route('/share/<int:file_id>', methods=['GET'])
@login_required
def share_file(file_id):
    file = File.query.get(file_id)
    if not file or file.user_id != current_user.id:
        return 'File not found', 404

    if request.method == 'GET':
        #token_Generation
        token = str(uuid.uuid4())
        new_share = Share(file_id=file.id, token=token, user_id=current_user.id)
        db.session.add(new_share)
        db.session.commit()

        shareable_link = url_for('shared_file', token=token, _external=True)

        return jsonify({'token': token, 'link': shareable_link})

@app.route('/shared/<token>')
def shared_file(token):
    share = Share.query.filter_by(token=token).first()
    if share:
        file = File.query.get(share.file_id)
        if file:
            directory = os.path.dirname(file.path)  #directory ka name extract krne ke liye
            filename = os.path.basename(file.path)  #filename extract krne ke liye
            return send_from_directory(directory, filename, as_attachment=True)
    return 'Shared file not found', 404

if __name__ == '__main__':
    app.run(debug=True)