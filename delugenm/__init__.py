"""
Windows Network Monitor Plugin for Deluge
Shuts down Deluge when a network interface is not up/connected
"""

from deluge.plugins.init import PluginBase
from .core import Core
from .gtkui import GtkUI

class WindowsNetworkMonitorPlugin(PluginBase):
    def enable(self):
        self.core = Core(self.config)
    
    def disable(self):
        self.core.disable()
    
    def configure(self):
        pass

plugin_base = WindowsNetworkMonitorPlugin(__name__)
