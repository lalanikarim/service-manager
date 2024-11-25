from flask import Flask, render_template, jsonify, request
import subprocess
from dotenv import load_dotenv
import os
import uvicorn
from asgiref.wsgi import WsgiToAsgi

load_dotenv()

app = Flask(__name__)

SERVICES = os.getenv('SERVICES', '').split(',')
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 5000))

def run_systemctl_command(command, service, *args):
    try:
        cmd = ['systemctl', '--user', command, service] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def get_service_description(service):
    success, description = run_systemctl_command('show', service, '--property=Description')
    if success:
        return description.split('=', 1)[-1].strip()
    return 'No description available'

@app.route('/')
def home():
    service_info = [(service, get_service_description(service)) for service in SERVICES]
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

@app.route('/restart/<service>')
def restart_service(service):
    success, message = run_systemctl_command('restart', service)
    return jsonify({'success': success, 'message': message})

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    uvicorn.run(asgi_app, host=HOST, port=PORT)
