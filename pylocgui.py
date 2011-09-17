#!/usr/bin/python
import wx
import os
import locale
import pyloc

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()

        filemenu = wx.Menu()
#        menu_open_file = filemenu.Append(wx.ID_OPEN, "&Open File", " Open a file")
        menu_open_dir = filemenu.Append(wx.ID_ANY, "Open &Directory", " Open a directory")
        filemenu.AppendSeparator()
        menu_about = filemenu.Append(wx.ID_ABOUT, "&About", " About Pyloc")
        filemenu.AppendSeparator()
        menu_exit = filemenu.Append(wx.ID_EXIT, "E&xit", " Exit Pyloc")

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)       

#        self.Bind(wx.EVT_MENU, self.on_open_file, menu_open_file)
        self.Bind(wx.EVT_MENU, self.on_open_dir, menu_open_dir)
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)

        self.Show(True)

    def on_about(self, event):
        dialog = wx.MessageDialog(self, "Simple LOC counter", "About", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def on_exit(self, event):
        self.Close(True)

#    def on_open_file(self, event):
#        self.dirname = "" 
#        dialog = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
#        if dialog.ShowModal() == wx.ID_OK:
#            self.filename = dialog.GetFilename()
#            self.dirname = dialog.GetDirectory()
#            f = open(os.path.join(self.dirname, self.filename), 'r')
#            self.control.SetValue(f.read())
#            f.close()
#        dialog.Destroy()

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
            self.result = self.result + pyloc.show_lang_stats(self.lang_stats)
            self.result = self.result + pyloc.show_summary(self.lang_stats)
       
        self.control.SetValue(self.result)

def main():
    locale.setlocale(locale.LC_ALL, 'en_US')

    app = wx.App(False)
    frame = MyFrame(None, "Pyloc")
    app.MainLoop()

if __name__ == "__main__":
    main()

