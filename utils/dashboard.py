from flask import Flask, render_template, jsonify, request
from threading import Thread
import logging

logger = logging.getLogger(__name__)

class Dashboard:
    """Web dashboard for monitoring"""

    def __init__(self, controller, port: int = 5000):
        self.controller = controller
        self.port = port
        self.app = Flask(__name__,
                        template_folder='../templates',
                        static_folder='../static')
        self._setup_routes()

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route('/')
        def index():
            return render_template('dashboard.html')

        @self.app.route('/api/stats')
        def get_stats():
            return jsonify(self.controller.get_system_stats())

        @self.app.route('/api/refresh/<int:driver_id>', methods=['POST'])
        def refresh_driver(driver_id):
            for driver in self.controller.drivers:
                if driver.driver_id == driver_id:
                    success = driver.refresh()
                    return jsonify({'success': success})
            return jsonify({'success': False, 'error': 'Driver not found'}), 404

    def run(self):
        """Run dashboard server"""
        logger.info(f"Dashboard starting on http://localhost:{self.port}")
        self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)


