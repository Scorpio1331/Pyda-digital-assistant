import wx 

class AutoWrapStaticText(wx.PyControl): 
    def __init__(self, parent, id=0, label="", 
                 pos=wx.DefaultPosition, size=wx.DefaultSize, 
                 style=0, name="wrapStatText"): 
        wx.PyControl.__init__(self, parent, id, pos, size, wx.NO_BORDER, 
                              wx.DefaultValidator, name) 
        self.st = wx.StaticText(self, 0, label, style=style) 
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
