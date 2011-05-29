#!/usr/bin/env python
import sys
import pygtk
import gtk

TextView = gtk.TextView(buffer=None)
Window = gtk.Window(gtk.WINDOW_TOPLEVEL)
class MainForm:
  def __init__(self):
    #Propiedades de la Ventana
    Window.set_title("Untitled - DevEditor")
    Window.set_default_size(750,450)
    Window.connect("destroy", self.destroy)
    
    #Creo Barra de Menus
    self.MenuBar = gtk.MenuBar()
    
    #Creo subMenus
    self.filemenu = gtk.Menu()
    self.openM = gtk.MenuItem("Open")
    self.filemenu.append(self.openM)
    self.openM.show()
    self.openM.connect("activate", self.open_file)
    self.fileM = gtk.MenuItem("File")
    self.fileM.show()
    self.fileM.set_submenu(self.filemenu)
    
    self.vbox = gtk.VBox(False, 0)
    Window.add(self.vbox)
    
    self.menub = gtk.MenuBar()
    self.vbox.pack_start(self.menub, False, False, 2)
    
    #Propiedades del TextView
    TextView.set_editable(True)
    TextView.set_cursor_visible(True)
    
    self.menub.append(self.fileM)
    self.sw = gtk.ScrolledWindow()
    self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.sw.add(TextView)
    
    self.vbox.pack_end(self.sw, True, True, 2)
    
    Window.add(TextView)
    TextView.show()
    Window.show()
    Window.show_all()
    
  def destroy(self, widget, data=None):
    gtk.main_quit()
  
  def open_file(self, event):
    self.chooser = gtk.FileChooserDialog(title="Open a file",action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
    self.chooser.set_default_response(gtk.RESPONSE_OK)
    
    self.filterText = gtk.FileFilter()
    self.filterText.set_name("Text Files")
    self.filterText.add_mime_type("text/data")
    self.filterText.add_pattern("*.txt")
    
    self.filterAll = gtk.FileFilter()
    self.filterAll.set_name("All Files")
    self.filterAll.add_pattern("*.*")
    
    self.chooser.add_filter(self.filterText)
    self.chooser.add_filter(self.filterAll)
    
    self.response = self.chooser.run()
    
    if self.response == gtk.RESPONSE_CANCEL:
      self.chooser.destroy()
      self.chooser.destroy()
    elif self.response == gtk.RESPONSE_OK:
      filename = self.chooser.get_filename()
      index = filename.rfind("/") + 1
      Window.set_title(filename[index:] + " - DevEditor")
      textbuffer = TextView.get_buffer()
      file = open(filename, "r")
      text = file.read()
      textbuffer.set_text(text)
      file.close()
      self.chooser.destroy()
      self.chooser.destroy()
      
def main():
  gtk.gdk.threads_enter()
  gtk.main()
  gtk.gdk.threads_leave()
  
if __name__ == "__main__":
  Initilize = MainForm()
  main()