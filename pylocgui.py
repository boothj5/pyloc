#!/usr/bin/python
import wx
from wx.lib.agw.piectrl import PieCtrl, PiePart
import os
import locale
import pyloc

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600), style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN )
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_NOBORDER)

        self.pie = wx.Panel(self.splitter, -1) 
        self.text = wx.Panel(self.splitter, -1)

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

    def on_about(self, event):
        dialog = wx.MessageDialog(self, "Simple LOC counter", "About", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def on_exit(self, event):
        self.Close(True)

    def on_open_dir(self, event):
        self.dirname = ""
        dialog = wx.DirDialog(self, "Choose a directory")
        if dialog.ShowModal() == wx.ID_OK:
            self.dirname = dialog.GetPath()
        dialog.Destroy()
        self.lang_stats = {}
        pyloc.init_stats(self.dirname, self.lang_stats)

        self.result = "\n" + "PYLOC\n" + "-----\n"
        self.result = self.result + "Folder   : " + self.dirname + "\n\n"
        if not self.lang_stats:
            self.result = self.result + "Could not find any code!\n"
        else:
            self.result = self.result + pyloc.show_summary(self.lang_stats)
            self.result = self.result + pyloc.show_lang_stats(self.lang_stats)
        
        self.results = wx.TextCtrl(self.text, style=wx.TE_MULTILINE, size=wx.Size(400, 600))
        self.results.WriteText(self.result)
        self.results.SetEditable(False)

        self.mypie = PieCtrl(self.pie, -1, wx.DefaultPosition, wx.Size(400,600))

        self.mypie.GetLegend().SetTransparent(True)
        self.mypie.GetLegend().SetHorizontalBorder(10)
        self.mypie.GetLegend().SetWindowStyle(wx.STATIC_BORDER)
        self.mypie.GetLegend().SetLabelFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                                   wx.FONTSTYLE_NORMAL,
                                                   wx.FONTWEIGHT_NORMAL,
                                                   False, "Courier New"))
        self.mypie.GetLegend().SetLabelColour(wx.Colour(0, 0, 127))

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
        for lang in self.lang_stats:
            name = lang
            total = self.lang_stats[lang][pyloc.TOTAL_LINES]
            counts.append((name, total))

        sorted_counts = reversed(sorted(counts, key=lambda l: l[1]))

        for lang, count in sorted_counts:
            part = PiePart()
    
            lines = pyloc.format_thousands(count)
            part.SetLabel(lang + " (" + str(lines) + ")")
            part.SetValue(count)
            part.SetColour(colours[colour])
            colour = colour + 1
            self.mypie._series.append(part)
        
        
        self.splitter.SplitVertically(self.pie, self.text)


def main():
    locale.setlocale(locale.LC_ALL, 'en_US')

    app = wx.App(False)
    frame = MyFrame(None, "Pyloc")
    frame.Show(True)
    app.SetTopWindow(frame)
    app.MainLoop()

if __name__ == "__main__":
    main()

