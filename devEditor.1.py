#!/usr/bin/env python
import wx
import os
import re

global pathName
class MainWindow(wx.Frame):
  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, title=title, size=(500,500))
    self.textCtrl = wx.TextCtrl(self, style= (wx.TE_MULTILINE | wx.TE_DONTWRAP))
    self.CreateStatusBar()

    filemenu= wx.Menu()

    menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a new file")
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
    self.Bind(wx.EVT_MENU, self.OnOpenFile, menuOpen)
    self.Bind(wx.EVT_MENU, self.OnSaveFile, menuSave)
    self.Bind(wx.EVT_MENU, self.OnSaveAsFile, menuSaveAs)
    self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    self.Show(True)

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