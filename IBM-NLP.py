import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions

authenticator = IAMAuthenticator('skuPbK5fq1SjLiN8cjGRciofFUKpRe7qKiOzdlCtMdbR')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/7f147e68-bdc7-494a-bcf9-73d1cdfae099')



#Process comments extracted:

data = {}

file = open("comments.txt", "r")
comments = file.read().splitlines()

count = 0 
for comment in comments:
    text = comment.split(":")[1]
    for i in range (len(text)):
        if (text[i] == ":"):
            text[i] = "-"

    if comment == "\n":
        continue
    info = comment.split(":")
    date = info[0]
    text = info[1]
    if (date not in data):
        data[date] = [text]
    else:
        data[date].append(text)


file.close()
    

# Sample comments
#comments = {"date1":["Apple is a doing great" , "Microsoft is not doing well today"], "date2":["Microsoft is bad", "Apple is doing wonderful"]} # Sample comments
emotions = {}
datasets = []

for i in data:
  for j in data[i]:
    try: 
        print (j)
        sentimentresponse = natural_language_understanding.analyze(text = j, features=Features(sentiment=SentimentOptions())).get_result()
        sentiment = sentimentresponse['sentiment']['document']['score'] # Sentiment analysis of the comment with target = entity 
        if i not in emotions:
            emotions[i] = [sentiment]
        else:
            emotions[i].append(sentiment)
    except Exception:
        continue


for i in emotions:   
  average = sum(emotions[i])/len(emotions[i])   #Compute the average of sentiments values as the final sentiment of the entity
  dataset = []
  dataset.append(i)
  dataset.append(average)
  datasets.append(dataset)

file = open("sentiments.txt","w")
for i in datasets:
    print(i)
    file.write(str(i[0]) + "," + str(i[1]) + "\n")
