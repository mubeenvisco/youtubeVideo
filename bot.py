# # from selenium import webdriver
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.common.action_chains import ActionChains
# # from selenium.webdriver.chrome.service import Service
# # from webdriver_manager.chrome import ChromeDriverManager
# # import time
# # import pandas as pd

# # URL = str(input("Enter the YouTube video URL: "))
# # DRIVIERS = int(input("Enter the number of drivers to use: "))
# # driver =[]
# # BreakRate = 5

# # for i in range(DRIVIERS):
# #     service = Service(ChromeDriverManager().install())
# #     driver.append(webdriver.Chrome(service=service))
# #     driver[i].get(URL)
# #     action = ActionChains(driver[i])
# #     action.send_keys(Keys.SPACE).perform()
# #     time.sleep(BreakRate)
# #     print(f"Driver {i+1} started and video playing.")

# # while True:
# #     time.sleep(60)
# #     for i in range(DRIVIERS):
# #        driver[i].refresh()
# #        action = ActionChains(driver[i])
# #        action.send_keys(Keys.SPACE).perform()
# ################################################################second version with logging and error handling#####################################################################
# # from selenium import webdriver
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.common.action_chains import ActionChains
# # from selenium.webdriver.chrome.service import Service
# # from webdriver_manager.chrome import ChromeDriverManager
# # import time
# # import random
# # import logging
# # import json
# # import os
# # from datetime import datetime

# # # Configure logging
# # logging.basicConfig(
# #     level=logging.INFO,
# #     format='%(asctime)s - %(levelname)s - %(message)s',
# #     handlers=[
# #         logging.FileHandler(f'youtube_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
# #         logging.StreamHandler()
# #     ]
# # )
# # logger = logging.getLogger(__name__)

# # # Default configuration
# # DEFAULT_CONFIG = {
# #     "refresh_interval": 60,
# #     "break_rate": 5,
# #     "min_delay": 2,
# #     "max_delay": 5,
# #     "video_check_timeout": 10,
# #     "max_retry_attempts": 3
# # }

# # def load_config(config_file='config.json'):
# #     """Load configuration from file or create default"""
# #     if os.path.exists(config_file):
# #         try:
# #             with open(config_file, 'r') as f:
# #                 config = json.load(f)
# #                 logger.info(f"Configuration loaded from {config_file}")
# #                 return config
# #         except Exception as e:
# #             logger.warning(f"Error loading config file: {e}. Using defaults.")
# #             return DEFAULT_CONFIG
# #     else:
# #         # Create default config file
# #         with open(config_file, 'w') as f:
# #             json.dump(DEFAULT_CONFIG, f, indent=4)
# #         logger.info(f"Default configuration file created: {config_file}")
# #         return DEFAULT_CONFIG

# # def random_delay(min_delay, max_delay):
# #     """Add random delay to appear more natural"""
# #     delay = random.uniform(min_delay, max_delay)
# #     logger.debug(f"Random delay: {delay:.2f} seconds")
# #     time.sleep(delay)

# # def check_video_playing(driver):
# #     """Check if video is currently playing"""
# #     try:
# #         is_playing = driver.execute_script(
# #             "return document.querySelector('video') && "
# #             "!document.querySelector('video').paused && "
# #             "!document.querySelector('video').ended && "
# #             "document.querySelector('video').readyState > 2"
# #         )
# #         return is_playing
# #     except Exception as e:
# #         logger.error(f"Error checking video state: {e}")
# #         return False

# # def get_video_info(driver):
# #     """Get current video playback information"""
# #     try:
# #         video_info = driver.execute_script(
# #             "var video = document.querySelector('video');"
# #             "return video ? {"
# #             "  currentTime: video.currentTime,"
# #             "  duration: video.duration,"
# #             "  paused: video.paused,"
# #             "  ended: video.ended,"
# #             "  readyState: video.readyState"
# #             "} : null;"
# #         )
# #         return video_info
# #     except Exception as e:
# #         logger.error(f"Error getting video info: {e}")
# #         return None

# # def play_video(driver):
# #     """Attempt to play the video"""
# #     try:
# #         # First try using JavaScript
# #         driver.execute_script(
# #             "var video = document.querySelector('video');"
# #             "if(video) video.play();"
# #         )
# #         random_delay(0.5, 1.5)
        
