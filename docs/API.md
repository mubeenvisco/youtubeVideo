# API Documentation

## Web Dashboard API

The web dashboard provides REST API endpoints for monitoring and control.

### Base URL
```
http://localhost:{dashboard_port}
```

### Endpoints

#### GET `/api/stats`

Returns comprehensive system statistics.

**Response:**
```json
{
    "uptime": "0:05:23",
    "active_drivers": 3,
    "total_drivers": 3,
    "total_refreshes": 15,
    "total_errors": 0,
    "url": "https://www.youtube.com/watch?v=...",
    "drivers": [
        {
            "driver_id": 1,
            "status": "running",
            "is_playing": true,
            "current_time": 45.2,
            "duration": 360.0,
            "refresh_count": 5,
            "error_count": 0,
            "last_refresh": "14:32:15",
            "uptime": "0:05:23",
            "cpu_percent": 12.3,
            "memory_mb": 156.7
        }
    ]
}
```

#### POST `/api/refresh/{driver_id}`

Manually refresh a specific driver.

**Parameters:**
- `driver_id` (int): The ID of the driver to refresh

**Response:**
```json
{
    "success": true
}
```

**Error Response:**
```json
{
    "success": false,
    "error": "Driver not found"
}
```

## Configuration API

### SystemConfig Class

The configuration is managed through the `SystemConfig` dataclass:

```python
@dataclass
class SystemConfig:
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
```

## Driver Management API

### DriverManager Class

Individual drivers expose the following methods:

- `initialize()`: Initialize and start video playback
- `refresh()`: Refresh page and restart video
- `update_stats()`: Update performance statistics
- `close()`: Close browser instance

### SystemController Class

The main controller provides:

- `initialize_drivers()`: Setup all driver instances
- `run()`: Start the main automation loop
- `get_system_stats()`: Get overall system statistics
- `shutdown()`: Gracefully stop all drivers

## Error Handling

The system includes comprehensive error handling:

- **Initialization Errors**: Automatic retry with exponential backoff
- **Playback Errors**: Fallback to keyboard simulation
- **Network Errors**: Connection timeout handling
- **Resource Errors**: Memory and CPU monitoring

## Logging API

### Logger Setup

The logging system provides:

- **File Logging**: Detailed logs saved to `logs/` directory
- **Console Logging**: Colored output for terminal
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Log Format

```
%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s
```

## Extension Points

### Custom Dashboard Templates

Override the default dashboard by modifying `DASHBOARD_HTML` in `utils/dashboard.py`.

### Custom Configuration Loaders

Extend `load_config_file()` in `utils/config_loader.py` for custom config sources.

### Additional Monitoring

Add custom metrics by extending the `DriverStats` and system stats methods.
