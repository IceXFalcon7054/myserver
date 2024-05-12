import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory

app = Flask(__name__)

# Define the folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_folders_and_files(folder_path):
    folders = []
    files = []
    for name in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, name)):
            folders.append(name)
        else:
            files.append(name)
    return folders, files

@app.route('/')
def index():
    # Get list of existing folders in the UPLOAD_FOLDER directory
    folders = [name for name in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], name))]
    # Create a dictionary to store files for each folder
    folder_files = {}
    for folder in folders:
        folder_files[folder] = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], folder))
    return render_template('myserver.html', folders=folders, folder_files=folder_files)

@app.route('/uploads')
def uploads():
    # Get list of all uploaded files
    files = [file for file in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], file))]
    return render_template('uploads.html', files=files)

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form['folder_name']
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    # Get the folder name from the request
    folder_name = request.form.get('folder_name', '')
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)

    # Save the file to the specified folder
    file.save(os.path.join(folder_path, file.filename))

    # Redirect to the root URL with a query parameter indicating success
    return redirect(url_for('index'))

@app.route('/downloads/<folder>/<filename>')
def download_file(folder, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