# #         # Check if playing
# #         if not check_video_playing(driver):
# #             # Fallback to spacebar
# #             logger.info("Video not playing, trying spacebar...")
# #             action = ActionChains(driver)
# #             action.send_keys(Keys.SPACE).perform()
# #             random_delay(0.5, 1.5)
        
# #         return check_video_playing(driver)
# #     except Exception as e:
# #         logger.error(f"Error playing video: {e}")
# #         return False

# # def initialize_driver(url, driver_id, config):
# #     """Initialize a driver and start playing video"""
# #     attempt = 0
# #     max_attempts = config.get('max_retry_attempts', 3)
    
# #     while attempt < max_attempts:
# #         try:
# #             logger.info(f"Initializing driver {driver_id} (attempt {attempt + 1}/{max_attempts})")
# #             service = Service(ChromeDriverManager().install())
# #             driver = webdriver.Chrome(service=service)
# #             driver.get(url)
            
# #             # Wait for video element to load
# #             WebDriverWait(driver, config.get('video_check_timeout', 10)).until(
# #                 EC.presence_of_element_located((By.TAG_NAME, "video"))
# #             )
# #             logger.info(f"Driver {driver_id}: Video element loaded")
            
# #             random_delay(config.get('min_delay', 2), config.get('max_delay', 5))
            
# #             # Start playing video
# #             if play_video(driver):
# #                 logger.info(f"Driver {driver_id}: Video is playing")
# #                 video_info = get_video_info(driver)
# #                 if video_info:
# #                     logger.info(f"Driver {driver_id}: Video duration: {video_info.get('duration', 'N/A'):.2f}s")
                
# #                 time.sleep(config.get('break_rate', 5))
# #                 return driver
# #             else:
# #                 logger.warning(f"Driver {driver_id}: Video failed to play")
# #                 driver.quit()
# #                 attempt += 1
                
# #         except Exception as e:
# #             logger.error(f"Error initializing driver {driver_id}: {e}")
# #             attempt += 1
# #             if attempt < max_attempts:
# #                 logger.info(f"Retrying in 3 seconds...")
# #                 time.sleep(3)
    
# #     logger.error(f"Failed to initialize driver {driver_id} after {max_attempts} attempts")
# #     return None

# # def refresh_driver(driver, driver_id, url, config):
# #     """Refresh driver and restart video"""
# #     try:
# #         logger.info(f"Refreshing driver {driver_id}...")
# #         driver.refresh()
        
# #         # Wait for video element
# #         WebDriverWait(driver, config.get('video_check_timeout', 10)).until(
# #             EC.presence_of_element_located((By.TAG_NAME, "video"))
# #         )
        
# #         random_delay(config.get('min_delay', 2), config.get('max_delay', 5))
        
# #         # Play video
# #         if play_video(driver):
# #             logger.info(f"Driver {driver_id}: Successfully refreshed and playing")
# #             video_info = get_video_info(driver)
# #             if video_info:
# #                 logger.debug(f"Driver {driver_id}: Current time: {video_info.get('currentTime', 0):.2f}s")
# #             return True
# #         else:
# #             logger.warning(f"Driver {driver_id}: Video not playing after refresh")
# #             return False
            
# #     except Exception as e:
# #         logger.error(f"Error refreshing driver {driver_id}: {e}")
# #         return False

# # def cleanup_drivers(drivers):
# #     """Close all drivers"""
# #     logger.info("Cleaning up drivers...")
# #     for i, driver in enumerate(drivers):
# #         if driver:
# #             try:
# #                 driver.quit()
# #                 logger.info(f"Driver {i+1} closed")
# #             except Exception as e:
# #                 logger.error(f"Error closing driver {i+1}: {e}")

# # def main():
# #     # Load configuration
# #     config = load_config()
    
# #     # Get user input
# #     url = input("Enter the YouTube video URL: ")
# #     num_drivers = int(input("Enter the number of drivers to use: "))
    
# #     logger.info(f"Starting automation with {num_drivers} driver(s)")
# #     logger.info(f"Target URL: {url}")
# #     logger.info(f"Configuration: {json.dumps(config, indent=2)}")
    
# #     # Initialize drivers
# #     drivers = []
# #     for i in range(num_drivers):
# #         driver = initialize_driver(url, i+1, config)
# #         if driver:
# #             drivers.append(driver)
# #         random_delay(config.get('min_delay', 2), config.get('max_delay', 5))
    
