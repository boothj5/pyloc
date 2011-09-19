#!/usr/bin/python
import wx
from math import radians
from wx.lib.agw.piectrl import PieCtrl, PiePart
import os
import locale
import pylocstats

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))

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
        dirname = ""
        dialog = wx.DirDialog(self, "Choose a directory")
        if dialog.ShowModal() == wx.ID_OK:
            dirname = dialog.GetPath()
        dialog.Destroy()
        self.sizer.DeleteWindows()
        lang_stats = {}
        
        pylocstats.init_stats(dirname, lang_stats)

        text = "\n" + "PYLOC\n" + "-----\n"
        text = text + "Folder   : " + dirname + "\n\n"
        if not lang_stats:
            text = text + "Could not find any code!\n"
        else:
            text = text + pylocstats.show_summary(lang_stats)
            text = text + pylocstats.show_lang_stats(lang_stats)
        
        self.stats = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(400,600))
        self.stats.WriteText(text)
        self.stats.SetEditable(False)

        self.langpie = PieCtrl(self, -1, wx.DefaultPosition, size=(400,600))
        self.langpie.SetAngle(radians(25))
        self.langpie.GetLegend().SetTransparent(True)
        self.langpie.GetLegend().SetHorizontalBorder(10)
        self.langpie.GetLegend().SetWindowStyle(wx.STATIC_BORDER)
        self.langpie.GetLegend().SetLabelFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                                   wx.FONTSTYLE_NORMAL,
                                                   wx.FONTWEIGHT_NORMAL,
                                                   False, "Courier New"))
        self.langpie.GetLegend().SetLabelColour(wx.Colour(0, 0, 127))

        colours = [ wx.Colour(200, 50, 50) ,
                    wx.Colour(50, 200, 50) ,
                    wx.Colour(50, 50, 200) ,
                    wx.Colour(100, 0, 200) ,
                    wx.Colour(200, 200, 0) ,
                    wx.Colour(0, 0, 200) ,
                    wx.Colour(200, 0, 200) ,
                    wx.Colour(0, 200, 200) ,
                    wx.Colour(0, 0, 50) ,
                    wx.Colour(0, 50, 0) ]
        
        colour = 0
        counts = []
        for lang in lang_stats:
            name = lang
            total = lang_stats[lang][pylocstats.TOTAL_LINES]
            counts.append((name, total))

        sorted_counts = reversed(sorted(counts, key=lambda l: l[1]))

        for lang, count in sorted_counts:
            part = PiePart()
    
            lines = pylocstats.format_thousands(count)
            part.SetLabel(lang + " (" + str(lines) + ")")
            part.SetValue(count)
            part.SetColour(colours[colour])
            colour = colour + 1
            self.langpie._series.append(part)
        
        self.sizer.Add(self.langpie, 1, wx.EXPAND | wx.ALIGN_LEFT)
        self.sizer.Add(self.stats, 1, wx.EXPAND | wx.ALIGN_RIGHT)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1) 
        self.sizer.Fit(self)
        self.Layout()

def main():
    locale.setlocale(locale.LC_ALL, '')
    app = wx.App(False)
    frame = MyFrame(None, "Pyloc")
    frame.Show(True)
#    app.SetTopWindow(frame)
    app.MainLoop()

if __name__ == "__main__":
    main()

