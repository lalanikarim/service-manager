from flask import Flask, render_template, jsonify, request
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

SERVICES = os.getenv('SERVICES', '').split(',')
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 5000))

def run_systemctl_command(command, service):
    try:
        result = subprocess.run(['systemctl', '--user', command, service], 
                                capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def get_service_info(service):
    _, name = run_systemctl_command('show', f'{service} --property=Description')
    _, description = run_systemctl_command('show', f'{service} --property=Description')
    return {
        'name': name.split('=')[-1] if '=' in name else service,
        'description': description.split('=')[-1] if '=' in description else 'No description available'
    }

@app.route('/')
def home():
    service_info = [get_service_info(service) for service in SERVICES]
    return render_template('index.html', services=service_info)

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
    app.run(host=HOST, port=PORT, debug=True)