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
    
    self.textView = gtk.TextView(buffer=None)
    self.textView.set_editable(True)
    self.textView.set_cursor_visible(True)
    self.window.add(self.textView)
    self.textView.show()
    self.window.show()
    
  def destroy(self, widget, data=None):
    gtk.main_quit()
  
def main():
  gtk.gdk.threads_enter()
  gtk.main()
  gtk.gdk.threads_leave()
  
if __name__ == "__main__":
  Initilize = MainForm()
  main()