from wx.lib.agw.piectrl import PieCtrl, PiePart
import pylocstats

def LangPieCtrl(PieCtrl):
    def __init__(self, parent, lang_stats):
    PieCtrl.__init__(self, parent, -1, wx.DefaultPosition, size=(400,600))
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

