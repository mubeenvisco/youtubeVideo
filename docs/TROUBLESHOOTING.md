# Troubleshooting Guide

## Common Issues

### ChromeDriver Errors

**Error:** `WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Solutions:**
1. Ensure Chrome is installed and up to date
2. The system should automatically download ChromeDriver, but you can manually run:
   ```bash
   webdriver-manager update
   ```
3. Check Chrome version compatibility

### Video Not Playing

**Symptoms:** Driver initializes but video doesn't start

**Solutions:**
1. Check YouTube URL is valid and publicly accessible
2. Try disabling headless mode to see browser behavior
3. Check network connectivity
4. Verify video isn't region-restricted

### Dashboard Not Loading

**Error:** Cannot connect to `http://localhost:5000`

**Solutions:**
1. Check if port 5000 is available: `netstat -an | find "5000"`
2. Change port in `config.json` if conflicted
3. Ensure Flask is properly installed
4. Check firewall settings

### High CPU/Memory Usage

**Symptoms:** System becomes slow or unresponsive

**Solutions:**
1. Reduce number of drivers
2. Enable headless mode
3. Increase refresh intervals
4. Monitor resource usage in dashboard
5. Close other applications

### Proxy Connection Issues

**Error:** Proxy servers failing to connect

**Solutions:**
1. Verify proxy format in `proxies.txt`
2. Test proxies manually
3. Check proxy authentication requirements
4. Try without proxies first

## Log Analysis

### Finding Errors

Check log files in `logs/` directory:

```bash
# View recent errors
tail -f logs/youtube_automation_*.log | grep ERROR
```

### Common Log Messages

- `Driver X: Initialization error`: Check Chrome installation
- `Video not playing after refresh`: Network or YouTube issues
- `Proxy connection failed`: Invalid proxy configuration
- `Memory limit exceeded`: Reduce driver count

## Performance Tuning

### Optimization Tips

1. **Headless Mode**: Reduces resource usage
2. **Refresh Intervals**: Balance between activity and performance
3. **Driver Count**: Start with 1-2 drivers, increase gradually
4. **Quality Settings**: Lower quality reduces bandwidth

### System Requirements

- **Minimum**: 4GB RAM, dual-core CPU
- **Recommended**: 8GB RAM, quad-core CPU for 5+ drivers
- **Network**: Stable broadband connection

## Recovery Procedures

### After System Crash

1. Check log files for error details
2. Restart with fewer drivers
3. Verify Chrome and dependencies
4. Test with simple YouTube video first

### Driver Recovery

The system includes automatic recovery:

- Failed drivers are retried up to `max_retry_attempts`
- Manual refresh available via dashboard
- Graceful shutdown on interruption

## Getting Help

### Debug Mode

Enable detailed logging by modifying logger setup in `utils/logger.py`:

```python
logger.setLevel(logging.DEBUG)
```

### System Information

For support requests, include:

- Python version: `python --version`
- Chrome version
- Operating system
- Full error logs
- Configuration file contents

## Prevention

### Best Practices

1. Regular system updates
2. Monitor resource usage
3. Use stable network connection
4. Keep Chrome updated
5. Regular log review
6. Backup configuration files
