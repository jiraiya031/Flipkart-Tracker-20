from flask import Flask, request, jsonify, send_file
import os
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    # Get a list of uploaded files and their URLs
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    urls = [f'http://flipkart-tracker-20.jiraiya31.repl.co/uploads/{filename}' for filename in files]
    return jsonify({'files': files, 'urls': urls})
print("test")
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['Price_Tracker.xlsx']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print("uploaded")
    return jsonify({'message': f'File {filename} uploaded successfully'})

@app.route('/download')
def download_file():
    # Replace `path/to/your/file` with the actual file path on your server
    return send_file('Price_Tracker.xlsx', as_attachment=True)

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    app.config['UPLOAD_FOLDER'] = './uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    t = Thread(target=run)
    t.start()
