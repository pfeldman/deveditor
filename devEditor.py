#!/usr/bin/env python
import sys
import pygtk
pygtk.require('2.0')
import gtk
import pango


class RichBuffer(gtk.TextBuffer):
    '''a buffer that makes it easy to manipulate a gtk textview with 
    rich text'''

    def __init__(self):
        '''constructor'''
        gtk.TextBuffer.__init__(self)

        self.colormap = gtk.gdk.colormap_get_system()

        self.fg_tags = {}
        self.bg_tags = {}
        self.font_tags = {}
        self.size_tags = {}
        self.bold_tag = self.create_tag("bold", weight=pango.WEIGHT_BOLD) 
        self.italic_tag = self.create_tag("italic", style=pango.STYLE_ITALIC) 
        self.underline_tag = self.create_tag("underline", underline=pango.UNDERLINE_SINGLE) 
        self.strike_tag = self.create_tag("strike", strikethrough=True) 

    def put_text(self, text, fg_color=None, bg_color=None, font=None, size=None, bold=False, italic=False, underline=False, strike=False):
        '''insert text at the current position with the style defined by the 
        optional parameters'''
        tags = self._parse_tags(fg_color, bg_color, font, size, bold, italic, underline, strike)
        iterator = self.get_iter_at_mark(self.get_insert())#(self.get_insert())
        self._insert(iterator, text, tags)

    def _insert(self, iterator, text, tags=None):
        '''insert text at the current position with the style defined by the 
        optional parameters'''
        if tags is not None:
            self.insert_with_tags(iterator, text, *tags)
        else:
            self.insert(iterator, text)

    def _parse_tags(self, fg_color=None, bg_color=None, font=None, size=None, bold=False, italic=False, underline=False, strike=False):
        '''parse the parameters and return a list of tags to apply that 
        format
        '''
        tags = []

        if fg_color:
            tag = self._parse_fg(fg_color)
            if tag:
                tags.append(tag)

        if bg_color:
            tag = self._parse_bg(bg_color)
            if tag:
                tags.append(tag)

        if font:
            tag = self._parse_font(font)
            if tag:
                tags.append(tag)

        if size:
            tag = self._parse_size(size)
            if tag:
                tags.append(tag)

        if bold:
            tags.append(self.bold_tag)

        if italic:
            tags.append(self.italic_tag)

        if underline:
            tags.append(self.underline_tag)

        if strike:
            tags.append(self.strike_tag)

        return tags

    def _parse_fg(self, value):
        '''parse the foreground color and return a tag'''
        if value in self.fg_tags:
            return self.fg_tags[value]

        try:
            color = gtk.gdk.color_parse(value)
            self.colormap.alloc_color(color)
        except ValueError:
            return None

        color_tag = self.create_tag('fg_' + value[1:], foreground_gdk=color)
        self.fg_tags[value] = color_tag

        return color_tag

    def _parse_bg(self, value):
        '''parse the background color and return a tag'''
        if value in self.bg_tags:
            return self.bg_tags[value]

        try:
            color = gtk.gdk.color_parse(value)
            self.colormap.alloc_color(color)
        except ValueError:
            return None

        color_tag = self.create_tag('bg_' + value[1:], background_gdk=color)
        self.bg_tags[value] = color_tag

        return color_tag

    def _parse_font(self, value):
        '''parse the font and return a tag'''
        if value in self.font_tags:
            return self.font_tags[value]

        font_tag = self.create_tag('font_' + value.replace(' ', '_'), 
            font=value)
        self.font_tags[value] = font_tag
        
        return font_tag

    def _parse_size(self, value):
        '''parse the font size and return a tag'''
        if value in self.size_tags:
            return self.size_tags[value]

        size_tag = self.create_tag('size_' + str(value), size_points=value)
        self.size_tags[value] = size_tag
        return size_tag

TextView = gtk.TextView()
buff = RichBuffer()
TextView.set_buffer(buff)
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
    #buff.put_text('buenas, como va? ', '#000000', '#FFFFFF', 'Arial', 10, True, True, True, True)
    #buff.put_text('esto es una prueba\n', '#CC0000', '#AAAAAA', 'Purisa', 14)
    #buff.put_text('un poco de formato\n', '#00CC00', '#FFFFFF', 'Andale Mono', 8, True, True, True, True)
    #buff.put_text('un poco mas\n', '#CCCCCC', '#0000CC', 'Andale Mono', 16, False, True, False, True)
    
  def destroy(self, widget, data=None):
    gtk.main_quit()
  
  def apply_style(self, objects):
    if self.textbuffer.get_has_selection():
      start, end = self.textbuffer.get_selection_bounds()
      self.textbuffer.remove_all_tags( start, end)
      for style in self.styles:
        self.textbuffer.apply_tag_by_name( style, start, end)
  
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
      #textbuffer = TextView.get_buffer()
      file = open(filename, "r")
      text = file.read()
      buff.set_text(text)
      file.close()
      self.chooser.destroy()
      self.chooser.destroy()
      lastFound = 0
      text = buff.get_text(buff.get_start_iter() , buff.get_end_iter())
      text1 = text
      search = ["function", "integer"]
      ind = 0
      buff.set_text("")
      lessWord = ""
      lessInd = 0
      while (ind <> -1):
	for i in range(0, len(search)):
	  if lessWord == "":
	    lessWord = search[i]
	    lessInd = text.find(search[i])
	    if (lessInd == -1):
	      lessWord = ""
	  elif text.find(search[i]) < lessInd and text.find(search[i]) > -1:
	    lessInd = text.find(search[i])
	    lessWord = search[i]
	ind = text.find(lessWord)
	if lessWord == "":
	  ind = -1
	  
	if (ind <> -1):
	  buff.put_text(text[0:ind], '#000000', '#FFFFFF', 'monospace', 10)
	  buff.put_text(lessWord, '#0404B4', '#FFFFFF', 'monospace', 10)
	  text = text[ind + len(lessWord):]
	  lessWord = ""
      
      buff.put_text(text, '#000000', '#FFFFFF', 'monospace', 10)
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