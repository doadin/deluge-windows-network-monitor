"""
Windows Network Monitor Plugin for Deluge
Shuts down Deluge when a network interface is not up/connected
"""

import logging
from deluge.plugins.init import PluginBase
from .core import Core

log = logging.getLogger(__name__)


class WindowsNetworkMonitorPlugin(PluginBase):
    def enable(self):
        """Enable the plugin"""
        try:
            log.info("Enabling Windows Network Monitor plugin")
            self.core = Core()
            self.core.enable()
            log.info("Windows Network Monitor plugin enabled successfully")
        except Exception as e:
            log.error(f"Failed to enable Windows Network Monitor plugin: {e}", exc_info=True)
            raise
    
    def disable(self):
        """Disable the plugin"""
        try:
            log.info("Disabling Windows Network Monitor plugin")
            if hasattr(self, 'core'):
                self.core.disable()
            log.info("Windows Network Monitor plugin disabled successfully")
        except Exception as e:
            log.error(f"Failed to disable Windows Network Monitor plugin: {e}", exc_info=True)
    
    def configure(self):
        """Configure the plugin"""
        pass


# Create and export the plugin instance
plugin_base = WindowsNetworkMonitorPlugin(__name__)