# #     if not drivers:
# #         logger.error("No drivers were initialized successfully. Exiting.")
# #         return
    
# #     logger.info(f"{len(drivers)} driver(s) running successfully")
# #     print(f"\n{'='*50}")
# #     print(f"Running with {len(drivers)} driver(s). Press Ctrl+C to stop.")
# #     print(f"{'='*50}\n")
    
# #     # Main loop
# #     refresh_count = 0
# #     try:
# #         while True:
# #             # Wait for refresh interval
# #             time.sleep(config.get('refresh_interval', 60))
# #             refresh_count += 1
            
# #             logger.info(f"=== Refresh cycle {refresh_count} ===")
            
# #             # Check and refresh each driver
# #             for i, driver in enumerate(drivers):
# #                 # Check if video is still playing before refresh
# #                 is_playing = check_video_playing(driver)
# #                 logger.info(f"Driver {i+1}: Video playing status before refresh: {is_playing}")
                
# #                 # Add random delay between driver refreshes
# #                 if i > 0:
# #                     random_delay(config.get('min_delay', 2), config.get('max_delay', 5))
                
# #                 # Refresh the driver
# #                 success = refresh_driver(driver, i+1, url, config)
                
# #                 if not success:
# #                     logger.warning(f"Driver {i+1}: Refresh failed, attempting recovery...")
# #                     # Could add recovery logic here
            
# #             logger.info(f"Refresh cycle {refresh_count} completed\n")
    
# #     except KeyboardInterrupt:
# #         logger.info("\nKeyboard interrupt received. Stopping...")
# #     except Exception as e:
# #         logger.error(f"Unexpected error in main loop: {e}")
# #     finally:
# #         cleanup_drivers(drivers)
# #         logger.info("Automation stopped. All drivers closed.")

# # if __name__ == "__main__":
# #     try:
# #         main()
# #     except Exception as e:
# #         logger.critical(f"Critical error: {e}")
# #         print(f"\nCritical error occurred. Check log file for details.")

#     ################################################################################thrid version with GUI##########################################################################################

# """
# Enhanced YouTube Automation System
# Features: Web Dashboard, Advanced Monitoring, Proxy Support, Resource Optimization
# """

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from flask import Flask, render_template_string, jsonify, request
# from threading import Thread, Lock
# from dataclasses import dataclass, asdict
# from typing import List, Optional, Dict
# from datetime import datetime, timedelta
# import time
# import random
# import logging
# import json
# import os
# import psutil
# import signal
# import sys

# # ==================== Configuration ====================

# @dataclass
# class DriverStats:
#     """Statistics for individual driver"""
#     driver_id: int
#     status: str  # 'running', 'stopped', 'error', 'refreshing'
#     is_playing: bool
#     current_time: float
#     duration: float
#     refresh_count: int
#     error_count: int
#     last_refresh: str
#     uptime: str
#     cpu_percent: float
#     memory_mb: float

# @dataclass
# class SystemConfig:
#     """System configuration"""
#     refresh_interval: int = 60
#     min_delay: float = 2.0
#     max_delay: float = 5.0
#     video_check_timeout: int = 10
#     max_retry_attempts: int = 3
#     headless: bool = False
#     use_proxy: bool = False
#     proxy_list: List[str] = None
#     mute_audio: bool = True
#     quality: str = "720p"
#     enable_dashboard: bool = True
#     dashboard_port: int = 5000

# # ==================== Logging Setup ====================

# class ColoredFormatter(logging.Formatter):
#     """Custom colored formatter for console output"""
    
#     COLORS = {
#         'DEBUG': '\033[36m',    # Cyan
#         'INFO': '\033[32m',     # Green
#         'WARNING': '\033[33m',  # Yellow
#         'ERROR': '\033[31m',    # Red
#         'CRITICAL': '\033[35m', # Magenta
#         'RESET': '\033[0m'
#     }

#     def format(self, record):
#         log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
#         record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
#         return super().format(record)

# def setup_logging():
#     """Setup logging with file and console handlers"""
#     log_filename = f'youtube_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
#     # File handler
#     file_handler = logging.FileHandler(log_filename)
#     file_handler.setLevel(logging.DEBUG)
#     file_formatter = logging.Formatter(
#         '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
#     )
#     file_handler.setFormatter(file_formatter)
    
