import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio
import os

class MyViewer(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Viewer Ismendoza")
        ##self.set_default_size(1024,700)
        self.set_default_size(900,700)
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "My Pictures Ismendoza"
        self.set_titlebar(header)




#win = MyViewer()
#win.connect("delete-event", Gtk.main_quit)
#win.show_all()
