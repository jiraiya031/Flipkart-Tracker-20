from flask import Flask, send_file

app = Flask(__name__)

@app.route('/download')
def download_file():
    # Replace `path/to/your/file` with the actual file path on your server
    return send_file('Prie_Tracker.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run()
