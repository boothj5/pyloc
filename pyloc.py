#!/usr/bin/python
from languages import *
import wx
from math import radians
from wx.lib.agw.piectrl import PieCtrl, PiePart
import wx.lib.agw.pyprogress as Progress
import os
import locale
import pylocstats

class MyFrame(wx.Frame):
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
            dlg = wx.ProgressDialog("PYLOC Scan",
                                    "Scanning source files...",
                                    maximum = num_files,
                                    parent=self,
                                    style = wx.PD_APP_MODAL
                                    #| wx.PD_ELAPSED_TIME
                                    | wx.PD_AUTO_HIDE
                                    #| wx.PD_ESTIMATED_TIME
                                    | wx.PD_REMAINING_TIME
                                   )
 
            count = 0
 
            for directory, dirnames, filenames in os.walk(self.dirname):
                for filename in filenames:
                    count += 1
                    dlg.Update(count)
                    basename, extension = os.path.splitext(filename)
                    for lang in languages:
                        if extension in languages[lang][EXTENSIONS]:
                            if not lang in lang_stats:
                                lang_stats[lang] = { pylocstats.SRC_FILES: 0 ,
                                                     pylocstats.CODE_LINES: 0 ,
                                                     pylocstats.COMM_LINES: 0 ,
                                                     pylocstats.WHITESPACE: 0 ,
                                                     pylocstats.TOTAL_LINES: 0 }
                            lang_stats[lang][pylocstats.SRC_FILES] = lang_stats[lang][pylocstats.SRC_FILES] + 1
                            pylocstats.process_file(directory + "/" + filename, lang, lang_stats)


            dlg.Destroy()
            text = "Folder   : " + self.dirname + "\n\n"
            if not lang_stats:
                text += "Could not find any code!\n"
            else:
                text += pylocstats.show_summary(lang_stats)
                text += pylocstats.show_lang_stats(lang_stats)
        
            self.stats = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(400,600))
            self.stats.WriteText(text)
            self.stats.SetEditable(False)

            self.langpie = create_langpie(self, lang_stats)            
       
            self.SetStatusText("Done.")
            self.sizer.Add(self.langpie, 1, wx.EXPAND | wx.ALIGN_LEFT)
            self.sizer.Add(self.stats, 1, wx.EXPAND | wx.ALIGN_RIGHT)
            self.SetSizer(self.sizer)
            self.SetAutoLayout(1) 
            self.sizer.Fit(self)
            self.Layout()
        else:
            dialog.Destroy()

def create_langpie(parent, lang_stats):
    langpie = PieCtrl(parent, -1, wx.DefaultPosition, size=(400,600))
    langpie.SetAngle(radians(25))
    langpie.GetLegend().SetTransparent(True)
    langpie.GetLegend().SetHorizontalBorder(10)
    langpie.GetLegend().SetWindowStyle(wx.STATIC_BORDER)
    langpie.GetLegend().SetLabelFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                                 wx.FONTSTYLE_NORMAL,
                                                 wx.FONTWEIGHT_NORMAL,
                                                 False, "Courier New"))
    langpie.GetLegend().SetLabelColour(wx.Colour(0, 0, 127))

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
        langpie._series.append(part)

    return langpie
    
def main():
    locale.setlocale(locale.LC_ALL, '')
    app = wx.App(False)
    frame = MyFrame(None, "PYLOC")
    frame.Show(True)
#    app.SetTopWindow(frame)
    app.MainLoop()

if __name__ == "__main__":
    main()

