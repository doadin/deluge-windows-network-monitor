"""
GTK UI for Network Monitor plugin (optional UI components)
"""

import logging

try:
    import gtk
    from deluge.plugins.init import GtkPluginBase
    from deluge.ui.client import client
    GTKUI_AVAILABLE = True
except ImportError:
    GTKUI_AVAILABLE = False

log = logging.getLogger(__name__)


class GtkUI(GtkPluginBase):
    """GTK UI for Network Monitor - configuration UI"""
    
    def enable(self):
        """Enable GTK UI"""
        if not GTKUI_AVAILABLE:
            log.debug("GTK UI not available")
            return
        
        log.info("Network Monitor GTK UI enabled")
        self._build_ui()
        self._load_config()
    
    def disable(self):
        """Disable GTK UI"""
        log.info("Network Monitor GTK UI disabled")
    
    def _build_ui(self):
        """Build the configuration UI"""
        try:
            # Create main container
            self.vbox = gtk.VBox(spacing=10)
            self.vbox.set_border_width(10)
            
            # Check interval section
            check_interval_hbox = gtk.HBox(spacing=5)
            check_interval_label = gtk.Label("Check Interval (seconds):")
            check_interval_label.set_size_request(200, -1)
            self.check_interval_spin = gtk.SpinButton()
            self.check_interval_spin.set_range(1, 300)
            self.check_interval_spin.set_increments(1, 10)
            self.check_interval_spin.set_value(5)
            check_interval_hbox.pack_start(check_interval_label, False, False)
            check_interval_hbox.pack_start(self.check_interval_spin, False, False)
            self.vbox.pack_start(check_interval_hbox, False, False)
            
            # Required adapters section
            adapters_label = gtk.Label("Required Network Adapters:")
            adapters_label.set_alignment(0, 0)
            self.vbox.pack_start(adapters_label, False, False)
            
            # Create scrolled window for adapter list
            scrolled_window = gtk.ScrolledWindow()
            scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrolled_window.set_size_request(-1, 150)
            
            # Create text view for adapters
            self.adapters_text = gtk.TextView()
            self.adapters_text.set_wrap_mode(gtk.WRAP_WORD)
            scrolled_window.add(self.adapters_text)
            self.vbox.pack_start(scrolled_window, True, True)
            
            # Info label
            info_label = gtk.Label(
                "Enter adapter names separated by commas or newlines.\n"
                "Leave empty to monitor all adapters."
            )
            info_label.set_alignment(0, 0)
            self.vbox.pack_start(info_label, False, False)
            
            # Buttons
            button_hbox = gtk.HBox(spacing=5)
            
            self.save_button = gtk.Button("Save Configuration")
            self.save_button.connect("clicked", self._on_save_clicked)
            button_hbox.pack_start(self.save_button, False, False)
            
            self.refresh_button = gtk.Button("Refresh")
            self.refresh_button.connect("clicked", self._on_refresh_clicked)
            button_hbox.pack_start(self.refresh_button, False, False)
            
            self.vbox.pack_start(button_hbox, False, False)
            
            # Show all widgets
            self.vbox.show_all()
            
        except Exception as e:
            log.error(f"Error building UI: {e}")
    
    def _load_config(self):
        """Load configuration from core plugin"""
        try:
            if client.is_connected():
                config = client.deluge_windows_network_monitor.get_config()
                if config:
                    self.check_interval_spin.set_value(config.get("check_interval", 5))
                    
                    adapters = config.get("required_adapters", [])
                    adapters_text = "\n".join(adapters)
                    self.adapters_text.get_buffer().set_text(adapters_text)
                    
                    log.info("Configuration loaded into UI")
        except Exception as e:
            log.error(f"Error loading configuration: {e}")
    
    def _on_save_clicked(self, widget):
        """Save button clicked"""
        try:
            check_interval = int(self.check_interval_spin.get_value())
            
            # Parse adapters from text
            buffer_text = self.adapters_text.get_buffer().get_text(
                self.adapters_text.get_buffer().get_start_iter(),
                self.adapters_text.get_buffer().get_end_iter()
            )
            
            # Split by comma or newline and clean up
            adapters = []
            for line in buffer_text.replace(",", "\n").split("\n"):
                adapter = line.strip()
                if adapter:
                    adapters.append(adapter)
            
            config = {
                "check_interval": check_interval,
                "required_adapters": adapters
            }
            
            if client.is_connected():
                client.deluge_windows_network_monitor.update_config(**config)
                log.info("Configuration saved successfully")
                
                # Show confirmation
                dialog = gtk.MessageDialog(
                    None,
                    gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_INFO,
                    gtk.BUTTONS_OK,
                    "Configuration saved successfully!"
                )
                dialog.run()
                dialog.destroy()
            
        except Exception as e:
            log.error(f"Error saving configuration: {e}")
            dialog = gtk.MessageDialog(
                None,
                gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_ERROR,
                gtk.BUTTONS_OK,
                f"Error saving configuration: {e}"
            )
            dialog.run()
            dialog.destroy()
    
    def _on_refresh_clicked(self, widget):
        """Refresh button clicked"""
        self._load_config()
    
    def get_config(self):
        """Get current configuration from core"""
        if client.is_connected():
            return client.deluge_windows_network_monitor.get_config()
        return None
    
    def set_config(self, config):
        """Update configuration on core"""
        if client.is_connected():
            return client.deluge_windows_network_monitor.update_config(**config)
        return False
