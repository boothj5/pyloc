#!/usr/bin/python
# 
# pyloc.py
#
# Copyright (C) 2012 James Booth <boothj5@gmail.com>
# 
# This file is part of Pyloc.
#
# Pyloc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyloc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyloc.  If not, see <http://www.gnu.org/licenses/>.

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

        # setup menus
        filemenu = wx.Menu()
        menu_open_dir = filemenu.Append(wx.ID_ANY, "Open &Directory", " Open a directory")
        filemenu.AppendSeparator()
        menu_about = filemenu.Append(wx.ID_ABOUT, "&About", " About Pyloc")
        filemenu.AppendSeparator()
        menu_exit = filemenu.Append(wx.ID_EXIT, "E&xit", " Exit Pyloc")

        # add menubar
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)       

        # bind menu events to handlers
        self.Bind(wx.EVT_MENU, self.on_open_dir, menu_open_dir)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)

        # main sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

    def on_about(self, event):
        dialog = wx.MessageDialog(self, "Simple LOC counter", "About", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def on_exit(self, event):
        self.Close(True)

    def on_open_dir(self, event):

        # show dialog to choose directory
        dialog = wx.DirDialog(self, "Choose a directory", self.dirname)
        action = dialog.ShowModal() 

        # if directory chosen
        if action == wx.ID_OK:
            self.SetStatusText("Preparing...")
            self.dirname = dialog.GetPath()
            dialog.Destroy()

            # clear the main sizer
            self.sizer.DeleteWindows()

            # get lang stats showing progress
            lang_stats = {}
            num_files = sum((len(f) for _, _, f in os.walk(self.dirname)))
            self.SetStatusText("Scanning...")
            progressDlg = StatsProgressDialog(self, self.dirname, lang_stats, num_files)

            for count in init_stats(self.dirname, lang_stats):
                progressDlg.Update(count)

            progressDlg.Destroy()
            self.SetStatusText("Done.")

            # calculate total PhyLOC
            total = calc_total(lang_stats)
            formatted_total = format_thousands(total)

            # set up controls
            self.langpie = LangPieCtrl(self, lang_stats)            
            self.rightpanel = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)

            # right panel controls
            self.summarypanel = wx.Panel(self.rightpanel, -1, style=wx.NO_BORDER)
            self.langchooserpanel = wx.Panel(self.rightpanel, -1, style=wx.NO_BORDER)
            self.stats = LangStatsCtrl(self.rightpanel, self.dirname, lang_stats)

            # summary panel text controls
            self.dirlabel = wx.StaticText(self.summarypanel, -1, 
                                          "Directory: ", style=wx.ALIGN_CENTRE)
            self.dirvalue = wx.StaticText(self.summarypanel, -1,
                                          self.dirname, style=wx.ALIGN_CENTRE)
            self.totallabel = wx.StaticText(self.summarypanel, -1, 
                                            "Total Physical LOC: ", style=wx.ALIGN_CENTRE)
            self.totalvalue = wx.StaticText(self.summarypanel, -1, 
                                            formatted_total, style=wx.ALIGN_CENTRE)


            # set up and layout summary panel sizer
            summarysizer = wx.GridSizer(2,2, 5, 5)
            summarysizer.Add(self.dirlabel, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALIGN_LEFT)
            summarysizer.Add(self.dirvalue, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALIGN_LEFT)
            summarysizer.Add(self.totallabel, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALIGN_LEFT)
            summarysizer.Add(self.totalvalue, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALIGN_LEFT)
            self.summarypanel.SetAutoLayout(True)
            self.summarypanel.SetSizer(summarysizer)
            self.summarypanel.Layout()

            # set up and layout right panel sizer
            rightsizer = wx.BoxSizer(wx.VERTICAL)
            rightsizer.Add(self.summarypanel, 1, wx.CENTRE)
            rightsizer.Add(self.langchooserpanel, 1, wx.EXPAND)
            rightsizer.Add(self.stats, 10, wx.EXPAND)
            self.rightpanel.SetAutoLayout(True)
            self.rightpanel.SetSizer(rightsizer)
            self.rightpanel.Layout()

            # set up and layout main sizer
            self.sizer.Add(self.langpie, 1, wx.EXPAND)
            self.sizer.Add(self.rightpanel, 1, wx.EXPAND)
            self.SetAutoLayout(True) 
            self.SetSizer(self.sizer)
            self.Layout()

        # if cancel chosen
        else:
            dialog.Destroy()

def main():
    locale.setlocale(locale.LC_ALL, '')
    app = wx.App(False)
    frame = PylocFrame(None, "PYLOC")
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()

