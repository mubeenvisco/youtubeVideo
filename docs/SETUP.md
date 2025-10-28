
## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Stable internet connection

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Chrome Installation

Ensure Google Chrome is installed and accessible. The system will automatically download the appropriate ChromeDriver.

### 3. Configure the System (Optional)

Edit `config.json` to customize settings:

```json
{
    "refresh_interval": 60,
    "headless": false,
    "enable_dashboard": true,
    "dashboard_port": 5000
}
```

### 4. Setup Proxies (Optional)

If using proxy rotation:

1. Add proxy servers to `proxies.txt` (one per line)
2. Set `"use_proxy": true` in `config.json`

## Running the Application

```bash
python main.py
```

Follow the prompts to enter the YouTube URL and number of drivers.

## Troubleshooting Setup Issues

### ChromeDriver Issues

If you encounter ChromeDriver errors:

1. Ensure Chrome is up to date
2. Try running: `webdriver-manager update`
3. Check if Chrome is in your PATH

### Permission Errors

On some systems, you may need to run with elevated privileges or adjust Chrome security settings.

### Port Conflicts

If the dashboard port (5000) is in use, change it in `config.json`.
