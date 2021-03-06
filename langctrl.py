#
# langctrl.py
#
# Copyright (C) 2011, 2012 James Booth <boothj5@gmail.com>
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

import wx
import os
from math import radians
from wx.lib.agw.piectrl import PieCtrl, PiePart
from languages import *
import pylocstats

class StatsProgressDialog(wx.ProgressDialog):
    def __init__(self, parent, dirname, lang_stats, num_files):
        wx.ProgressDialog.__init__(self, "PYLOC Scan",
                                   "Scanning source files...",
                                    maximum = num_files,
                                    parent=parent,
                                    style = wx.PD_APP_MODAL
                                    #| wx.PD_ELAPSED_TIME
                                    | wx.PD_AUTO_HIDE
                                    #| wx.PD_ESTIMATED_TIME
                                    | wx.PD_REMAINING_TIME
                                   )

class LangStatsCtrl(wx.TextCtrl):
    def __init__(self, parent, dirname, lang_stats):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE)
        text = "Folder   : " + dirname + "\n\n"
        if not lang_stats:
            text += "Could not find any code!\n"
        else:
            text += pylocstats.show_summary(lang_stats)
            text += pylocstats.show_lang_stats(lang_stats)

        self.WriteText(text)
        self.SetEditable(False)


class LangPieCtrl(PieCtrl):
    def __init__(self, parent, lang_stats):
        PieCtrl.__init__(self, parent, -1, wx.DefaultPosition)
        self.SetAngle(radians(25))
        self.GetLegend().SetTransparent(True)
        self.GetLegend().SetHorizontalBorder(10)
        self.GetLegend().SetWindowStyle(wx.STATIC_BORDER)
        self.GetLegend().SetLabelFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                                  wx.FONTSTYLE_NORMAL,
                                                  wx.FONTWEIGHT_NORMAL,
                                                  False, "Courier New"))
        self.GetLegend().SetLabelColour(wx.Colour(0, 0, 127))

        colours = [ wx.Colour(200, 50, 50) ,
                    wx.Colour(50, 200, 50) ,
                    wx.Colour(50, 50, 200) ,
                    wx.Colour(100, 0, 200) ,
                    wx.Colour(200, 200, 0) ,
                    wx.Colour(0, 0, 200) ,
                    wx.Colour(200, 0, 200) ,
                    wx.Colour(0, 200, 200) ,
                    wx.Colour(0, 0, 50) ,
                    wx.Colour(0, 25, 50) ,
                    wx.Colour(25, 0, 50) ,
                    wx.Colour(0, 100, 50) ,
                    wx.Colour(175, 175, 50) ,
                    wx.Colour(50, 100, 175) ,
                    wx.Colour(175, 100, 175) ,
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
            self._series.append(part)

