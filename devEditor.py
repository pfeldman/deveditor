#!/usr/bin/env python
import sys
import pygtk
pygtk.require('2.0')
import gtk
import pango

TextView = gtk.TextView(buffer=None)
Window = gtk.Window(gtk.WINDOW_TOPLEVEL)
StatusBar = gtk.Statusbar()
filename = ""
class MainForm:
  def __init__(self):
    #Propiedades de la Ventana
    Window.set_title("Untitled - DevEditor")
    Window.set_default_size(750,450)
    Window.set_position(gtk.WIN_POS_CENTER)
    Window.connect("destroy", self.destroy)
    
    #Creo Barra de Menus
    self.MenuBar = gtk.MenuBar()
    agr = gtk.AccelGroup()
    Window.add_accel_group(agr)
    #Creo subMenus
    self.filemenu = gtk.Menu()
    self.openM = gtk.ImageMenuItem(gtk.STOCK_OPEN, agr)
    self.sepM = gtk.SeparatorMenuItem()
    self.saveM = gtk.ImageMenuItem(gtk.STOCK_SAVE, agr)
    self.saveAsM = gtk.ImageMenuItem(gtk.STOCK_SAVE_AS, agr)
    key,mod = gtk.accelerator_parse("<Control>O")
    self.openM.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
    key,mod = gtk.accelerator_parse("<Control>S")
    self.saveM.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
    self.filemenu.append(self.openM)
    self.filemenu.append(self.sepM)
    self.filemenu.append(self.saveM)
    self.filemenu.append(self.saveAsM)
    
    self.openM.connect("activate", self.open_file)
    self.saveM.connect("activate", self.save_file)
    self.saveAsM.connect("activate", self.save_fileas)
    self.fileM = gtk.MenuItem("File")
    self.fileM.set_submenu(self.filemenu)
    
    self.vbox = gtk.VBox(False, 0)
    Window.add(self.vbox)
    
    self.menub = gtk.MenuBar()
    self.vbox.pack_start(self.menub, False, False, 0)
    
    #Propiedades del TextView
    TextView.set_editable(True)
    TextView.set_cursor_visible(True)
    TextView.set_border_window_size(gtk.TEXT_WINDOW_LEFT,1)
    TextView.set_border_window_size(gtk.TEXT_WINDOW_RIGHT,1)
    TextView.set_border_window_size(gtk.TEXT_WINDOW_TOP,1)
    TextView.set_border_window_size(gtk.TEXT_WINDOW_BOTTOM,1)

    
    fontdesc = pango.FontDescription("monospace 9")
    TextView.modify_font(fontdesc)
    self.menub.append(self.fileM)
    self.sw = gtk.ScrolledWindow()
    self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.sw.add(TextView)

    self.vbox.pack_start(self.sw, True, True, 0)
    self.vbox.pack_end(StatusBar, False, True, 8)
    
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
      global filename
      filename = self.chooser.get_filename()
      index = filename.rfind("/") + 1
      StatusBar.push(0, filename[index:] + " opened")
      Window.set_title(filename[index:] + " - DevEditor")
      textbuffer = TextView.get_buffer()
      file = open(filename, "r")
      text = file.read()
      textbuffer.set_text(text)
      file.close()
      self.chooser.destroy()
      self.chooser.destroy()
      
  def save_file(self, event):
    global filename
    if filename == "":
      self.save_fileas(event)
    else:
      self.save(filename)

  def save(self, filename):
    textbuffer = TextView.get_buffer()
    index = filename.replace("\\","/").rfind("/") + 1
    text = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())
    file = open(filename, "w")
    file.write(text)
    file.close()
    StatusBar.push(0, filename[index:] + " saved")
    Window.set_title(filename[index:] + " - DevEditor")
    
  def save_fileas(self, event):
    self.chooser = gtk.FileChooserDialog(title="Save file",action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
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
      self.save(filename)
      self.chooser.destroy()
      self.chooser.destroy()
	
def main():
  gtk.gdk.threads_enter()
  gtk.main()
  gtk.gdk.threads_leave()
  
if __name__ == "__main__":
  Initilize = MainForm()
  main()