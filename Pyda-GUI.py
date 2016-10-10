#!/ usr/bin/python

import wx

class MyFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="Pyda",size=wx.Size(450,100))
		panel = wx.Panel(self)
		my_sizer = wx.BoxSizer(wx.VERTICAL)
		lbl = wx.StaticText(panel, label = "Hi")
		my_sizer.Add(lbl,0,wx.ALL,5)
		self.txt = wx.TextCtrl(panel,style=wx.TE_PROCESS_ENTER,size=(400,30))
		self.txt.SetFocus()
		self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
		my_sizer.Add(self.txt,0,wx.ALL,5)
		panel.SetSizer(my_sizer)
		self.Show(True)
		
	def OnEnter(self, event):
		input = self.txt.GetValue()
		input = input.lower()

if __name__ == '__main__':
	app = wx.App(True)
	frame = MyFrame()
	app.MainLoop()