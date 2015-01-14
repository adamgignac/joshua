from gi.repository import Gtk, Gdk

class EnhancedNotebook(Gtk.Notebook):
    """A gtk.Notebook with configurable right click menu on tabs and a
    "New tab" button
    """
    def __init__(self, menu_items, new_callback=None):
        """Init function.
        Args:
        menu_items: a dictionary of labels and functions to be used to create
            items for the tab context menu.
        new_callback: the function to be called when the "New tab" button is
            clicked.
        """
        super(EnhancedNotebook, self).__init__()
        self.menu_items = menu_items
        if new_callback:
            self.new_callback = new_callback
            
        #Add a new tab button
        new_image = Gtk.Image()
        new_image.set_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.MENU)
        if new_callback:
            new_button = Gtk.Button()
            new_button.set_image(new_image)
            new_button.connect('clicked', self.on_new_clicked)
            self.set_action_widget(new_button, Gtk.PackType.END) #Yeehaw
            new_button.show()
        self.set_scrollable(True)
    
    #Override the append_page method to add an EventBox to the label
    def append_page(self, page_widget, tab_label=None):
        if page_widget:
            if not tab_label:
                tab_label = Gtk.Label("New Tab")
            eb = Gtk.EventBox()
            eb.set_visible_window(False)
            eb.add(tab_label)
            eb.connect_object('button-press-event', self.on_button_press, 
                self._make_menu(self.menu_items, tab_label.get_text()))
            eb.show_all()
            super(EnhancedNotebook, self).append_page(page_widget, tab_label=eb)
    
    #Override get_label, get_label_text, set_label, set_label_text to work
    #around the EventBox
    
    def get_tab_label(self, child):
        eb = super(EnhancedNotebook, self).get_tab_label(child)
        return eb.get_child()
    
    def get_tab_label_text(self, child):
        eb = super(EnhancedNotebook, self).get_tab_label(child)
        try:
            return eb.get_child().get_text()
        except:
            return None #Because some widgets don't have get_text()
    
    def set_tab_label(self, child, tab_label=None):
        if not tab_label:
            tab_label = Gtk.Label("")
        eb = Gtk.EventBox()
        eb.set_visible_window(False)
        eb.add(tab_label)
        eb.connect_object('button-press-event', self.on_button_press, 
            self._make_menu(self.menu_items, tab_label.get_text()))
        eb.show_all()
        super(EnhancedNotebook, self).set_tab_label(child, eb)
    
    def set_tab_label_text(self, child, tab_label=None):
        eb = Gtk.EventBox()
        eb.set_visible_window(False)
        eb.add(Gtk.Label(tab_label))
        eb.connect_object('button-press-event', self.on_button_press, 
            self._make_menu(self.menu_items, tab_label.get_text()))
        eb.show_all()
        super(EnhancedNotebook, self).set_tab_label(child, eb)
    
    #Custom methods============================================================
    def _make_menu(self, items, tab_label):
        """Create a menu from the given items
            items: a dictionary consisting of {'label':callback}
            tab_label: the string used to label the current tab, passed
            as an argument to the function
            callback signature:
            def menu_callback(widget, menu, tab_label)
        """
        menu = Gtk.Menu()
        for item in items:
            menu_item = Gtk.MenuItem(item)
            menu_item.connect('activate', items[item], tab_label)
            menu.append(menu_item)
        menu.show_all()
        return menu

    def on_button_press(self, menu, event):
        """Note that widget is the menu, not the widget being clicked"""
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            #Only respond to right clicks
            menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False
    
    def on_new_clicked(self, widget):
        resp = self.new_callback()
        if resp: #If self.new_callback returns successfully:
            new_page, label = resp #unpack
            self.append_page(new_page, label)
        self.show_all()
        
if __name__ == '__main__':
    w = Gtk.Window()
    w.set_size_request(300, 300)
    w.connect('destroy', lambda w:Gtk.main_quit())
    
    def foo(window, data):
        print(data)
    
    def new():
        """Returns the widget to add to the notebook"""
        return Gtk.Label("New page")

    book = EnhancedNotebook({'menu option':foo}, new)
    w.add(book)
    
    book.append_page(Gtk.Label("Page 1"), tab_label=Gtk.Label("one"))
    book.append_page(Gtk.Label("Page 2"), tab_label=Gtk.Label("two"))
    w.show_all()
    Gtk.main()