#     # Console handler with colors
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.INFO)
#     console_formatter = ColoredFormatter(
#         '%(asctime)s - %(levelname)s - %(message)s',
#         datefmt='%H:%M:%S'
#     )
#     console_handler.setFormatter(console_formatter)
    
#     # Root logger
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)
    
#     return logger

# logger = setup_logging()

# # ==================== Driver Manager ====================

# class DriverManager:
#     """Manages individual Chrome driver instances"""
    
#     def __init__(self, driver_id: int, url: str, config: SystemConfig, proxy: Optional[str] = None):
#         self.driver_id = driver_id
#         self.url = url
#         self.config = config
#         self.proxy = proxy
#         self.driver: Optional[webdriver.Chrome] = None
#         self.stats = DriverStats(
#             driver_id=driver_id,
#             status='initializing',
#             is_playing=False,
#             current_time=0.0,
#             duration=0.0,
#             refresh_count=0,
#             error_count=0,
#             last_refresh='Never',
#             uptime='0:00:00',
#             cpu_percent=0.0,
#             memory_mb=0.0
#         )
#         self.start_time = datetime.now()
#         self.process = None
        
#     def _create_driver(self) -> webdriver.Chrome:
#         """Create Chrome driver with options"""
#         chrome_options = Options()
        
#         if self.config.headless:
#             chrome_options.add_argument('--headless=new')
#             chrome_options.add_argument('--disable-gpu')
        
#         # Performance optimizations
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#         chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         chrome_options.add_experimental_option('useAutomationExtension', False)
        
#         # Mute audio
#         if self.config.mute_audio:
#             chrome_options.add_argument('--mute-audio')
        
#         # Proxy configuration
#         if self.proxy:
#             chrome_options.add_argument(f'--proxy-server={self.proxy}')
#             logger.info(f"Driver {self.driver_id}: Using proxy {self.proxy}")
        
#         # User agent
#         chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=chrome_options)
        
#         # Set quality preference
#         driver.execute_cdp_cmd('Network.enable', {})
        
#         return driver
    
#     def initialize(self) -> bool:
#         """Initialize driver and start video"""
#         for attempt in range(self.config.max_retry_attempts):
#             try:
#                 logger.info(f"Driver {self.driver_id}: Initializing (attempt {attempt + 1}/{self.config.max_retry_attempts})")
                
#                 self.driver = self._create_driver()
#                 self.driver.get(self.url)
                
#                 # Store process for monitoring
#                 try:
#                     self.process = psutil.Process(self.driver.service.process.pid)
#                 except:
#                     pass
                
#                 # Wait for video element
#                 WebDriverWait(self.driver, self.config.video_check_timeout).until(
#                     EC.presence_of_element_located((By.TAG_NAME, "video"))
#                 )
                
#                 time.sleep(random.uniform(self.config.min_delay, self.config.max_delay))
                
#                 # Set quality if possible
#                 self._set_quality()
                
#                 # Start playing
#                 if self._play_video():
#                     self.stats.status = 'running'
#                     self._update_video_info()
#                     logger.info(f"Driver {self.driver_id}: Successfully initialized")
#                     return True
#                 else:
#                     self.driver.quit()
#                     self.stats.error_count += 1
                    
#             except Exception as e:
#                 logger.error(f"Driver {self.driver_id}: Initialization error: {e}")
#                 self.stats.error_count += 1
#                 if self.driver:
#                     try:
#                         self.driver.quit()
#                     except:
#                         pass
                
#                 if attempt < self.config.max_retry_attempts - 1:
#                     time.sleep(3)
        
#         self.stats.status = 'error'
#         logger.error(f"Driver {self.driver_id}: Failed to initialize")
#         return False
    
#     def _set_quality(self):
#         """Attempt to set video quality"""
#         try:
#             # Click on settings gear
#             self.driver.execute_script("""
#                 var settingsButton = document.querySelector('.ytp-settings-button');
#                 if (settingsButton) settingsButton.click();
#             """)
#             time.sleep(0.5)
            
#             # Note: Full quality selection requires more complex interaction
#             # This is a simplified version
            
#         except Exception as e:
#             logger.debug(f"Driver {self.driver_id}: Could not set quality: {e}")
    
