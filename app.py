from flask import Flask, render_template, jsonify, request
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

SERVICES = os.getenv('SERVICES', '').split(',')

def run_systemctl_command(command, service):
    try:
        result = subprocess.run(['systemctl', '--user', command, service], 
                                capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

@app.route('/')
def home():
    return render_template('index.html', services=SERVICES)

@app.route('/start/<service>')
def start_service(service):
    success, message = run_systemctl_command('start', service)
    return jsonify({'success': success, 'message': message})

@app.route('/stop/<service>')
def stop_service(service):
    success, message = run_systemctl_command('stop', service)
    return jsonify({'success': success, 'message': message})

@app.route('/status/<service>')
def service_status(service):
    success, message = run_systemctl_command('is-active', service)
    status = 'active' if success else 'inactive'
    return jsonify({'status': status, 'message': message})

if __name__ == '__main__':
    app.run(debug=True)