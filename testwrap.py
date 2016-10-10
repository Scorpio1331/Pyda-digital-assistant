import wx



class TestFrame(wx.Frame): 
    def __init__(self):
        wx.Frame.__init__(self, None, title="test",size=wx.Size(450,100))
        p = wx.Panel(self)
        try:
            box = wx.StaticBox(p, -1, "AutoWrapStaticText") 
            sbs = wx.StaticBoxSizer(box, wx.VERTICAL) 
            awst = AutoWrapStaticText(p, label='test') 
            sbs.Add(awst, 1, wx.EXPAND) 
            sizer = wx.BoxSizer(wx.HORIZONTAL) 
            sizer.Add(sbs, 1, wx.EXPAND|wx.ALL, 25) 
            p.SetSizer(sizer) 
        except Exception as e:
            print e
        self.Show(True)


class AutoWrapStaticText(wx.PyControl): 
    def __init__(self, parent, id=0, label="", 
                 pos=wx.DefaultPosition, size=wx.DefaultSize, 
                 style=0, name="wrapStatText"): 
        wx.PyControl.__init__(self, parent, id, pos, size, wx.NO_BORDER, 
                              wx.DefaultValidator, name) 
        self.st = wx.StaticText(self, -1, label, style=style) 
        self._label = label # save the unwrapped text 
        self._Rewrap() 
        self.Bind(wx.EVT_SIZE, self.OnSize) 
        

    def SetLabel(self, label): 
        self._label = label 
        self._Rewrap() 
    def GetLabel(self): 
        return self._label 

    def SetFont(self, font): 
        self.st.SetFont(font) 
        self._Rewrap() 
    def GetFont(self): 
        return self.st.GetFont() 


    def OnSize(self, evt): 
        self.st.SetSize(self.GetSize()) 
        self._Rewrap() 

    def _Rewrap(self): 
        self.st.Freeze() 
        self.st.SetLabel(self._label) 
        self.st.Wrap(self.GetSize().width) 
        self.st.Thaw() 

    def DoGetBestSize(self): 
        # this should return something meaningful for what the best 
        # size of the widget is, but what that size should be while we 
        # still don't know the actual width is still an open 
        # question...  Just return a dummy value for now. 
        return wx.Size(100,100) 
 


app = wx.App(True)
frame = TestFrame()
#import wx.lib.inspection
#wx.lib.inspection.InspectionTool().Show() 
app.MainLoop()