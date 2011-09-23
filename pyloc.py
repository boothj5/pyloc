#!/usr/bin/python
from languages import *
import wx
from langctrl import LangPieCtrl, LangStatsCtrl, StatsProgressDialog
import wx.lib.agw.pyprogress as Progress
import os
import locale
import pylocstats

class PylocFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))

        self.dirname = ""

        self.CreateStatusBar()

        filemenu = wx.Menu()
        menu_open_dir = filemenu.Append(wx.ID_ANY, "Open &Directory", " Open a directory")
        filemenu.AppendSeparator()
        menu_about = filemenu.Append(wx.ID_ABOUT, "&About", " About Pyloc")
        filemenu.AppendSeparator()
        menu_exit = filemenu.Append(wx.ID_EXIT, "E&xit", " Exit Pyloc")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)       

        self.Bind(wx.EVT_MENU, self.on_open_dir, menu_open_dir)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

    def on_about(self, event):
        dialog = wx.MessageDialog(self, "Simple LOC counter", "About", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def on_exit(self, event):
        self.Close(True)

    def on_open_dir(self, event):
        dialog = wx.DirDialog(self, "Choose a directory", self.dirname)
        action = dialog.ShowModal() 
        if action == wx.ID_OK:
            self.SetStatusText("Preparing...")
            self.dirname = dialog.GetPath()
            dialog.Destroy()
            self.sizer.DeleteWindows()
            lang_stats = {}
 
            num_files = sum((len(f) for _, _, f in os.walk(self.dirname)))

            self.SetStatusText("Scanning...")

            StatsProgressDialog(self, self.dirname, lang_stats, num_files)
       
            self.stats = LangStatsCtrl(self, self.dirname, lang_stats)
            self.langpie = LangPieCtrl(self, lang_stats)            
       
            self.SetStatusText("Done.")
            self.sizer.Add(self.langpie, 1, wx.EXPAND)
            self.sizer.Add(self.stats, 1, wx.EXPAND)
            self.SetSizer(self.sizer)
            self.SetAutoLayout(True) 
            self.Layout()
        else:
            dialog.Destroy()

def main():
    locale.setlocale(locale.LC_ALL, '')
    app = wx.App(False)
    frame = PylocFrame(None, "PYLOC")
    frame.Show(True)
#    app.SetTopWindow(frame)
    app.MainLoop()

if __name__ == "__main__":
    main()