#     def _play_video(self) -> bool:
#         """Play the video"""
#         try:
#             # JavaScript play
#             self.driver.execute_script("""
#                 var video = document.querySelector('video');
#                 if (video) {
#                     video.play();
#                     video.muted = true;
#                 }
#             """)
#             time.sleep(1)
            
#             # Verify playing
#             is_playing = self._check_playing()
            
#             if not is_playing:
#                 # Fallback to spacebar
#                 from selenium.webdriver.common.action_chains import ActionChains
#                 ActionChains(self.driver).send_keys(Keys.SPACE).perform()
#                 time.sleep(1)
#                 is_playing = self._check_playing()
            
#             self.stats.is_playing = is_playing
#             return is_playing
            
#         except Exception as e:
#             logger.error(f"Driver {self.driver_id}: Error playing video: {e}")
#             return False
    
#     def _check_playing(self) -> bool:
#         """Check if video is playing"""
#         try:
#             return self.driver.execute_script("""
#                 var video = document.querySelector('video');
#                 return video && !video.paused && !video.ended && video.readyState > 2;
#             """)
#         except:
#             return False
    
#     def _update_video_info(self):
#         """Update video playback information"""
#         try:
#             info = self.driver.execute_script("""
#                 var video = document.querySelector('video');
#                 return video ? {
#                     currentTime: video.currentTime,
#                     duration: video.duration,
#                     paused: video.paused
#                 } : null;
#             """)
            
#             if info:
#                 self.stats.current_time = info.get('currentTime', 0)
#                 self.stats.duration = info.get('duration', 0)
#                 self.stats.is_playing = not info.get('paused', True)
                
#         except Exception as e:
#             logger.debug(f"Driver {self.driver_id}: Error updating video info: {e}")
    
#     def refresh(self) -> bool:
#         """Refresh driver and restart video"""
#         try:
#             self.stats.status = 'refreshing'
#             logger.info(f"Driver {self.driver_id}: Refreshing...")
            
#             self.driver.refresh()
            
#             WebDriverWait(self.driver, self.config.video_check_timeout).until(
#                 EC.presence_of_element_located((By.TAG_NAME, "video"))
#             )
            
#             time.sleep(random.uniform(self.config.min_delay, self.config.max_delay))
            
#             if self._play_video():
#                 self.stats.status = 'running'
#                 self.stats.refresh_count += 1
#                 self.stats.last_refresh = datetime.now().strftime('%H:%M:%S')
#                 self._update_video_info()
#                 logger.info(f"Driver {self.driver_id}: Refresh successful")
#                 return True
#             else:
#                 self.stats.status = 'error'
#                 self.stats.error_count += 1
#                 return False
                
#         except Exception as e:
#             logger.error(f"Driver {self.driver_id}: Refresh error: {e}")
#             self.stats.status = 'error'
#             self.stats.error_count += 1
#             return False
    
#     def update_stats(self):
#         """Update driver statistics"""
#         self._update_video_info()
        
#         # Update uptime
#         uptime = datetime.now() - self.start_time
#         hours, remainder = divmod(int(uptime.total_seconds()), 3600)
#         minutes, seconds = divmod(remainder, 60)
#         self.stats.uptime = f"{hours}:{minutes:02d}:{seconds:02d}"
        
#         # Update resource usage
#         if self.process:
#             try:
#                 self.stats.cpu_percent = self.process.cpu_percent()
#                 self.stats.memory_mb = self.process.memory_info().rss / 1024 / 1024
#             except:
#                 pass
    
#     def close(self):
#         """Close driver"""
#         if self.driver:
#             try:
#                 self.driver.quit()
#                 self.stats.status = 'stopped'
#                 logger.info(f"Driver {self.driver_id}: Closed")
#             except Exception as e:
#                 logger.error(f"Driver {self.driver_id}: Error closing: {e}")

# # ==================== System Controller ====================

# class SystemController:
#     """Main controller for the automation system"""
    
#     def __init__(self, url: str, num_drivers: int, config: SystemConfig):
#         self.url = url
#         self.num_drivers = num_drivers
#         self.config = config
#         self.drivers: List[DriverManager] = []
#         self.running = False
#         self.stats_lock = Lock()
#         self.start_time = datetime.now()
        
#     def initialize_drivers(self):
#         """Initialize all drivers"""
#         logger.info(f"Initializing {self.num_drivers} driver(s)...")
        
#         proxies = self._get_proxy_list() if self.config.use_proxy else [None] * self.num_drivers
        
