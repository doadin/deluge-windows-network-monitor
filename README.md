# Windows Network Monitor Plugin for Deluge

Monitors Windows network interfaces and automatically shuts down Deluge when no active network connection is detected.

## Features

- Continuously monitors Windows network adapters using WMI
- Checks for active/connected network interfaces
- Automatically shuts down Deluge if no connected interface is found
- Configurable check interval
- Optional: Monitor specific network adapters
- Comprehensive logging for debugging

## Requirements

- Deluge 2.0+
- Python 3.6+
- Windows OS (uses WMI for network monitoring)
- pywin32 package

## Installation

### From Source

1. Clone or download this plugin
2. Navigate to the plugin directory
3. Run: `python setup.py install`
4. Enable the plugin in Deluge preferences

### Manual

1. Build the plugin: `python setup.py bdist_egg`
2. Copy the `.egg` file to your Deluge plugins directory:
   - Windows: `%APPDATA%\Deluge\plugins\`
   - Linux: `~/.config/deluge/plugins/`
3. Restart Deluge and enable the plugin

## Network Adapter Status Values

The plugin considers these statuses as "active/connected":
- **2 (Connected)** - Adapter is actively connected
- **9 (Authentication Succeeded)** - Adapter authenticated and connected

These statuses indicate the adapter is NOT connected:
- **0 (Disconnected)** - Not connected
- **5 (Hardware Not Present)** - Hardware unavailable
- **7 (Media Disconnected)** - Physical disconnection
- **Disabled** - Adapter is disabled

## Configuration

The plugin checks network status every 5 seconds by default. You can customize this in the core.py file:

```python
self.check_interval = 5  # Change this value (in seconds)
```

To monitor specific adapters only, modify:

```python
self.required_adapters = ["Ethernet", "WiFi"]  # List your adapter names
```

## How It Works

1. Plugin enables and starts a background monitoring thread
2. Every 5 seconds, it queries Windows WMI for all network adapters
3. Checks if at least one adapter is in "Connected" status
4. If no active adapters are found, Deluge is gracefully shut down
5. All events are logged for debugging

## Logging

Check Deluge logs to see plugin activity:
- Windows: `%APPDATA%\Deluge\deluge.log`

Look for entries from "deluge_windows_network_monitor" logger.

## Troubleshooting

### Plugin not loading
- Ensure pywin32 is installed: `pip install pywin32`
- Check Deluge logs for errors

### WMI errors
- The WMI module requires proper Windows permissions
- Run Deluge with appropriate privileges if issues persist

### Plugin not shutting down
- Check logs to verify network monitoring is active
- Verify adapter names match WMI output

## License

GPL-3.0

## Support

For issues, questions, or suggestions, please create an issue on the repository.
