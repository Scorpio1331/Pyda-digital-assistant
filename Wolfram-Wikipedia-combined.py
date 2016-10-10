import wikipedia, wolframalpha

while True:
	input = raw_input("Q: ")
	
	try:
		#Wolfram Alpha
		app_id = "A8TXGT-9LYUXTY4PK"
		client = wolframalpha.Client(app_id)
		res = client.query(input)
		answer = next(res.results).text
		print(answer)
	except:
		#Wikipedia
		print wikipedia.summary(input, sentences=6hon)