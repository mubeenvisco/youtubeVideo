from .driver_manager import DriverManager
from threading import Lock
from datetime import datetime
from typing import List
import time
import random
import logging
import os

logger = logging.getLogger(__name__)

class SystemController:
    """Main controller for the automation system"""

    def __init__(self, url: str, num_drivers: int, config):
        self.url = url
        self.num_drivers = num_drivers
        self.config = config
        self.drivers: List[DriverManager] = []
        self.running = False
        self.stats_lock = Lock()
        self.start_time = datetime.now()

    def initialize_drivers(self):
        """Initialize all drivers"""
        logger.info(f"Initializing {self.num_drivers} driver(s)...")

        proxies = self._get_proxy_list() if self.config.use_proxy else [None] * self.num_drivers

        for i in range(self.num_drivers):
            proxy = proxies[i % len(proxies)] if proxies else None
            driver_manager = DriverManager(i + 1, self.url, self.config)
            driver_manager.set_proxy(proxy)

            if driver_manager.initialize():
                self.drivers.append(driver_manager)

            time.sleep(random.uniform(self.config.min_delay, self.config.max_delay))

        if not self.drivers:
            raise Exception("No drivers initialized successfully")

        logger.info(f"Successfully initialized {len(self.drivers)}/{self.num_drivers} driver(s)")

    def _get_proxy_list(self) -> List[str]:
        """Load proxy list from config"""
        if self.config.proxy_list:
            return self.config.proxy_list

        # Try loading from file
        if os.path.exists('proxies.txt'):
            with open('proxies.txt', 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
                logger.info(f"Loaded {len(proxies)} proxies from proxies.txt")
                return proxies

        return []

    def run(self):
        """Main run loop"""
        self.running = True
        refresh_count = 0

        logger.info("="*60)
        logger.info(f"System running with {len(self.drivers)} driver(s)")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*60)

        try:
            while self.running:
                time.sleep(self.config.refresh_interval)
                refresh_count += 1

                logger.info(f"\n{'='*60}")
                logger.info(f"Refresh Cycle #{refresh_count}")
                logger.info(f"{'='*60}")

                for driver in self.drivers:
                    driver.refresh()
                    time.sleep(random.uniform(self.config.min_delay, self.config.max_delay))

                # Update all stats
                self._update_all_stats()

        except KeyboardInterrupt:
            logger.info("\nShutdown signal received...")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            self.shutdown()

    def _update_all_stats(self):
        """Update statistics for all drivers"""
        with self.stats_lock:
            for driver in self.drivers:
                driver.update_stats()

    def get_system_stats(self) -> dict:
        """Get overall system statistics"""
        with self.stats_lock:
            total_refreshes = sum(d.stats.refresh_count for d in self.drivers)
            total_errors = sum(d.stats.error_count for d in self.drivers)
            active_drivers = sum(1 for d in self.drivers if d.stats.status == 'running')

            uptime = datetime.now() - self.start_time

            return {
                'uptime': str(uptime).split('.')[0],
                'active_drivers': active_drivers,
                'total_drivers': len(self.drivers),
                'total_refreshes': total_refreshes,
                'total_errors': total_errors,
                'url': self.url,
                'drivers': [{
                    'driver_id': d.stats.driver_id,
                    'status': d.stats.status,
                    'is_playing': d.stats.is_playing,
                    'current_time': d.stats.current_time,
                    'duration': d.stats.duration,
                    'refresh_count': d.stats.refresh_count,
                    'error_count': d.stats.error_count,
                    'last_refresh': d.stats.last_refresh,
                    'uptime': d.stats.uptime,
                    'cpu_percent': d.stats.cpu_percent,
                    'memory_mb': d.stats.memory_mb
                } for d in self.drivers]
            }

    def shutdown(self):
        """Shutdown all drivers"""
        self.running = False
        logger.info("Shutting down all drivers...")

        for driver in self.drivers:
            driver.close()

        logger.info("System shutdown complete")
