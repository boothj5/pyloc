#!/usr/bin/python
from languages import *
import wx
from langctrl import LangPieCtrl, LangStatsCtrl, StatsProgressDialog
import wx.lib.agw.pyprogress as Progress
import os
import locale
from pylocstats import init_stats, calc_total, format_thousands

class PylocFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000,800))

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
            progressDlg = StatsProgressDialog(self, self.dirname, lang_stats, num_files)

            for count in init_stats(self.dirname, lang_stats):
                progressDlg.Update(count)

            progressDlg.Destroy()
            total = calc_total(lang_stats)
            formatted_total = format_thousands(total)
            self.SetStatusText("Done.")

            # left
            self.langpie = LangPieCtrl(self, lang_stats)            

            # right
            self.rightpanel = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)

            # right top    
            self.totaltext = wx.StaticText(self.rightpanel, -1, "Total Physical LOC: " + formatted_total, style=wx.ALIGN_CENTRE)
            # right middle
            self.langchooserpanel = wx.Panel(self.rightpanel, -1, style=wx.SIMPLE_BORDER)
            # right bottom
            self.stats = LangStatsCtrl(self.rightpanel, self.dirname, lang_stats)

            # set up right sizer, and layout right panel
            rightsizer = wx.BoxSizer(wx.VERTICAL)
            rightsizer.Add(self.totaltext, 1, wx.CENTRE)
            rightsizer.Add(self.langchooserpanel, 1, wx.EXPAND)
            rightsizer.Add(self.stats, 10, wx.EXPAND)
            self.rightpanel.SetAutoLayout(True)
            self.rightpanel.SetSizer(rightsizer)
            self.rightpanel.Layout()

            # set up main sizer, with left and right and layout
            self.sizer.Add(self.langpie, 1, wx.EXPAND)
            self.sizer.Add(self.rightpanel, 1, wx.EXPAND)
            self.SetAutoLayout(True) 
            self.SetSizer(self.sizer)
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

