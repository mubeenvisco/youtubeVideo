from dataclasses import dataclass
from typing import List, Optional
import json
import os
import logging

logger = logging.getLogger(__name__)

@dataclass
class SystemConfig:
    """System configuration"""
    refresh_interval: int = 60
    min_delay: float = 2.0
    max_delay: float = 5.0
    video_check_timeout: int = 10
    max_retry_attempts: int = 3
    headless: bool = False
    use_proxy: bool = False
    proxy_list: List[str] = None
    mute_audio: bool = True
    quality: str = "720p"
    enable_dashboard: bool = True
    dashboard_port: int = 5000

def load_config_file(filename='config.json') -> SystemConfig:
    """Load configuration from file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                logger.info(f"Configuration loaded from {filename}")
                return SystemConfig(**data)
        except Exception as e:
            logger.warning(f"Error loading config: {e}. Using defaults.")

    # Create default config
    config = SystemConfig()
    with open(filename, 'w') as f:
        json.dump({
            "refresh_interval": config.refresh_interval,
            "min_delay": config.min_delay,
            "max_delay": config.max_delay,
            "video_check_timeout": config.video_check_timeout,
            "max_retry_attempts": config.max_retry_attempts,
            "headless": config.headless,
            "use_proxy": config.use_proxy,
            "proxy_list": config.proxy_list,
            "mute_audio": config.mute_audio,
            "quality": config.quality,
            "enable_dashboard": config.enable_dashboard,
            "dashboard_port": config.dashboard_port
        }, f, indent=4)
    logger.info(f"Default configuration created: {filename}")

    return config
