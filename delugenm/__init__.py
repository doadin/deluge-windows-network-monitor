"""
Windows Network Monitor Plugin for Deluge
Shuts down Deluge when a network interface is not up/connected
"""

import logging
import sys
import traceback

log = logging.getLogger(__name__)

try:
    from deluge.plugins.init import PluginBase
    log.info("Successfully imported PluginBase")
except Exception as e:
    log.error(f"Failed to import PluginBase: {e}")
    traceback.print_exc()
    raise

try:
    from .core import Core
    log.info("Successfully imported Core")
except Exception as e:
    log.error(f"Failed to import Core: {e}")
    traceback.print_exc()
    raise


class WindowsNetworkMonitorPlugin(PluginBase):
    def enable(self):
        """Enable the plugin"""
        try:
            log.info("=" * 50)
            log.info("Enabling Windows Network Monitor plugin")
            log.info("=" * 50)
            
            log.info("Creating Core instance...")
            self.core = Core()
            log.info("Core instance created successfully")
            
            log.info("Calling core.enable()...")
            self.core.enable()
            log.info("Core enabled successfully")
            
            log.info("Windows Network Monitor plugin enabled successfully")
            log.info("=" * 50)
        except Exception as e:
            log.error("=" * 50)
            log.error(f"Failed to enable Windows Network Monitor plugin: {e}")
            log.error(f"Exception type: {type(e).__name__}")
            log.error("Full traceback:")
            log.error(traceback.format_exc())
            log.error("=" * 50)
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
log.info("Creating plugin_base instance...")
plugin_base = WindowsNetworkMonitorPlugin(__name__)
log.info("plugin_base instance created successfully")