#         for i in range(self.num_drivers):
#             proxy = proxies[i % len(proxies)] if proxies else None
#             driver_manager = DriverManager(i + 1, self.url, self.config, proxy)
            
#             if driver_manager.initialize():
#                 self.drivers.append(driver_manager)
            
#             time.sleep(random.uniform(self.config.min_delay, self.config.max_delay))
        
#         if not self.drivers:
#             raise Exception("No drivers initialized successfully")
        
#         logger.info(f"Successfully initialized {len(self.drivers)}/{self.num_drivers} driver(s)")
    
#     def _get_proxy_list(self) -> List[str]:
#         """Load proxy list from config"""
#         if self.config.proxy_list:
#             return self.config.proxy_list
        
#         # Try loading from file
#         if os.path.exists('proxies.txt'):
#             with open('proxies.txt', 'r') as f:
#                 proxies = [line.strip() for line in f if line.strip()]
#                 logger.info(f"Loaded {len(proxies)} proxies from proxies.txt")
#                 return proxies
        
#         return []
    
#     def run(self):
#         """Main run loop"""
#         self.running = True
#         refresh_count = 0
        
#         logger.info("="*60)
#         logger.info(f"System running with {len(self.drivers)} driver(s)")
#         logger.info("Press Ctrl+C to stop")
#         logger.info("="*60)
        
#         try:
#             while self.running:
#                 time.sleep(self.config.refresh_interval)
#                 refresh_count += 1
                
#                 logger.info(f"\n{'='*60}")
#                 logger.info(f"Refresh Cycle #{refresh_count}")
#                 logger.info(f"{'='*60}")
                
#                 for driver in self.drivers:
#                     driver.refresh()
#                     time.sleep(random.uniform(self.config.min_delay, self.config.max_delay))
                
#                 # Update all stats
#                 self._update_all_stats()
                
#         except KeyboardInterrupt:
#             logger.info("\nShutdown signal received...")
#         except Exception as e:
#             logger.error(f"Error in main loop: {e}")
#         finally:
#             self.shutdown()
    
#     def _update_all_stats(self):
#         """Update statistics for all drivers"""
#         with self.stats_lock:
#             for driver in self.drivers:
#                 driver.update_stats()
    
#     def get_system_stats(self) -> Dict:
#         """Get overall system statistics"""
#         with self.stats_lock:
#             total_refreshes = sum(d.stats.refresh_count for d in self.drivers)
#             total_errors = sum(d.stats.error_count for d in self.drivers)
#             active_drivers = sum(1 for d in self.drivers if d.stats.status == 'running')
            
#             uptime = datetime.now() - self.start_time
            
#             return {
#                 'uptime': str(uptime).split('.')[0],
#                 'active_drivers': active_drivers,
#                 'total_drivers': len(self.drivers),
#                 'total_refreshes': total_refreshes,
#                 'total_errors': total_errors,
#                 'url': self.url,
#                 'drivers': [asdict(d.stats) for d in self.drivers]
#             }
    
#     def shutdown(self):
#         """Shutdown all drivers"""
#         self.running = False
#         logger.info("Shutting down all drivers...")
        
#         for driver in self.drivers:
#             driver.close()
        
#         logger.info("System shutdown complete")

# # ==================== Web Dashboard ====================

# class Dashboard:
#     """Web dashboard for monitoring"""
    
#     def __init__(self, controller: SystemController, port: int = 5000):
#         self.controller = controller
#         self.port = port
#         self.app = Flask(__name__)
#         self._setup_routes()
    
#     def _setup_routes(self):
#         """Setup Flask routes"""
        
#         @self.app.route('/')
#         def index():
#             return render_template_string(DASHBOARD_HTML)
        
#         @self.app.route('/api/stats')
#         def get_stats():
#             return jsonify(self.controller.get_system_stats())
        
#         @self.app.route('/api/refresh/<int:driver_id>', methods=['POST'])
#         def refresh_driver(driver_id):
#             for driver in self.controller.drivers:
#                 if driver.driver_id == driver_id:
#                     success = driver.refresh()
#                     return jsonify({'success': success})
#             return jsonify({'success': False, 'error': 'Driver not found'}), 404
    
#     def run(self):
#         """Run dashboard server"""
#         logger.info(f"Dashboard starting on http://localhost:{self.port}")
#         self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)

