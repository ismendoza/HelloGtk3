import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio
import os
from viewer import MyViewer
myUser = os.environ.get( "USERNAME" )
sdir = "c:\\users\\"+myUser+"\\pictures\\"

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Ismendoza")
        ##self.set_default_size(1024,700)
        self.set_default_size(900,700)
        #self.maximize()
        vbox = Gtk.VBox()
        self.add(vbox)

        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "My Pictures Ismendoza"
        self.set_titlebar(header)

        pixbuficon = GdkPixbuf.Pixbuf.new_from_file_at_scale("explorer.png", 50, 50, True)
        self.listFiles = []

        self.combo_store = Gtk.ListStore(str)
        self.combo_store.append([sdir])
        self.source_combo = Gtk.ComboBox.new_with_model_and_entry(self.combo_store)

        self.source_combo.set_entry_text_column(0)
        self.source_combo.set_active(0)
        self.source_entry = self.source_combo.get_child()
        self.source_entry.set_icon_activatable(1, True)
        self.source_entry.set_icon_from_pixbuf (1, pixbuficon)
        self.source_entry.connect("icon-press", self.on_press)
        self.source_entry.connect("activate", self.add_entry)

        vbox.pack_start(self.source_combo, False, False, 0)
        self.sw = Gtk.ScrolledWindow()
        vbox.add(self.sw)

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(10)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        j.display_images(self,sdir)

        self.sw.add(self.flowbox)
        self.source_combo.connect("changed", self.on_name_combo_changed)

    def display_images(self, selectedDir):
        #Load Images
        n_children = len(self.flowbox)
        print(n_children)
        if n_children > 0:
            for child in self.flowbox.get_children():
                #print(child.get_child().get_child()
                self.flowbox.remove(child)
        for file in os.listdir(selectedDir):
            if file.endswith(".jpg"):
                f = os.path.join(selectedDir+"\\", file)
                self.listFiles.append(f)
                image = Gtk.Image()
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(f, 100, 150, True)
                image.set_from_pixbuf(pixbuf)
                eventbox = Gtk.EventBox()
                eventbox.connect("button_press_event", self.on_eventbox_click)
                eventbox.add(image)
                self.flowbox.add(eventbox)
        self.flowbox.show_all()

    def on_press(self, entry, event, pos):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selectedFolder = dialog.get_filename()
            mylist = []
            for a in self.combo_store:
                mylist.append(a[0])
            #for i in range(0, len(mylist)):
                #print(mylist[i])
            if selectedFolder in mylist:
                print(selectedFolder)
                self.source_entry.set_text(selectedFolder)
                j.display_images(self,selectedFolder)
            else:
                self.combo_store.append([selectedFolder])
                self.source_entry.set_text(selectedFolder)
                j.display_images(self,selectedFolder)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")

        dialog.destroy()

    def on_name_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            name = model[tree_iter][:1]
            print("Selected: name=%s" % (name))
            print("seleccionado: " +name[0])
            #Load Images
            j.display_images(self, name[0])
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())

    def add_entry(self,entry):
        entrada = self.source_entry.get_text()
        mylist = []
        for a in self.combo_store:
            mylist.append(a[0])
        #for i in range(0, len(mylist)):
            #print(mylist[i])
        if entrada in mylist:
            print(entrada)
            j.display_images(self,entrada)
        else:
            self.combo_store.append([entrada])
            j.display_images(self, entrada)

    def on_eventbox_click(self,evenbox, event):
        viewer = MyViewer()
        titulo = Gtk.Label("NUEVA VENTANA")
        viewer.add(titulo)
        viewer.connect("destroy", Gtk.Widget.destroy)
        viewer.show_all()

j = MyWindow
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
