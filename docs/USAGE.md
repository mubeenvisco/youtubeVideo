# Usage Guide

## Basic Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Enter the YouTube video URL when prompted
3. Specify the number of browser instances
4. Choose optional settings (headless mode, dashboard)

## Command Line Options

The system prompts for configuration during startup:

- **YouTube URL**: Full URL of the video to automate
- **Number of drivers**: How many browser instances to run (1-10 recommended)
- **Headless mode**: Run browsers in background (y/n)
- **Web dashboard**: Enable monitoring interface (y/n)

## Web Dashboard

When enabled, access the dashboard at `http://localhost:5000`

### Dashboard Features

- **System Statistics**: Uptime, active drivers, total refreshes/errors
- **Driver Details**: Individual driver status, video progress, resource usage
- **Manual Controls**: Force refresh specific drivers
- **Real-time Updates**: Auto-refreshing data every 2 seconds

## Configuration Options

### Refresh Settings

- `refresh_interval`: Seconds between page refreshes (default: 60)
- `min_delay`/`max_delay`: Random delay range between actions (default: 2-5s)

### Browser Settings

- `headless`: Run without visible browser windows
- `mute_audio`: Start videos muted to reduce resource usage
- `quality`: Preferred video quality (currently basic implementation)

### Dashboard Settings

- `enable_dashboard`: Enable web interface
- `dashboard_port`: Port for dashboard server (default: 5000)

## Advanced Usage

### Proxy Rotation

1. Add proxies to `proxies.txt`:
   ```
   http://proxy1.example.com:8080
   http://proxy2.example.com:8080
   ```

2. Enable in config: `"use_proxy": true`

### Monitoring Logs

Check `logs/` directory for detailed logs with timestamps.

### Resource Management

- Monitor CPU/memory usage in dashboard
- Adjust refresh intervals based on system performance
- Use headless mode to reduce visual overhead

## Stopping the System

- Press `Ctrl+C` in the terminal
- The system will gracefully close all browser instances
- Check logs for any errors during shutdown
