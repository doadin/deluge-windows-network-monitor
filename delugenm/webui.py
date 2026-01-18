"""
Web UI for Network Monitor plugin
"""

import logging
from deluge.plugins.webui import WebUIPluginBase
from deluge.web.auth import requires_auth
import json

log = logging.getLogger(__name__)


class WebUI(WebUIPluginBase):
    """Web UI for Network Monitor - configuration API and UI"""
    
    def enable(self):
        """Enable Web UI"""
        log.info("Network Monitor Web UI enabled")
    
    def disable(self):
        """Disable Web UI"""
        log.info("Network Monitor Web UI disabled")
    
    @requires_auth
    def get_config(self):
        """Get current configuration"""
        try:
            config = self.core.get_config()
            return json.dumps(config)
        except Exception as e:
            log.error(f"Error getting config: {e}")
            return json.dumps({"error": str(e)})
    
    @requires_auth
    def set_config(self, check_interval=None, required_adapters=None):
        """Update configuration"""
        try:
            config = {}
            if check_interval is not None:
                config["check_interval"] = int(check_interval)
            if required_adapters is not None:
                # Handle both list and comma-separated string
                if isinstance(required_adapters, str):
                    config["required_adapters"] = [
                        adapter.strip() 
                        for adapter in required_adapters.replace(",", ";").split(";")
                        if adapter.strip()
                    ]
                else:
                    config["required_adapters"] = required_adapters
            
            if config:
                self.core.update_config(**config)
                return json.dumps({"success": True, "config": self.core.get_config()})
            else:
                return json.dumps({"error": "No configuration provided"})
        except Exception as e:
            log.error(f"Error setting config: {e}")
            return json.dumps({"error": str(e)})