# # ==================== Dashboard HTML ====================

# DASHBOARD_HTML = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>YouTube Automation Dashboard</title>
#     <style>
#         * { margin: 0; padding: 0; box-sizing: border-box; }
#         body { 
#             font-family: 'Segoe UI', Arial, sans-serif; 
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             color: #333;
#             padding: 20px;
#         }
#         .container { max-width: 1400px; margin: 0 auto; }
#         .header {
#             background: white;
#             padding: 30px;
#             border-radius: 10px;
#             box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#             margin-bottom: 20px;
#         }
#         .header h1 { color: #667eea; margin-bottom: 10px; }
#         .stats-grid {
#             display: grid;
#             grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#             gap: 15px;
#             margin-bottom: 20px;
#         }
#         .stat-card {
#             background: white;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         }
#         .stat-card h3 { color: #666; font-size: 14px; margin-bottom: 10px; }
#         .stat-card .value { font-size: 32px; font-weight: bold; color: #667eea; }
#         .drivers-grid {
#             display: grid;
#             grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
#             gap: 15px;
#         }
#         .driver-card {
#             background: white;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#             border-left: 4px solid #667eea;
#         }
#         .driver-card.error { border-left-color: #e74c3c; }
#         .driver-card.running { border-left-color: #2ecc71; }
#         .driver-header {
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             margin-bottom: 15px;
#         }
#         .driver-id { font-size: 18px; font-weight: bold; }
#         .status {
#             padding: 5px 12px;
#             border-radius: 20px;
#             font-size: 12px;
#             font-weight: bold;
#             text-transform: uppercase;
#         }
#         .status.running { background: #2ecc71; color: white; }
#         .status.error { background: #e74c3c; color: white; }
#         .status.refreshing { background: #f39c12; color: white; }
#         .driver-info { font-size: 13px; color: #666; line-height: 1.8; }
#         .driver-info div { display: flex; justify-content: space-between; }
#         .refresh-btn {
#             margin-top: 10px;
#             padding: 8px 16px;
#             background: #667eea;
#             color: white;
#             border: none;
#             border-radius: 5px;
#             cursor: pointer;
#             font-size: 13px;
#         }
#         .refresh-btn:hover { background: #5568d3; }
#         .progress-bar {
#             width: 100%;
#             height: 6px;
#             background: #ecf0f1;
#             border-radius: 3px;
#             margin: 10px 0;
#             overflow: hidden;
#         }
#         .progress-fill {
#             height: 100%;
#             background: #667eea;
#             transition: width 0.3s;
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>🎬 YouTube Automation Dashboard</h1>
#             <p id="url"></p>
#         </div>
        
#         <div class="stats-grid">
#             <div class="stat-card">
#                 <h3>Uptime</h3>
#                 <div class="value" id="uptime">0:00:00</div>
#             </div>
#             <div class="stat-card">
#                 <h3>Active Drivers</h3>
#                 <div class="value" id="active-drivers">0</div>
#             </div>
#             <div class="stat-card">
#                 <h3>Total Refreshes</h3>
#                 <div class="value" id="total-refreshes">0</div>
#             </div>
#             <div class="stat-card">
#                 <h3>Total Errors</h3>
#                 <div class="value" id="total-errors">0</div>
#             </div>
#         </div>
        
#         <div class="drivers-grid" id="drivers-grid"></div>
#     </div>

#     <script>
#         function updateDashboard() {
#             fetch('/api/stats')
#                 .then(res => res.json())
#                 .then(data => {
#                     document.getElementById('url').textContent = data.url;
#                     document.getElementById('uptime').textContent = data.uptime;
#                     document.getElementById('active-drivers').textContent = 
#                         `${data.active_drivers}/${data.total_drivers}`;
#                     document.getElementById('total-refreshes').textContent = data.total_refreshes;
#                     document.getElementById('total-errors').textContent = data.total_errors;
                    
