import wikipedia
import tungsten as wolframalpha


wolframKeywords = ["solve", "equation","integrate","diffrentiate"]
wikiKeywords = ["what is an","what is a","who is","what is","what are","when was","where was"]
weatherKeywords = ["weather","temperature","condition","forecast","radar","alerts","tides","currents","satellite","storm"]

while True:
	input = raw_input("Q: ")
	try:
		if any(x in input for x in wikiKeywords) and not input.__contains__("what is the"):
			#Wikipedia
			for keyword in wikiKeywords:
				if keyword in input:
					input = input.replace(keyword,"")
					print input
					break;
			print wikipedia.summary(input)
		elif any(x in input for x in weatherKeywords):
			print "weather"
		elif any(x in input for x in wolframKeywords) or any (char.isdigit() for char in str(input)):
			#Wolfram Alpha
			print input
			app_id = "A8TXGT-9LYUXTY4PK"
			client = wolframalpha.Tungsten(app_id)
			res = client.query(input)
			podsList = res.pods
			for pod in podsList:
				print pod.title
			answer = next(res.results)
			print(answer)
	except Exception as e:
		print 'Failed: ', e

