#!/usr/bin/env python
import sys
import pygtk
import gtk

class MainForm:
  def __init__(self):
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title("Untitled - DevEditor")
    self.window.set_default_size(750,450)
    self.window.connect("destroy", self.destroy)

    self.MenuBar = gtk.MenuBar()
    self.filemenu = gtk.Menu()
    self.openM = gtk.MenuItem("Open")
    self.filemenu.append(self.openM)
    self.openM.show()
    self.fileM = gtk.MenuItem("File")
    self.fileM.show()
    self.fileM.set_submenu(self.filemenu)
    self.vbox = gtk.VBox(False, 0)
    self.window.add(self.vbox)
    self.vbox.show()
    
    self.menub = gtk.MenuBar()
    self.vbox.pack_start(self.menub, False, False, 2)
    self.menub.show()
    
    self.textView = gtk.TextView(buffer=None)
    self.textView.set_editable(True)
    self.textView.set_cursor_visible(True)
    
    self.vbox.pack_end(self.textView, True, True, 2)
    
    self.menub.append(self.fileM)
    

    
    self.window.add(self.textView)
    self.textView.show()
    self.window.show()
    self.window.show_all()
    
  def destroy(self, widget, data=None):
    gtk.main_quit()
  
def main():
  gtk.gdk.threads_enter()
  gtk.main()
  gtk.gdk.threads_leave()
  
if __name__ == "__main__":
  Initilize = MainForm()
  main()