#                     const grid = document.getElementById('drivers-grid');
#                     grid.innerHTML = data.drivers.map(d => {
#                         const progress = d.duration ? (d.current_time / d.duration * 100).toFixed(1) : 0;
#                         return `
#                             <div class="driver-card ${d.status}">
#                                 <div class="driver-header">
#                                     <div class="driver-id">Driver ${d.driver_id}</div>
#                                     <span class="status ${d.status}">${d.status}</span>
#                                 </div>
#                                 <div class="progress-bar">
#                                     <div class="progress-fill" style="width: ${progress}%"></div>
#                                 </div>
#                                 <div class="driver-info">
#                                     <div><span>Playing:</span><span>${d.is_playing ? '▶️ Yes' : '⏸️ No'}</span></div>
#                                     <div><span>Progress:</span><span>${Math.floor(d.current_time)}s / ${Math.floor(d.duration)}s</span></div>
#                                     <div><span>Refreshes:</span><span>${d.refresh_count}</span></div>
#                                     <div><span>Errors:</span><span>${d.error_count}</span></div>
#                                     <div><span>Last Refresh:</span><span>${d.last_refresh}</span></div>
#                                     <div><span>Uptime:</span><span>${d.uptime}</span></div>
#                                     <div><span>CPU:</span><span>${d.cpu_percent.toFixed(1)}%</span></div>
#                                     <div><span>Memory:</span><span>${d.memory_mb.toFixed(1)} MB</span></div>
#                                 </div>
#                                 <button class="refresh-btn" onclick="refreshDriver(${d.driver_id})">
#                                     🔄 Refresh Now
#                                 </button>
#                             </div>
#                         `;
#                     }).join('');
#                 });
#         }
        
#         function refreshDriver(driverId) {
#             fetch(`/api/refresh/${driverId}`, { method: 'POST' })
#                 .then(res => res.json())
#                 .then(data => {
#                     if (data.success) {
#                         alert(`Driver ${driverId} refreshed successfully`);
#                     } else {
#                         alert(`Failed to refresh driver ${driverId}`);
#                     }
#                     updateDashboard();
#                 });
#         }
        
#         updateDashboard();
#         setInterval(updateDashboard, 2000);
#     </script>
# </body>
# </html>
# """

# # ==================== Main Application ====================

# def load_config_file(filename='config.json') -> SystemConfig:
#     """Load configuration from file"""
#     if os.path.exists(filename):
#         try:
#             with open(filename, 'r') as f:
#                 data = json.load(f)
#                 logger.info(f"Configuration loaded from {filename}")
#                 return SystemConfig(**data)
#         except Exception as e:
#             logger.warning(f"Error loading config: {e}. Using defaults.")
    
#     # Create default config
#     config = SystemConfig()
#     with open(filename, 'w') as f:
#         json.dump(asdict(config), f, indent=4)
#     logger.info(f"Default configuration created: {filename}")
    
#     return config

# def main():
#     """Main application entry point"""
#     print("\n" + "="*60)
#     print("   YouTube Automation System - Enhanced Edition")
#     print("="*60 + "\n")
    
#     # Load configuration
#     config = load_config_file()
    
#     # Get user input
#     url = input("Enter YouTube video URL: ").strip()
#     num_drivers = int(input("Enter number of drivers: "))
    
#     # Optional settings
#     headless_input = input("Run in headless mode? (y/n) [n]: ").strip().lower()
#     config.headless = headless_input == 'y'
    
#     dashboard_input = input("Enable web dashboard? (y/n) [y]: ").strip().lower()
#     config.enable_dashboard = dashboard_input != 'n'
    
#     # Initialize controller
#     controller = SystemController(url, num_drivers, config)
    
#     try:
#         controller.initialize_drivers()
        
#         # Start dashboard in separate thread if enabled
#         if config.enable_dashboard:
#             dashboard = Dashboard(controller, config.dashboard_port)
#             dashboard_thread = Thread(target=dashboard.run, daemon=True)
#             dashboard_thread.start()
#             print(f"\n📊 Dashboard available at: http://localhost:{config.dashboard_port}\n")
        
#         # Run main controller
#         controller.run()
        
#     except Exception as e:
#         logger.critical(f"Critical error: {e}")
#         controller.shutdown()
    
#     print("\nThank you for using YouTube Automation System!")

# if __name__ == "__main__":
#     # Handle signals for graceful shutdown
#     def signal_handler(sig, frame):
#         logger.info("\nShutdown signal received...")
#         sys.exit(0)
    
#     signal.signal(signal.SIGINT, signal_handler)
#     signal.signal(signal.SIGTERM, signal_handler)
    
#     try:
#         main()
#     except Exception as e:
#         logger.critical(f"Fatal error: {e}")
#         sys.exit(1)