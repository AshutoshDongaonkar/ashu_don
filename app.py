import logging
from datetime import datetime
from pathlib import Path
import json
import pytz
import os
from flask import Flask, request, jsonify, send_file, make_response
from config import Config
from models import db, ClientRecord
from models import db, GetApi
from models import db, ReportException

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

@app.route('/api/parameters', methods=['POST'])
def get_parameters():
    try:
        data = request.json
        if not all(key in data for key in ['param1', 'param2']):
            return jsonify({'error': 'Invalid input'}), 400
                
         #record = GetApi.query.first()  # Adjust query to get appropriate record(s)
        record = GetApi.query.filter_by(
            param6= 'active',
            param7=data['param1'],
            param8=data['param2']
        ).first()
        
        if record:
            return jsonify({
                'command': record.param1,
                'path': record.param2,
                'filename': record.param3,
                'timetoexecute': record.param4,
                'gotosleep': record.param5
            })
        log_error(f"GetApi has no active record for: {data['param1']} & {data['param2']} ")    
        return jsonify({'message': 'No data found'}), 404
    except Exception as e:
        #log_error(f"Error in /api endpoint: {str(e)}")
        log_error("Error in /api endpoint for " + data['param1'] + "_" + data['param2'] + ": " + str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
  
@app.route('/status', methods=['POST'])
def set_status():
    try:
        data = request.json
        if not all(key in data for key in ['param1', 'param2', 'param3']):
            return jsonify({'error': 'Invalid input'}), 400
            
        
        #record = GetApi.query.first()  # Adjust query to get appropriate record(s)
        record = GetApi.query.filter_by(
            param6='active',
            param7=data['param1'],
            param8=data['param2']
        ).first()
        
        if record:
            record.param6='inactive'
            record.param9=data['param3']
            db.session.commit()
            return jsonify({'message': 'Operation Succeful'}), 200
            
        log_error(f"Unable to mark operation completion for: {data['param1']} & {data['param2']} ")    
        return jsonify({'message': 'Unable to mark operation completion'}), 404
    except Exception as e:
        #log_error(f"Error in /status endpoint: {str(e)}")
        log_error("Error in /status endpoint " + data['param1'] + "_" + data['param2'] + ": " + str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
 
        
@app.route('/download', methods=['POST'])
def download_file():
    try:
    	
        data = request.json
        if not all(key in data for key in ['param1', 'param2']):
            return jsonify({'error': 'Invalid input'}), 400
                
        record = GetApi.query.filter_by(
            param6='active',
            param7=data['param1'],
            param8=data['param2']
        ).first()
    	#record = GetApi.query.first()  # Adjust query to get appropriate record(s)
    	# Path to the file you want to make available for download
        if not record:
    	    log_error(f"GETApi has no active file to upload for: {data['param1']} & {data['param2']}  ")
    	    return make_response('File not found', 404)
    	    
    	    
        file_path = '/var/www/flaskMSPS/payload/' + record.param3
        
        #'record.param6='inactive'
        #'db.session.commit()
    	
        if not os.path.exists(file_path):
    	    
    	    return make_response('File not found', 404)
    
    	# Send the file to the client
        return send_file(file_path, as_attachment=True)    	
    except Exception as e:
        #log_error(f"Error in /web endpoint: {str(e)}")
        log_error("Error in /download endpoint for " + data['param1'] + "_" + data['param2'] + ": " + str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/getfile', methods=['GET'])        # this method is for BAT and VBscript to direct download
def getfile():
    try:
    	    
        file_path = '/var/www/flaskMSPS/payload/MSPS.exe'
                
    	# Send the file to the client
        return send_file(file_path, as_attachment=True)    	
    except Exception as e:
        #log_error(f"Error in /web endpoint: {str(e)}")
        log_error("Error in /download endpoint for " + data['param1'] + "_" + data['param2'] + ": " + str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


	
@app.route('/web', methods=['POST'])
def update_or_create_record():
    try:
        data = request.json
        if not all(key in data for key in ['param1', 'param2', 'param3', 'param4', 'param5']):
            return jsonify({'error': 'Invalid input'}), 400

        existing_record = ClientRecord.query.filter_by(
            param1=data['param1'],
            param2=data['param2'],
            param3=data['param3']
        ).first()

        if existing_record:
            return jsonify({'message': 'Record already exists'}), 200

        Client_record = ClientRecord(
            param1=data['param1'],      # IP address
            param2=data['param2'],      # machine name
            param3=data['param3'],      # user name
            param4=data['param4'],      # system information
            param5=data['param5']       # date & time stamp
        )
        # add a new record to GetApi table. this record will identify the target machine when it makes a API call
        GetApi_record = GetApi(
            param1= '20',
            param2= 'C:\MSP\config.json',
            param3= 'config.json',
            param4= '',
            param5= '',
            param6= 'active',      # 'active'/'inactive' status
            param7=data['param2'],      # machine name
            param8=data['param3']       # user name, together with machine name forms the foreign key on this table
        )
        
        
        db.session.add(Client_record)
        db.session.add(GetApi_record)
        db.session.commit()
        return jsonify({'message': 'Record created'}), 201
    except Exception as e:
        #log_error(f"Error in /web endpoint for {data['param1']} & {data['param2']} : {str(e)}")
        log_error("Error in /web endpoint for " + + data['param1'] + "_" + data['param2'] + ": " + str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/reportexception', methods=['POST'])
def reportexception():
    try:
        data = request.json
        if not all(key in data for key in ['param1', 'param2', 'param3', 'param4', 'param5','param6']):
            return jsonify({'error': 'Invalid input'}), 400

        new_record = ReportException(
            param1=data['param1'],    # Error message
            param2=data['param2'],    # Date & time stamp
            param3=data['param3'],    # IP Address
            param4=data['param4'],    # Machine name
            param5=data['param5'],    # User Name
            param6=data['param6']     # System Information
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Record created'}), 201
    except Exception as e:
        #log_error(f"Error in /web endpoint for {data['param1']} & {data['param2']} : {str(e)}")
        log_error("Error in /web endpoint " + data['param1'] + "_" + data['param2'] + ": " + str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        param1 = request.form.get('param1')
        param2 = request.form.get('param2')
        
        if not param1 or not param2:
            return jsonify({'error': 'Invalid input'}), 400
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        #create a folder machine_user if it is not available alread
        path = '/var/www/flaskMSPS/uploads/' + param1 + '_' + param2
        user_dir = Path(path)
        if not user_dir.exists():
            try: 
                user_dir.mkdir(parents=True, exist_ok=True)
                log_error("Successfully created user dir: " + path)
            except Exception as e2:
                log_error(f"Unable to create user dir for {data['param1']} & {data['param2']} : {str(e2)}")
               
        file_path = os.path.join(user_dir, file.filename)
        file.save(file_path)

        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        #log_error(f"Error in /upload endpoint: {str(e)}")
        log_error("Error in /upload endpoint for " + param1 + "_" + param2 + ": " + str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=False)
