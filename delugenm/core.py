"""
Core plugin logic for Network Monitor
"""

import logging
import threading
import time
from datetime import datetime

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

from deluge.core.pluginmanager import CorePluginBase
from deluge import component

log = logging.getLogger(__name__)

# Network adapter status codes
STATUS_DISCONNECTED = 0
STATUS_CONNECTING = 1
STATUS_CONNECTED = 2
STATUS_DISCONNECTING = 3
STATUS_HARDWARE_NOT_PRESENT = 5
STATUS_MEDIA_DISCONNECTED = 7
STATUS_AUTHENTICATING = 8
STATUS_AUTHENTICATION_SUCCEEDED = 9
STATUS_AUTHENTICATION_FAILED = 10
STATUS_INVALID_ADDRESS = 11
STATUS_CREDENTIALS_REQUIRED = 12

# Active connection statuses (adapter is up/connected)
ACTIVE_STATUSES = {STATUS_CONNECTED, STATUS_AUTHENTICATION_SUCCEEDED}


class Core(CorePluginBase):
    def enable(self):
        """Enable the plugin"""
        if not WMI_AVAILABLE:
            log.error("WMI module not available. Install pywin32 to use this plugin.")
            return
        
        log.info("Network Monitor plugin enabled")
        self.monitor_thread = None
        self.monitoring = False
        self.check_interval = 5  # seconds
        self.required_adapters = []  # If empty, monitor all adapters
        
        self._start_monitoring()
    
    def disable(self):
        """Disable the plugin"""
        log.info("Network Monitor plugin disabled")
        self._stop_monitoring()
    
    def _start_monitoring(self):
        """Start the network monitoring thread"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        log.info("Network monitoring started")
    
    def _stop_monitoring(self):
        """Stop the network monitoring thread"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        log.info("Network monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                if not self._check_network_status():
                    log.warning("Network interface not connected - shutting down Deluge")
                    self._shutdown_deluge()
                    break
                
                time.sleep(self.check_interval)
            except Exception as e:
                log.error(f"Error in monitoring loop: {e}")
                time.sleep(self.check_interval)
    
    def _check_network_status(self):
        """
        Check if network interfaces are connected.
        Returns True if at least one active interface is found, False otherwise.
        """
        if not WMI_AVAILABLE:
            return True  # Can't check, assume network is OK
        
        try:
            c = wmi.WMI()
            active_adapters = []
            
            for nic in c.Win32_NetworkAdapter():
                # Skip disabled or disconnected adapters
                if not nic.NetEnabled:
                    continue
                
                adapter_status = nic.NetConnectionStatus
                adapter_name = nic.Name or "Unknown"
                
                # Check if status indicates connected
                if adapter_status in ACTIVE_STATUSES:
                    active_adapters.append(adapter_name)
                    log.debug(f"Active adapter found: {adapter_name} (status: {adapter_status})")
            
            # If we have required adapters, check if any are active
            if self.required_adapters:
                for req_adapter in self.required_adapters:
                    for nic in c.Win32_NetworkAdapter():
                        if nic.Name == req_adapter and nic.NetConnectionStatus in ACTIVE_STATUSES:
                            return True
                return False
            else:
                # If no specific adapters required, just need at least one active
                if active_adapters:
                    log.debug(f"Active adapters: {', '.join(active_adapters)}")
                    return True
                else:
                    log.warning("No active network adapters found")
                    return False
        
        except Exception as e:
            log.error(f"Error checking network status: {e}")
            return True  # Assume OK on error to avoid false shutdowns
    
    def _shutdown_deluge(self):
        """Shutdown Deluge"""
        try:
            log.info("Initiating Deluge shutdown")
            # Get the daemon component and shutdown
            component.get("Daemon").shutdown()
        except Exception as e:
            log.error(f"Error shutting down Deluge: {e}")
    
    def update(self):
        """Called when config is updated"""
        pass
