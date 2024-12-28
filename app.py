from flask import Flask, request, redirect, url_for, render_template, jsonify, session , send_from_directory , flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
from werkzeug.utils import secure_filename
import os
import uuid
from models import db, User, Folder, File, Share
from config import Config 
import datetime
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

#allowed_extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf', 'doc', 'docx', 'zip', 'mkv' ,'mp3' ,'mp4', 'tsx', 'csv', 'xlsx', 'pptx', 'ppt', 'html', 'css', 'js', 'py', 'java','apk','dmg', 'c', 'cpp', 'php', 'sql', 'json', 'xml', 'yaml', 'yml', 'md', 'log', 'sh', 'bat', 'ps1', 'psm1', 'psd1', 'ps1xml', 'pssc', 'reg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/profile')
@login_required
def profile():
    #all_Folders
    folder_count = Folder.query.filter_by(user_id=current_user.id).count()
    
    #all_Files
    files = File.query.filter_by(user_id=current_user.id).all()
    file_count = len(files)
    
    #calculate_Total_storage
    total_size = 0
    for file in files:
        try:
            if file.path and os.path.exists(file.path):
                total_size += os.path.getsize(file.path)
        except (OSError, FileNotFoundError):
            continue
    
    #file_types
    file_types = {}
    for file in files:
        if file.file_metadata is not None:
            file_type = file.file_metadata.get('type', 'unknown')
            file_types[file_type] = file_types.get(file_type, 0) + 1
    
    #recent_files
    recent_files = File.query.filter_by(user_id=current_user.id)\
        .filter(File.file_metadata.isnot(None))\
        .order_by(File.id.desc())\
        .limit(5)\
        .all()
    
    #storage_limit
    storage_limit = 10 * 1024 * 1024 * 1024  #10GB
    
    return render_template('profile.html',
                         folder_count=folder_count,
                         file_count=file_count,
                         total_size=total_size,
                         storage_limit=storage_limit,
                         file_types=file_types,
                         recent_files=recent_files)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/folder/create/<int:parent_folder_id>', methods=['GET', 'POST'])
@login_required
def create_folder(parent_folder_id=0):
    if parent_folder_id == 0:
        parent_folder = None
    else:
        parent_folder = Folder.query.get_or_404(parent_folder_id)
        if parent_folder.user_id != current_user.id:
            flash("You don't have permission to create a folder here.", 'danger')
            return redirect(url_for('dashboard'))

    if request.method == 'POST':
        folder_name = request.form['folder_name']
        
        existing_folder = Folder.query.filter_by(name=folder_name, parent_id=parent_folder.id if parent_folder else 0, user_id=current_user.id).first()
        if existing_folder:
            return jsonify({"error": "A folder with this name already exists"}), 400

        new_folder = Folder(
            name=folder_name,
            parent_id=parent_folder.id if parent_folder else 0, 
            user_id=current_user.id
        )
        db.session.add(new_folder)
        db.session.commit()

        return jsonify({"success": True, "redirect": url_for('view_folder', folder_id=new_folder.id)})

    return render_template('create_folder.html', parent_folder=parent_folder)

@app.route('/folder/view/<int:folder_id>', methods=['GET'])
@login_required
def view_folder(folder_id):
    folder = Folder.query.get(folder_id)
    
    if not folder or folder.user_id != current_user.id:
        flash("You don't have permission to view this folder.", 'danger')
        return redirect(url_for('dashboard'))

    return render_template('view_folder.html', folder=folder)

@app.route('/dashboard')
@login_required
def dashboard():
    folders = Folder.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', folders=folders)

@app.route('/upload/<int:folder_id>', methods=['POST'])
@login_required
def upload_file(folder_id):
    folder = Folder.query.get(folder_id)

    if not folder or folder.user_id != current_user.id:
        return jsonify({"error": "Permission denied"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        #folder_already_exists
        existing_file = File.query.filter_by(
            filename=filename,
            folder_id=folder.id,
            user_id=current_user.id
        ).first()
        
        if existing_file:
            return jsonify({"error": "File already exists"}), 409  

        folder_path = os.path.join(Config.NAS_DIRECTORY, current_user.username, str(folder.id))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, filename)
        file.save(file_path)

        file_metadata = {
            'size': os.path.getsize(file_path),
            'filename': filename,
            'type': file.content_type,
            'upload_date': str(datetime.datetime.now())
        }

        new_file = File(
            filename=filename,
            path=file_path,
            user_id=current_user.id,
            folder_id=folder.id,
            metadata=file_metadata
        )
        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"error": "Invalid file type"}), 400

@app.route('/files')
@login_required
def list_files():
    files = File.query.filter_by(user_id=current_user.id).all()
    return render_template('files.html', files=files)

@app.route('/folder/delete/<int:folder_id>', methods=['POST'])
@login_required
def delete_folder(folder_id):
    folder = Folder.query.get(folder_id)

    #check_folder_owner
    if folder.user_id != current_user.id:
        flash("You don't have permission to delete this folder.", 'danger')
        return redirect(url_for('dashboard'))

    #delete_folder
    db.session.delete(folder)
    db.session.commit()

    flash("Folder deleted successfully!", 'success')
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
        return redirect(url_for('view_folder', folder_id=file.folder_id))
    return 'File not found', 404

@app.route('/delete_in_all_files/<int:file_id>')
@login_required
def delete_in_all_files(file_id):
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id:
        os.remove(file.path)
        db.session.delete(file)
        db.session.commit()
        return redirect(url_for('list_files', folder_id=file.folder_id))
    return 'File not found', 404

@app.route('/share/<int:file_id>', methods=['GET'])
@login_required
def share_file(file_id):
    file = File.query.get(file_id)
    if not file or file.user_id != current_user.id:
        return 'File not found', 404

    if request.method == 'GET':
        #generate_share_link
        token = str(uuid.uuid4())
        new_share = Share(file_id=file.id, token=token, user_id=current_user.id)
        db.session.add(new_share)
        db.session.commit()

        shareable_link = url_for('shared_file', token=token, _external=True)

        return render_template('share_file.html', link=shareable_link)

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