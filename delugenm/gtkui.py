"""
GTK UI for Network Monitor plugin (optional UI components)
"""

import logging

try:
    from deluge.plugins.init import GtkPluginBase
    GTKUI_AVAILABLE = True
except ImportError:
    GTKUI_AVAILABLE = False

log = logging.getLogger(__name__)


class GtkUI:
    """GTK UI for Network Monitor - minimal implementation"""
    
    def enable(self):
        """Enable GTK UI"""
        if not GTKUI_AVAILABLE:
            log.debug("GTK UI not available")
            return
        log.info("Network Monitor GTK UI enabled")
    
    def disable(self):
        """Disable GTK UI"""
        log.info("Network Monitor GTK UI disabled")
