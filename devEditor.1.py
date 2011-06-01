#!/usr/bin/env python
import wx
import os
import re

global pathName
global activaTab
global activeFiles
global textC
class MainWindow(wx.Frame):
  def __init__(self, parent, title):
    global activaTab
    global activeFiles
    global textC
    
    textC = []
    wx.Frame.__init__(self, parent, title=title, size=(1000,1000))
    self.SetIcon(wx.Icon('ico.ico', wx.BITMAP_TYPE_ICO))
    self.Maximize()
    grilla = wx.GridBagSizer()
    self.treeView = wx.TreeCtrl(self)
    self.panel = []
    grilla.Add(self.treeView,(0,0),(10,20), wx.EXPAND)
    
    self.tabbed = wx.Notebook(self, -1, style=(wx.NB_TOP))
    
    self.panel.append(wx.NotebookPage(self.tabbed, -1))
    self.tabbed.AddPage(self.panel[0], "Untitled")
    activaTab = 0
    activeFiles = []
    activeFiles.append("")
    textC.append(wx.TextCtrl(self.panel[0], style= (wx.TE_MULTILINE | wx.TE_DONTWRAP)))
    
    self.tabbed.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
    grilla.Add(self.tabbed,(0,20),(10,80), wx.EXPAND)
    
    
    
    
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
    
    
    
    
    grilla.AddGrowableCol(20)
    grilla.AddGrowableRow(2)
    
    self.SetSizerAndFit(grilla)
    self.CreateStatusBar()

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
    
    menuBar = wx.MenuBar(wx.MB_DOCKABLE)
    menuBar.Append(filemenu,"&File")
    self.SetMenuBar(menuBar)
    textC[0].SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
    
    self.tabbed.Bind(wx.EVT_MIDDLE_UP, self.OnCloseTab)
    self.panel[0].Bind(wx.EVT_MIDDLE_UP, self.OnCloseTab)
    self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.treeView)
    textC[0].Bind(wx.EVT_KEY_UP, self.hightlighting)
    self.Bind(wx.EVT_TOOL, self.OnNewFile, newTool)
    self.Bind(wx.EVT_TOOL, self.OnOpenFile, openTool)
    self.Bind(wx.EVT_TOOL, self.OnSaveFile, saveTool)
    self.Bind(wx.EVT_TOOL, self.OnSaveAsFile, saveasTool)
    self.Bind(wx.EVT_MENU, self.OnNewFile, menuNew)
    self.Bind(wx.EVT_MENU, self.OnOpenProyectFolder, menuOpenProy)
    self.Bind(wx.EVT_MENU, self.OnOpenFile, menuOpen)
    self.Bind(wx.EVT_MENU, self.OnSaveFile, menuSave)
    self.Bind(wx.EVT_MENU, self.OnSaveAsFile, menuSaveAs)
    self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    self.Show(True)
  def OnNewFile(self,e):
    self.panel.append(wx.NotebookPage(self.tabbed, -1))
    self.tabbed.AddPage(self.panel[len(self.panel)-1], "Untitled")
    textC.append(wx.TextCtrl(self.panel[len(self.panel)-1], style= (wx.TE_MULTILINE | wx.TE_DONTWRAP)))
    activeFiles.append("")
    self.tabbed.SetSelection(len(textC)-1)
    textC[len(textC)-1].SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
    textC[len(textC)-1].Bind(wx.EVT_KEY_UP, self.hightlighting)
    
  def OnCloseTab(self,e):
    toClose = self.tabbed.GetSelection()
    del self.panel[toClose]
    del textC[toClose]
    del activeFiles[toClose]
    self.tabbed.RemovePage(toClose)
    
  def OnPageChanged(self, e):
    activaTab = e.GetSelection()
    self.hightlighting(e)
    
  def OnActivated(self, e):
    global textC
    global activeFiles
    realPathName = self.GetItemText(e.GetItem()).split("  				-  \"")[1][:-1]
    filename = realPathName = self.GetItemText(e.GetItem()).split("  				-  \"")[0]
    continueCon = True
    item = 0
    for i in range(0, len(activeFiles)):
      if activeFiles[i] == realPathName:
	continueCon = False
	item = i
	self.tabbed.SetSelection(item)
	
    if continueCon == True:
      self.panel.append(wx.NotebookPage(self.tabbed, -1))
      self.tabbed.AddPage(self.panel[len(self.panel)-1], filename)
      textC.append(wx.TextCtrl(self.panel[len(self.panel)-1], style= (wx.TE_MULTILINE | wx.TE_DONTWRAP)))
      activeFiles.append(realPathName)
      f = open(realPathName, 'r')
      textC[len(textC)-1].SetValue(f.read())
      f.close()
      textC[len(textC)-1].SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
      textC[len(textC)-1].Bind(wx.EVT_KEY_UP, self.hightlighting)
      self.tabbed.SetSelection(len(textC)-1)
      self.hightlighting(e)

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
      
  def OnOpenFile(self,e):
    global pathName
    global activeFiles
    global textC
    self.dirname = ''
    dlg = wx.FileDialog(self, "Open file", self.dirname, "", "*", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
      filename = dlg.GetFilename()
      self.dirname = dlg.GetDirectory()
      pathName = os.path.join(self.dirname, filename)
      continueCon = True
      for i in range(0, len(activeFiles)):
	if activeFiles[i] == pathName:
	  item = i
	  self.tabbed.SetSelection(item)
	  continueCon = False
	  
      if continueCon == True:
	self.panel.append(wx.NotebookPage(self.tabbed, -1))
	self.tabbed.AddPage(self.panel[len(self.panel)-1], filename)
	textC.append(wx.TextCtrl(self.panel[len(self.panel)-1], style= (wx.TE_MULTILINE | wx.TE_DONTWRAP)))
	activeFiles.append(pathName)
	f = open(pathName, 'r')
	self.tabbed.SetSelection(len(textC)-1)
	textC[len(textC)-1].SetValue(f.read())
	textC[len(textC)-1].SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
	textC[len(textC)-1].Bind(wx.EVT_KEY_UP, self.hightlighting)
	f.close()
	self.hightlighting(e)
      dlg.Destroy()
      
      
  def hightlighting(self, e):
    indexText = self.tabbed.GetSelection()
    global textC
    text = textC[indexText].GetValue()
    textC[indexText].SetStyle(0, len(textC[indexText].GetValue()) ,wx.TextAttr('#000000', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_NORMAL)))
    search = ["function",
	      "/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/", 
	      "\"([^\"]+)\"",
	      "\'([^\']+)\'",
	      "//([^\n]+)\n"]
	      
    searchCol = [wx.TextAttr('#000000', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_BOLD)), 
		 wx.TextAttr('#A4A4A4', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.ITALIC, wx.FONTWEIGHT_LIGHT)),
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
	textC[indexText].SetStyle(long(ind), long(ind + len(lessWord)),searchCol[index])
	ind = ind - plus
	text = text[ind + len(lessWord):]
	plus = plus + ind + len(lessWord)
	lessWord = ""      
      
  def OnSaveFile(self,e):
    global activeFiles
    global textC
    indexText = self.tabbed.GetSelection()
    if activeFiles[indexText] <> '':
      f = open(pathName, 'w')
      f.write(textC[indexText].GetValue())
      f.close()
    else:
      self.OnSaveAsFile(e)

  def OnSaveAsFile(self,e):
    global activeFiles
    global textC
    indexText = self.tabbed.GetSelection()
    self.dirname = ''
    dlg = wx.FileDialog(self, "Save As", self.dirname, "", "*", wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
      filename = dlg.GetFilename()
      self.dirname = dlg.GetDirectory()
      pathName = os.path.join(self.dirname, filename)
      self.tabbed.SetPageText(indexText,filename) 
      f = open(pathName, 'w')
      activeFiles[indexText] = pathName
      f.write(textC[indexText].GetValue())
      f.close()
      dlg.Destroy()
      
  def OnExit(self,e):
    self.Close(True)
    
app = wx.App(False)
frame = MainWindow(None, "DevEditor")
app.MainLoop()