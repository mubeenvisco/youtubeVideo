from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import time
import random
import logging
import psutil
import subprocess
import re
import os

logger = logging.getLogger(__name__)

@dataclass
class DriverStats:
    """Statistics for individual driver"""
    driver_id: int
    status: str  # 'running', 'stopped', 'error', 'refreshing'
    is_playing: bool
    current_time: float
    duration: float
    refresh_count: int
    error_count: int
    last_refresh: str
    uptime: str
    cpu_percent: float
    memory_mb: float

class DriverManager:
    """Manages individual Chrome driver instances"""

    def __init__(self, driver_id: int, url: str, config):
        self.driver_id = driver_id
        self.url = url
        self.config = config
        self.proxy = None  # Will be set by SystemController
        self.driver: Optional[webdriver.Chrome] = None
        self.stats = DriverStats(
            driver_id=driver_id,
            status='initializing',
            is_playing=False,
            current_time=0.0,
            duration=0.0,
            refresh_count=0,
            error_count=0,
            last_refresh='Never',
            uptime='0:00:00',
            cpu_percent=0.0,
            memory_mb=0.0
        )
        self.start_time = datetime.now()
        self.process = None

    def set_proxy(self, proxy: Optional[str]):
        """Set proxy for this driver"""
        self.proxy = proxy

    def _get_chrome_version(self):
        """Get installed Chrome version"""
        try:
            # For Windows
            cmd = 'reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version'
            output = subprocess.check_output(cmd, shell=True).decode()
            version = re.search(r"REG_SZ\s+(\d+\.\d+\.\d+)", output).group(1)
            return version
        except:
            return None

    def _create_driver(self) -> webdriver.Chrome:
        """Create Chrome driver with options"""
        chrome_options = Options()

        if self.config.headless:
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--disable-gpu')

        # Performance optimizations
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Mute audio
        if self.config.mute_audio:
            chrome_options.add_argument('--mute-audio')

        # Proxy configuration
        if self.proxy:
            chrome_options.add_argument(f'--proxy-server={self.proxy}')
            logger.info(f"Driver {self.driver_id}: Using proxy {self.proxy}")

        # User agent
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # Try to use cached ChromeDriver first, bypass Selenium Manager
        try:
            # Get the cached driver path
            cache_dir = os.path.join(os.path.expanduser("~"), ".wdm", "drivers", "chromedriver", "win64")
            if os.path.exists(cache_dir):
                # Find the latest version directory
                versions = [d for d in os.listdir(cache_dir) if os.path.isdir(os.path.join(cache_dir, d))]
                if versions:
                    latest_version = sorted(versions, key=lambda x: [int(i) for i in x.split('.')])[-1]
                    driver_path = os.path.join(cache_dir, latest_version, "chromedriver-win32", "chromedriver.exe")
                    if os.path.exists(driver_path):
                        logger.info(f"Driver {self.driver_id}: Using cached ChromeDriver at {driver_path}")
                        service = Service(driver_path)
                    else:
                        raise FileNotFoundError("Cached driver not found")
                else:
                    raise FileNotFoundError("No cached versions found")
            else:
                raise FileNotFoundError("Cache directory not found")
        except Exception as e:
            logger.warning(f"Driver {self.driver_id}: Could not use cached driver ({e}), falling back to webdriver-manager")
            try:
                service = Service(ChromeDriverManager().install())
            except Exception as e2:
                logger.error(f"Driver {self.driver_id}: webdriver-manager also failed: {e2}")
                raise e2

        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Set quality preference
        driver.execute_cdp_cmd('Network.enable', {})

        return driver

    def initialize(self) -> bool:
        """Initialize driver and start video"""
        for attempt in range(self.config.max_retry_attempts):
            try:
                logger.info(f"Driver {self.driver_id}: Initializing (attempt {attempt + 1}/{self.config.max_retry_attempts})")

                self.driver = self._create_driver()
                self.driver.get(self.url)

                # Store process for monitoring
                try:
                    self.process = psutil.Process(self.driver.service.process.pid)
                except:
                    pass

                # Wait for video element
                WebDriverWait(self.driver, self.config.video_check_timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )

                time.sleep(random.uniform(self.config.min_delay, self.config.max_delay))

                # Set quality if possible
                self._set_quality()

                # Start playing
                if self._play_video():
                    self.stats.status = 'running'
                    self._update_video_info()
                    logger.info(f"Driver {self.driver_id}: Successfully initialized")
                    return True
                else:
                    self.driver.quit()
                    self.stats.error_count += 1

            except Exception as e:
                logger.error(f"Driver {self.driver_id}: Initialization error: {e}")
                self.stats.error_count += 1
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass

                if attempt < self.config.max_retry_attempts - 1:
                    time.sleep(3)

        self.stats.status = 'error'
        logger.error(f"Driver {self.driver_id}: Failed to initialize")
        return False

    def _set_quality(self):
        """Attempt to set video quality"""
        try:
            # Click on settings gear
            self.driver.execute_script("""
                var settingsButton = document.querySelector('.ytp-settings-button');
                if (settingsButton) settingsButton.click();
            """)
            time.sleep(0.5)

            # Note: Full quality selection requires more complex interaction
            # This is a simplified version

        except Exception as e:
            logger.debug(f"Driver {self.driver_id}: Could not set quality: {e}")

    def _play_video(self) -> bool:
        """Play the video"""
        try:
            # JavaScript play
            self.driver.execute_script("""
                var video = document.querySelector('video');
                if (video) {
                    video.play();
                    video.muted = true;
                }
            """)
            time.sleep(1)

            # Verify playing
            is_playing = self._check_playing()

            if not is_playing:
                # Fallback to spacebar
                ActionChains(self.driver).send_keys(Keys.SPACE).perform()
                time.sleep(1)
                is_playing = self._check_playing()

            self.stats.is_playing = is_playing
            return is_playing

        except Exception as e:
            logger.error(f"Driver {self.driver_id}: Error playing video: {e}")
            return False

    def _check_playing(self) -> bool:
        """Check if video is playing"""
        try:
            return self.driver.execute_script("""
                var video = document.querySelector('video');
                return video && !video.paused && !video.ended && video.readyState > 2;
            """)
        except:
            return False

    def _update_video_info(self):
        """Update video playback information"""
        try:
            info = self.driver.execute_script("""
                var video = document.querySelector('video');
                return video ? {
                    currentTime: video.currentTime,
                    duration: video.duration,
                    paused: video.paused
                } : null;
            """)

            if info:
                self.stats.current_time = info.get('currentTime', 0)
                self.stats.duration = info.get('duration', 0)
                self.stats.is_playing = not info.get('paused', True)

        except Exception as e:
            logger.debug(f"Driver {self.driver_id}: Error updating video info: {e}")

    def refresh(self) -> bool:
        """Refresh driver and restart video"""
        try:
            self.stats.status = 'refreshing'
            logger.info(f"Driver {self.driver_id}: Refreshing...")

            self.driver.refresh()

            WebDriverWait(self.driver, self.config.video_check_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )

            time.sleep(random.uniform(self.config.min_delay, self.config.max_delay))

            if self._play_video():
                self.stats.status = 'running'
                self.stats.refresh_count += 1
                self.stats.last_refresh = datetime.now().strftime('%H:%M:%S')
                self._update_video_info()
                logger.info(f"Driver {self.driver_id}: Refresh successful")
                return True
            else:
                self.stats.status = 'error'
                self.stats.error_count += 1
                return False

        except Exception as e:
            logger.error(f"Driver {self.driver_id}: Refresh error: {e}")
            self.stats.status = 'error'
            self.stats.error_count += 1
            return False

    def update_stats(self):
        """Update driver statistics"""
        self._update_video_info()

        # Update uptime
        uptime = datetime.now() - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.stats.uptime = f"{hours}:{minutes:02d}:{seconds:02d}"

        # Update resource usage
        if self.process:
            try:
                self.stats.cpu_percent = self.process.cpu_percent()
                self.stats.memory_mb = self.process.memory_info().rss / 1024 / 1024
            except:
                pass

    def close(self):
        """Close driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.stats.status = 'stopped'
                logger.info(f"Driver {self.driver_id}: Closed")
            except Exception as e:
                logger.error(f"Driver {self.driver_id}: Error closing: {e}")
