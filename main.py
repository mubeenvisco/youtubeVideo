from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils.config_loader import load_config_file, SystemConfig
from utils.logger import setup_logging
from utils.system_controller import SystemController
from threading import Thread
import logging

app = Flask(__name__, template_folder='templates', static_folder='static')
logger = setup_logging()

# Global variables for controller and thread
controller = None
automation_thread = None

@app.route('/')
def index():
    """Render configuration form"""
    return render_template('config.html')

@app.route('/start', methods=['POST'])
def start():
    """Start automation with provided config"""
    global controller, automation_thread

    # If automation is running, stop it first
    if controller and controller.running:
        logger.info("Stopping existing automation before starting new one")
        controller.shutdown()
        controller = None
        automation_thread = None

    url = request.form.get('url')
    num_drivers = int(request.form.get('num_drivers'))
    headless = request.form.get('headless') == 'true'
    enable_dashboard = request.form.get('enable_dashboard') == 'true'

    config = load_config_file()
    config.headless = headless
    config.enable_dashboard = enable_dashboard

    try:
        controller = SystemController(url, num_drivers, config)
        controller.initialize_drivers()

        # Start automation in background thread
        automation_thread = Thread(target=controller.run, daemon=True)
        automation_thread.start()

        return redirect(url_for('dashboard'))
    except Exception as e:
        logger.error(f"Failed to start automation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop():
    """Stop automation"""
    global controller, automation_thread

    if controller:
        controller.shutdown()
        controller = None
        automation_thread = None

    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Render dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    if controller:
        return jsonify(controller.get_system_stats())
    else:
        return jsonify({'error': 'No active automation'}), 404

@app.route('/api/refresh/<int:driver_id>', methods=['POST'])
def refresh_driver(driver_id):
    """Refresh specific driver"""
    if not controller:
        return jsonify({'success': False, 'error': 'No active automation'}), 404

    for driver in controller.drivers:
        if driver.driver_id == driver_id:
            success = driver.refresh()
            return jsonify({'success': success})

    return jsonify({'success': False, 'error': 'Driver not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
