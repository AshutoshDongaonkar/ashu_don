import logging
from datetime import datetime
import pytz
import os
from flask import Flask, request, jsonify
from config import Config
from models import db, DataRecord

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Set up logging
logging.basicConfig(filename=Config.LOGGING_FILE, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
timezone = pytz.timezone(Config.TIMEZONE)

def log_error(error_message):
    now = datetime.now(timezone)
    logging.error(f"{now} - {error_message}")

@app.route('/api', methods=['GET'])
def get_parameters():
    try:
        record = DataRecord.query.first()  # Adjust query to get appropriate record(s)
        if record:
            return jsonify({
                'param1': record.param1,
                'param2': record.param2,
                'param3': record.param3,
                'param4': record.param4,
                'param5': record.param5
            })
        return jsonify({'message': 'No data found'}), 404
    except Exception as e:
        log_error(f"Error in /api endpoint: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/web', methods=['POST'])
def update_or_create_record():
    try:
        data = request.json
        if not all(key in data for key in ['param1', 'param2', 'param3', 'param4', 'param5']):
            return jsonify({'error': 'Invalid input'}), 400

        existing_record = DataRecord.query.filter_by(
            param1=data['param1'],
            param2=data['param2'],
            param3=data['param3']
        ).first()

        if existing_record:
            return jsonify({'message': 'Record already exists'}), 200

        new_record = DataRecord(
            param1=data['param1'],
            param2=data['param2'],
            param3=data['param3'],
            param4=data['param4'],
            param5=data['param5']
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Record created'}), 201
    except Exception as e:
        log_error(f"Error in /web endpoint: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        log_error(f"Error in /upload endpoint: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
