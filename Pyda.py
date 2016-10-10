#!/ usr/bin/python

import wx, urllib2, wx.lib.scrolledpanel
import AutoWrapStaticText
import json, StringIO
import wikipedia
import tungsten as wolframalpha


class InformationFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, wx.GetApp().TopWindow, title="Results")
		
		

class MainFrame(wx.Frame):
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
		
	
		#wikiList = ["who is","what is"]
		#try:
		#	resultsFrame = InformationFrame()
		#	panel = wx.lib.scrolledpanel.ScrolledPanel(resultsFrame)
		#	panel.SetBackgroundColour('white')
		#	panel.SetupScrolling()
		#	resultsSizer = wx.BoxSizer(wx.VERTICAL)
		#	if any(char.isdigit() for char in str(input)):
		#		#Wolfram Alpha
		#		app_id = "A8TXGT-9LYUXTY4PK"
		#		client = wolframalpha.Tungsten(app_id)
		#		res = client.query(input)
		#		if res.error:
		#			raise QueryError('Query unsuccessful')
		#		for pod in res.pods:		
		#			my_sizer = wx.BoxSizer(wx.HORIZONTAL)
		#			lbl = wx.StaticText(panel, label = (pod.title + ': '))
		#			lbl.Wrap()
		#			my_sizer.Add(lbl,0,wx.ALL|wx.EXPAND,5)
		#			buf = urllib2.urlopen(pod.format['img'][0]['url']).read()
		#			sbuf = StringIO.StringIO(buf)
		#			Image = wx.ImageFromStream(sbuf).ConvertToBitmap()
		#			image = wx.StaticBitmap(panel, wx.ID_ANY, Image, (Image.GetWidth(),Image.GetHeight()))
		#			my_sizer.Add(image,0,wx.ALL|wx.EXPAND,5)
		#			resultsSizer.Add(my_sizer,0,wx.ALL|wx.EXPAND,5)
		#			resultsSizer.Add(wx.StaticLine(panel,),0,wx.ALL|wx.EXPAND,5)						
#
#			elif any(x in input for x in wikiList):
#				input = input[7:]
#				#Wikipedia
#				my_sizer = wx.BoxSizer(wx.HORIZONTAL)
#				lbl = wx.StaticText(panel, label = wikipedia.summary(input))
#				my_sizer.Add(lbl,0,wx.ALL|wx.EXPAND,5)
#				resultsSizer.Add(my_sizer,0,wx.ALL|wx.EXPAND,5)
					
		#	panel.SetSizer(resultsSizer)
		#	resultsSizer.Fit(resultsFrame)
		#	resultsFrame.Show()
		#except Exception as e:
		#	print "Failed: ", e
			
			
	wolframKeywords = ["solve","integrate","diffrentiate"]
	wikiKeywords = ["what is an","what is a","who is","what is","what are","when was","where was"]
	weatherKeywords = ["weather","temperature","condition","forecast","radar","alerts","tides","currents","satellite","storm"]

	def GetData(self,input):
		resultsFrame = InformationFrame()
		panel = wx.lib.scrolledpanel.ScrolledPanel(resultsFrame)
		panel.SetBackgroundColour('white')
		panel.SetupScrolling()
		resultsSizer = wx.BoxSizer(wx.VERTICAL)
		numOfResults = 0
		resultsFrom = []
		try:
			#Wolfram Alpha
			app_id = "A8TXGT-9LYUXTY4PK"
			client = wolframalpha.Tungsten(app_id)
			res = client.query(input)
			if res.error:
				raise QueryError('Query unsuccessful')
			resultsTitleSizer = wx.BoxSizer(wx.HORIZONTAL)
			resultsTitle = wx.StaticText(panel,label = 'Wolfram Alpha Results')
			resultsTitleSizer.Add(resultsTitle,0,wx.ALL|wx.EXPAND,5)
			resultsTitleSizer.Add(wx.StaticLine(panel,),0,wx.ALL|wx.EXPAND,5)
			resultsSizer.Add(resultsTitleSizer,0,wx.ALL|wx.EXPAND,5)
			for pod in res.pods:		
				my_sizer = wx.BoxSizer(wx.HORIZONTAL)
				lbl = wx.StaticText(panel, label = (pod.title + ': '))
				my_sizer.Add(lbl,0,wx.ALL|wx.EXPAND,5)
				buf = urllib2.urlopen(pod.format['img'][0]['url']).read()
				sbuf = StringIO.StringIO(buf)
				Image = wx.ImageFromStream(sbuf).ConvertToBitmap()
				image = wx.StaticBitmap(panel, wx.ID_ANY, Image, (Image.GetWidth(),Image.GetHeight()))
				my_sizer.Add(image,0,wx.ALL|wx.EXPAND,5)
				resultsSizer.Add(my_sizer,0,wx.ALL|wx.EXPAND,5)
				resultsSizer.Add(wx.StaticLine(panel,),0,wx.ALL|wx.EXPAND,5)
			numOfResults += 1
			resultsFrom.append('WolframAlpha')
		except Exception:
			pass
			
		try:
			#Wikipedia
			newInput = input
			for keyword in self.wikiKeywords:
				if keyword in newInput:
					newInput = newInput.replace(keyword,"")
					break
			summary = ""
			if numOfResults > 0:
				summary = wikipedia.summary(newInput,sentences = 6)
			else:
				summary = wikipedia.summary(newInput)
			resultsTitleSizer = wx.BoxSizer(wx.HORIZONTAL)
			resultsTitle = wx.StaticText(panel,label = 'Wikipedia Results')
			resultsTitleSizer.Add(resultsTitle,0,wx.ALL|wx.EXPAND,5)
			resultsTitleSizer.Add(wx.StaticLine(panel,),0,wx.ALL|wx.EXPAND,5)
			resultsSizer.Add(resultsTitleSizer,0,wx.ALL|wx.EXPAND,5)
			
			summarySizer = wx.BoxSizer(wx.HORIZONTAL)
			lbl = AutoWrapStaticText(panel, label = summary)
			summarySizer.Add(lbl,0,wx.EXPAND|wx.ALL,5)
			resultsSizer.Add(summarySizer,0,wx.ALL|wx.EXPAND,5)
			
			numOfResults += 1
			resultsFrom.append('Wikipedia')
		except Exception as e:
			print e
		panel.SetSizer(resultsSizer)
		resultsSizer.Fit(resultsFrame)
		resultsFrame.Show()

	def OnEnter(self, event):
		input = self.txt.GetValue()
		input = input.lower()
		self.GetData(input)


class AutoWrapStaticText(wx.PyControl): 
    def __init__(self, parent, id=0, label="", 
                 pos=wx.DefaultPosition, size=wx.DefaultSize, 
                 style=0, name="wrapStatText"): 
        wx.PyControl.__init__(self, parent, id, pos, size, wx.NO_BORDER, 
                              wx.DefaultValidator, name) 
        self.st = wx.StaticText(self, 0, label, style=style)
        self.BackgroundColour = 'white'
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
        self.st.Wrap(parent.GetSize().width) 
        self.st.Thaw() 

    def DoGetBestSize(self): 
        # this should return something meaningful for what the best 
        # size of the widget is, but what that size should be while we 
        # still don't know the actual width is still an open 
        # question...  Just return a dummy value for now. 
        return wx.Size(100,100) 


if __name__ == '__main__':
	app = wx.App(True)
	frame = MainFrame()
	app.MainLoop()