import wolframalpha

input = raw_input("Q: ")
app_id = "A8TXGT-9LYUXTY4PK"
client = wolframalpha.Client(app_id)

res = client.query(input)
answer = next(res.results).text

print(answer)