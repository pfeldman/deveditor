#!/usr/bin/env python
import wx
import os
import re

global pathName

class LazyTree(wx.TreeCtrl):
    def __init__(self, *args, **kwargs):
        super(LazyTree, self).__init__(*args, **kwargs)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapseItem)
        self.__collapsing = False
        #root = self.AddRoot('root')
        #self.SetItemHasChildren(root)

    def OnExpandItem(self, event):
        nrChildren = 6
        for childIndex in range(nrChildren):
            child = self.AppendItem(event.GetItem(), 'child %d'%childIndex)

    def OnCollapseItem(self, event):
        if self.__collapsing:
            event.Veto()
        else:
            self.__collapsing = True
            item = event.GetItem()
            self.CollapseAndReset(item)
            self.SetItemHasChildren(item)
            self.__collapsing = False



class MainWindow(wx.Frame):
  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, title=title, size=(500,500))
    grilla = wx.GridBagSizer()
    self.treeView = LazyTree(self)
    grilla.Add(self.treeView,(0,0),(10,20), wx.EXPAND)
    self.textCtrl = wx.TextCtrl(self, style= (wx.TE_MULTILINE | wx.TE_DONTWRAP))
    grilla.Add(self.textCtrl,(0,20),(10,26), wx.EXPAND)
    grilla.AddGrowableCol(20)
    grilla.AddGrowableRow(2)
    
    self.SetSizerAndFit(grilla)
    self.CreateStatusBar()

    filemenu= wx.Menu()

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
    self.textCtrl.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_NORMAL))
    
    
    self.textCtrl.Bind(wx.EVT_KEY_UP, self.hightlighting)
    self.Bind(wx.EVT_MENU, self.OnOpenProyectFolder, menuOpenProy)
    self.Bind(wx.EVT_MENU, self.OnOpenFile, menuOpen)
    self.Bind(wx.EVT_MENU, self.OnSaveFile, menuSave)
    self.Bind(wx.EVT_MENU, self.OnSaveAsFile, menuSaveAs)
    self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    self.Show(True)

  def OnOpenProyectFolder(self,e):
    dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
      #a = os.system("sabelo[0]='/home/pablo/Fuentes/deveditor/devEditor.old.py'")
      a = os.system('i=0 && for f in `find /home/pablo/Fuentes/deveditor/`; do')
      b = os.system("$f")
      print b
      #c = os.system("; done'")
      #sabelo[$i]= && i=$i+1
      
      #a = os.system('i=0 && for f in `find ' + dialog.GetPath() + '`; do sabelo[i]="$f" && i=$i+1; done && clear')
      #print a
      #c[len(c)] = 
      #a = string(a)
      #b = str(a).split('\n')
      #b = str(a)
      #c = b.rsplit('dialog.GetPath()')
      #print c[0]
      dialog.Destroy()
      
  def OnOpenFile(self,e):
    global pathName
    self.dirname = ''
    dlg = wx.FileDialog(self, "Open file", self.dirname, "", "*.*;*.txt", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
      filename = dlg.GetFilename()
      self.Title = filename + " - DevEditor"
      self.dirname = dlg.GetDirectory()
      pathName = os.path.join(self.dirname, filename)
      f = open(pathName, 'r')
      self.textCtrl.SetValue(f.read())
      f.close()
      dlg.Destroy()
      self.hightlighting(e)
      
  def hightlighting(self, e):
    text = self.textCtrl.GetValue()
    search = ["function",
	      "/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/", 
	      "\"([^\"]+)\"",
	      "\'([^\']+)\'"]
	      
    searchCol = [wx.TextAttr('#000000', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_BOLD)), 
		 wx.TextAttr('#A4A4A4', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.ITALIC, wx.FONTWEIGHT_LIGHT)),
		 wx.TextAttr('#B40404', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_LIGHT)),
		 wx.TextAttr('#B40404', wx.NullColour , wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.FONTWEIGHT_LIGHT))]
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
	elif p.search(text) != None and p.search(text).start() < lessInd.start():
	  lessInd = p.search(text)
	  lessWord = text[lessInd.start():lessInd.end()]
	  a = lessInd
	  lessInd = lessInd.start()
	  index = i
      
      ind = text.find(lessWord)
      ind = ind + plus
      if lessWord == "":
	ind = -1
	
      if (ind <> -1):
	self.textCtrl.SetStyle(long(ind), long(ind + len(lessWord)),searchCol[index])
	ind = ind - plus
	text = text[ind + len(lessWord):]
	plus = plus + ind + len(lessWord)
	lessWord = ""
	
	
	
      
      
  def OnSaveFile(self,e):
    global pathName
    if pathName <> '':
      f = open(pathName, 'w')
      f.write(self.textCtrl.GetValue())
    else:
      self.OnSaveAsFile(e)

  def OnSaveAsFile(self,e):
    self.dirname = ''
    dlg = wx.FileDialog(self, "Save As", self.dirname, "", "*.*;*.txt", wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
      filename = dlg.GetFilename()
      self.dirname = dlg.GetDirectory()
      pathName = os.path.join(self.dirname, filename)
      f = open(pathName, 'w')
      f.write(self.textCtrl.GetValue())
      f.close()
      dlg.Destroy()
      
  def OnExit(self,e):
    self.Close(True)
    
app = wx.App(False)
frame = MainWindow(None, "DevEditor")
app.MainLoop()