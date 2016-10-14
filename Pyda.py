#!/ usr/bin/python

import wx, urllib2, wx.lib.scrolledpanel
from AutoWrapStaticText import AutoWrapStaticText
import json, StringIO
import wikipedia
import tungsten as wolframalpha


#Create frame template to report information to the user
class InformationFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, wx.GetApp().TopWindow, title="Results")


#Create main frame to ask user for question
class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="Pyda",size=wx.Size(450,100))
		panel = wx.Panel(self)
		my_sizer = wx.BoxSizer(wx.VERTICAL)
		#Add label and textbox for user to ask type a question
		lbl = wx.StaticText(panel, label = "Hi")
		my_sizer.Add(lbl,0,wx.ALL,5)
		self.txt = wx.TextCtrl(panel,style=wx.TE_PROCESS_ENTER,size=(400,30))
		self.txt.SetFocus()
		#Bind event for user typing in textbox
		self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
		my_sizer.Add(self.txt,0,wx.ALL,5)
		panel.SetSizer(my_sizer)
		#Show frame
		self.Show(True)


	#Arrays to store keywords for each integration
	wolframKeywords = ["solve","integrate","diffrentiate"]
	wikiKeywords = ["what is an","what is a","who is","who was","what is","what are","when was","where was"]
	weatherKeywords = ["weather","temperature","condition","forecast","radar","alerts","tides","currents","satellite","storm"]

	#Function to search integrated apis for data and post results in a new InformationFrame
	def GetData(self,input):
		resultsFrame = InformationFrame()
		panel = wx.lib.scrolledpanel.ScrolledPanel(resultsFrame)
		panel.SetBackgroundColour('white')
		panel.SetupScrolling()
		resultsSizer = wx.BoxSizer(wx.VERTICAL)
		numOfResults = 0
		resultsFrom = []
		if any(x in input for x in self.wolframKeywords) :
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
		if any(x in input for x in self.wikiKeywords) :
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
				summarySizer = wx.BoxSizer(wx.VERTICAL)
				lbl = AutoWrapStaticText(panel, label = summary)
				lbl.SetBackgroundColour('white')
				summarySizer.Add(lbl,0,wx.EXPAND|wx.ALL,5)
				resultsSizer.Add(summarySizer,0,wx.ALL|wx.EXPAND,5)
				numOfResults += 1
				resultsFrom.append('Wikipedia')
			except Exception as e:
				print e
		if any(x in input for x in self.weatherKeywords) :
			try:
				#Weather
				newInput = input
				for keyword in self.weatherKeywords:
					if keyword in newInput:
						newInput = newInput.replace(keyword,"")
						break
				newInput = newInput.title()
				apiKey = "203f287ba8cf5c5f"
				newInput = newInput.strip()
				f = urllib2.urlopen('http://api.wunderground.com/api/'+apiKey+'/geolookup/conditions/q/IA/'+newInput+'.json')
				#f = urllib2.urlopen('http://api.wunderground.com/api/'+apiKey+'/geolookup/conditions/q/IA/'+location+'.json')
				json_string = f.read()
				parsed_json = json.loads(json_string)
				location = parsed_json['location']['city']
				country = parsed_json['location']['country']
				temp_c = parsed_json['current_observation']['temp_c']
				summary = "Current temperature in %s, %s is: %s" % (location, country, temp_c)
				url = parsed_json['current_observation']['image']['url']
				sbuf = StringIO.StringIO(url)
				Image = wx.ImageFromStream(sbuf).ConvertToBitmap()
				image = wx.StaticBitmap(panel, wx.ID_ANY, Image, (Image.GetWidth(),Image.GetHeight()))

				f.close()



				resultsTitleSizer = wx.BoxSizer(wx.HORIZONTAL)
				resultsTitle = wx.StaticText(panel,label = 'Weather Results')
				resultsTitleSizer.Add(resultsTitle,0,wx.ALL|wx.EXPAND,5)
				resultsTitleSizer.Add(wx.StaticLine(panel,),0,wx.ALL|wx.EXPAND,5)
				resultsSizer.Add(resultsTitleSizer,0,wx.ALL|wx.EXPAND,5)
				summarySizer = wx.BoxSizer(wx.VERTICAL)
				lbl = AutoWrapStaticText(panel, label = summary)
				lbl.SetBackgroundColour('white')
				summarySizer.Add(lbl,0,wx.EXPAND|wx.ALL,5)
				resultsSizer.Add(summarySizer,0,wx.ALL|wx.EXPAND,5)
				resultsSizer.Add(image,0,wx.ALL|wx.EXPAND,5)
				numOfResults += 1
				resultsFrom.append('Weather')
			except Exception as e:
				print e
		panel.SetSizer(resultsSizer)
		resultsSizer.Fit(resultsFrame)
		resultsFrame.Show()

	def OnEnter(self, event):
		input = self.txt.GetValue()
		input = input.lower()
		self.GetData(input)


if __name__ == '__main__':
	app = wx.App(True)
	frame = MainFrame()
	#import wx.lib.inspection
	#wx.lib.inspection.InspectionTool().Show()
	app.MainLoop()
