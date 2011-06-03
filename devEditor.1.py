#!/usr/bin/env python
import wx
import os
import re

class MainWindow(wx.Frame):
  def __init__(self, parent, title):
    
    self.panel = []
    self.textC = []
    self.textContainer = []
    self.activeFiles = []
    self.control = False
    self.shift = False
    #CREO LA VENTANA
    wx.Frame.__init__(self, parent, title=title, size=(1000,1000))
    self.Show(True)
    self.SetIcon(wx.Icon('./ico.ico', wx.BITMAP_TYPE_ICO))
    
    #CREO BARRA DE MENUS
    filemenu= wx.Menu()
    menuNew = filemenu.Append(wx.ID_NEW, "&New"," Open a new file")
    filemenu.AppendSeparator()
    menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a new file")
    menuOpenProy = filemenu.Append(0, "&Open Proyect"," Open a full preyect file")
    filemenu.AppendSeparator()
    menuSave = filemenu.Append(wx.ID_SAVE,"&Save"," Save the file")
    menuSaveAs = filemenu.Append(wx.ID_SAVEAS,"Save &as"," Save the file as a new file")
    filemenu.AppendSeparator()
    menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
    menuBar = wx.MenuBar()
    menuBar.Append(filemenu,"&File")
    self.SetMenuBar(menuBar)
    
    #CREO EVENTOS DEL MENU
    self.Bind(wx.EVT_MENU, self.OnNewFile, menuNew)
    self.Bind(wx.EVT_MENU, self.OnOpenProyectFolder, menuOpenProy)
    self.Bind(wx.EVT_MENU, self.OnOpenFile, menuOpen)
    self.Bind(wx.EVT_MENU, self.OnSaveFile, menuSave)
    self.Bind(wx.EVT_MENU, self.OnSaveAsFile, menuSaveAs)
    self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
    
    #CREO STATUS BAR
    self.CreateStatusBar()
    
    #CREO VENTANA SPLITEADA
    self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)
    self.editPanel = wx.Panel(self.splitter, -1)
    self.tabbed = wx.Notebook(self.editPanel, -1, style=0)
    self.filesPanel = wx.Panel(self.splitter, -1)
    
    self._layout()
    
    #CREO UN NUEVO TAB
    self.OnNewFile(self)
    
    #EVENTOS DEL TABBED
    self.tabbed.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
    self.tabbed.Bind(wx.EVT_MIDDLE_UP, self.OnCloseTab)
    
    #CREO EL TREEVIEW
    sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
    self.treeView = wx.TreeCtrl(self.filesPanel)
    sizer_4.Add(self.treeView, 100, wx.wx.EXPAND, 0)
    self.filesPanel.SetSizer(sizer_4)
    
    #CREO TOOL BAR
    self.toolbar = self.CreateToolBar()
    self.toolbar.SetToolBitmapSize((16,16))  # sets icon size
 
    new_ico = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16,16))
    newTool = self.toolbar.AddSimpleTool(wx.ID_ANY, new_ico, "New", "Open a new tab")

    open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
    openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Open", "Open a file to edit")
    self.toolbar.AddSeparator()
    
    save_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, (16,16))
    saveTool = self.toolbar.AddSimpleTool(wx.ID_ANY, save_ico, "Save", "Saves the chages to disk")

    saveas_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, (16,16))
    saveasTool = self.toolbar.AddSimpleTool(wx.ID_ANY, saveas_ico, "Save As", "Saves As a new file the chages to disk")
    
    self.toolbar.AddSeparator()
    self.toolbar.Realize()
    
    #EVENTOS DEL TOOL BAR
    self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.treeView)
    self.Bind(wx.EVT_TOOL, self.OnNewFile, newTool)
    self.Bind(wx.EVT_TOOL, self.OnOpenFile, openTool)
    self.Bind(wx.EVT_TOOL, self.OnSaveFile, saveTool)
    self.Bind(wx.EVT_TOOL, self.OnSaveAsFile, saveasTool)
    self.Maximize()

  def _layout(self):
    sizer_1 = wx.BoxSizer(wx.VERTICAL)
    sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_1.Add(self.splitter, 1, wx.EXPAND, 20)
    self.SetSizer(sizer_1)
    self.editPanel.SetSizer(sizer_2)
    sizer_3.Add(self.tabbed, 1, wx.EXPAND, 0)
    self.editPanel.SetSizer(sizer_3)
    self.splitter.SplitVertically(self.filesPanel, self.editPanel, 400)
    sizer_1.Fit(self)
    sizer_1.SetSizeHints(self)
    self.Layout()
    
  def OnNewFile(self,e):
    self.panel.append(wx.Panel(self.tabbed, -1))
    self.tabbed.AddPage(self.panel[len(self.panel)-1], "Untitled")
    self.textC.append(wx.TextCtrl(self.panel[len(self.panel)-1], style= (wx.TE_MULTILINE | wx.TE_DONTWRAP)))
    self.textContainer.append(wx.BoxSizer(wx.HORIZONTAL))
    self.textContainer[len(self.panel)-1].Add(self.textC[len(self.panel)-1], 1, wx.ALL|wx.EXPAND, 5)
    self.panel[len(self.panel)-1].SetSizer(self.textContainer[len(self.panel)-1])
    self.tabbed.SetSelection(len(self.textC)-1)
    self.textC[len(self.textC)-1].SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
    self.activeFiles.append("")
    self.textC[len(self.textC)-1].Bind(wx.EVT_KEY_UP, self.hightlighting)
    self.textC[len(self.textC)-1].Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

  def OnKeyDown(self, e):
    indexText = self.tabbed.GetSelection()
    global controll
    global textC
    global shift
    keycode = e.GetKeyCode()
    if keycode == wx.WXK_CONTROL:
      init = self.textC[indexText].GetInsertionPoint()
      self.hightlighting(e)
      self.control = True
      text = " " + self.textC[indexText].GetValue() + " "
      while text[init-1:init] <> " " and text[init-1:init] <> ")" and text[init-1:init] <> ";"  and text[init-1:init] <> "	"  and text[init-1:init] <> ".":
	init = init - 1
	
      end = init+1
      while text[end-1:end] <> " " and text[end-1:end] <> "(" and text[end-1:end] <> "{" and text[end-1:end] <> "	":
	end = end + 1
      
      init = init-1
      end = end-1
      self.textC[indexText].SetStyle(init, end, wx.TextAttr('#000000', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_BOLD)))
      e.Skip()
    elif keycode == wx.WXK_SHIFT:
      self.shift = True
    elif keycode == 114 or keycode == 82:
      if self.control == True and self.shift == True:
	wx.MessageBox('Choose Resource Box', 'Info')
      else:
	e.Skip()
    else:
      if self.control == False:
	tabName = self.tabbed.GetPageText(indexText)
	if tabName[len(tabName) - 1:] <> '*':
	  self.tabbed.SetPageText(indexText, self.tabbed.GetPageText(indexText) + "*")
	e.Skip()
      
  def OnCloseTab(self,e):
    toClose = self.tabbed.GetSelection()
    del self.panel[toClose]
    del self.textC[toClose]
    del self.activeFiles[toClose]
    del self.textContainer[toClose]
    self.tabbed.RemovePage(toClose)
    
  def OnPageChanged(self, e):
    self.hightlighting(e)
    
  def OnActivated(self, e):
    realPathName = self.GetItemText(e.GetItem()).split("  				-  \"")[1][:-1]
    filename = realPathName = self.GetItemText(e.GetItem()).split("  				-  \"")[0]
    continueCon = True
    item = 0
    for i in range(0, len(self.activeFiles)):
      if self.activeFiles[i] == realPathName:
	continueCon = False
	item = i
	self.tabbed.SetSelection(item)
	
    if continueCon == True:
      self.Open(e,realPathName, filename)

  def GetItemText(self, item):
    if item:
      return self.treeView.GetItemText(item)
    else:
      return ""
      
  def AddTreeNodes(self, parentItem, items):
    for item in items:
      if type(item) == str:
	self.treeView.AppendItem(parentItem, item)
      else:
	newItem = self.treeView.AppendItem(parentItem, item[0])
	self.AddTreeNodes(newItem, item[0])
	
  def OnOpenProyectFolder(self,e):
    dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
      a = os.system('find ' + dialog.GetPath() + ' > ../foundedDirs.txt')
      f = open('../foundedDirs.txt', 'r')
      a = f.readline()
      a = f.readline()
      b = a.split(dialog.GetPath())
      li = []
      lastli = 0;
      lastlen = 1
      rootName = dialog.GetPath().split("/")
      rootName =  rootName[len(rootName) - 1]
      li.append(self.treeView.AddRoot(rootName))
      stop = 0
      while len(b) > 1:
	b = a.split(dialog.GetPath())
	a = f.readline()
	if len(b) > 1:
	  b[1] = b[1].replace("\n", "")
	  c = b[1].split('/')
	  if len(c) > lastlen:
	    lastlen = len(c)
	    if lastli + 1>=len(li):
	      li.append(self.treeView.AppendItem(li[len(li)-1], c[lastlen - 1] + "  				-  \"" + dialog.GetPath() + b[1] + "\""))
	      lastli = len(li)-1
	    else:
	      li[lastli + 1] = self.treeView.AppendItem(li[lastli], c[lastlen - 1] + "  				-  \"" + dialog.GetPath() + b[1] + "\"")
	      lastli = lastli+1
	    parent = lastli - 1
	  elif len(c) == lastlen:
	    li[lastli] = self.treeView.AppendItem(li[parent], c[lastlen - 1] + "  				-  \"" + dialog.GetPath() + b[1] + "\"")
	  elif len(c) < lastlen:
	    dif = lastlen - len(c)
	    lastli = len(c)-1
	    parent = lastli - 1
	    lastlen = len(c)
	    li[lastli] = self.treeView.AppendItem(li[parent], c[lastlen - 1] + "  				-  \"" + dialog.GetPath() + b[1] + "\"")
	  
      os.system('rm ../foundedDirs.txt')
      dialog.Destroy()
      
  def Open(self, e, fullPath, filename):
    self.OnNewFile(e)
    f = open(fullPath, 'r')
    self.textC[len(self.textC)-1].SetValue(f.read())
    f.close()
    self.tabbed.SetSelection(len(self.textC)-1)
    self.hightlighting(e)
    self.tabbed.SetPageText(len(self.textC)-1,filename)
    self.activeFiles[len(self.textC)-1] = fullPath
    
  def OnOpenFile(self,e):
    self.dirname = ''
    dlg = wx.FileDialog(self, "Open file", self.dirname, "", "*", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
      filename = dlg.GetFilename()
      self.dirname = dlg.GetDirectory()
      pathName = os.path.join(self.dirname, filename)
      continueCon = True
      for i in range(0, len(self.activeFiles)):
	if self.activeFiles[i] == pathName:
	  item = i
	  self.tabbed.SetSelection(item)
	  continueCon = False
	  
      if continueCon == True:
	self.Open(e,pathName, filename)
      dlg.Destroy()
      
      
  def hightlighting(self, e):
    global controll
    self.control = False
    self.shift = False
    indexText = self.tabbed.GetSelection()
    text = self.textC[indexText].GetValue()
    self.textC[indexText].SetStyle(0, len(self.textC[indexText].GetValue()) ,wx.TextAttr('#000000', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_NORMAL)))
    search = ["function",
	      "/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/", 
	      "\"([^\"]+)\"",
	      "\"\"",
	      "\'\'",
	      "\'([^\']+)\'",
	      "//([^\n]+)\n"]
	      
    searchCol = [wx.TextAttr('#000000', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_BOLD)), 
		 wx.TextAttr('#A4A4A4', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.ITALIC, wx.FONTWEIGHT_LIGHT)),
		 wx.TextAttr('#B40404', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_LIGHT)),
		 wx.TextAttr('#B40404', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_LIGHT)),
		 wx.TextAttr('#B40404', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_LIGHT)),
		 wx.TextAttr('#B40404', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_LIGHT)),
		 wx.TextAttr('#A4A4A4', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.ITALIC, wx.FONTWEIGHT_LIGHT))]
    ind = 0
    lessWord = ""
    lessInd = 0
    index = 0
    plus = 0
    while (ind <> -1):
      for i in range(0, len(search)):
	p = re.compile(search[i])
	if lessWord == "":
	  lessInd = p.search(text)
	  if (lessInd <> None):
	    lessWord = text[lessInd.start(): lessInd.end()]
	    index = i
	elif p.search(text) != None:
	  if p.search(text).start() < lessInd.start():
	    lessInd = p.search(text)
	    lessWord = text[lessInd.start():lessInd.end()]
	    a = lessInd
	    index = i
      
      ind = text.find(lessWord)
      ind = ind + plus
      if lessWord == "":
	ind = -1
	
      if (ind <> -1):
	self.textC[indexText].SetStyle(long(ind), long(ind + len(lessWord)),searchCol[index])
	ind = ind - plus
	text = text[ind + len(lessWord):]
	plus = plus + ind + len(lessWord)
	lessWord = ""      
	
  def Save(self, fullPath):
    indexText = self.tabbed.GetSelection()
    f = open(fullPath, 'w')
    f.write(self.textC[indexText].GetValue())
    f.close()
    tabName = self.tabbed.GetPageText(indexText)
    if tabName[len(tabName) - 1:] == '*':
      self.tabbed.SetPageText(indexText, self.tabbed.GetPageText(indexText)[:-1])
    
  def OnSaveFile(self,e):
    indexText = self.tabbed.GetSelection()
    if self.activeFiles[indexText] <> '':
      self.Save(self.activeFiles[indexText])
    else:
      self.OnSaveAsFile(e)

  def OnSaveAsFile(self,e):
    indexText = self.tabbed.GetSelection()
    self.dirname = ''
    dlg = wx.FileDialog(self, "Save As", self.dirname, "", "*", wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
      filename = dlg.GetFilename()
      self.dirname = dlg.GetDirectory()
      pathName = os.path.join(self.dirname, filename)
      self.tabbed.SetPageText(indexText,filename) 
      self.Save(pathName)
      self.activeFiles[indexText] = pathName
      dlg.Destroy()
      
  def OnExit(self,e):
    self.Close(True)
    
app = wx.App(False)
frame = MainWindow(None, "DevEditor")
app.MainLoop()
