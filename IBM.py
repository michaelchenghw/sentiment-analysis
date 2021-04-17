pip install --upgrade "ibm-watson>=5.1.0"


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

# Sample comments
comments = {"date1":["Apple is a doing great" , "Microsoft is not doing well today"], "date2":["Microsoft is bad", "Apple is doing wonderful"]} # Sample comments
emotions = {}

for i in comments:
  for j in comments[i]:
    print (j)
    entityresponse = natural_language_understanding.analyze(text = j, features=Features(entities=EntitiesOptions(limit=1))).get_result()
    entity = entityresponse['entities'][0]['text'] # Entity recognition of the string
    sentimentresponse = natural_language_understanding.analyze(text = j, features=Features(sentiment=SentimentOptions(targets=[entity]))).get_result()
    sentiment = sentimentresponse['sentiment']['targets'][0]['score'] # Sentiment analysis of the comment with target = entity 
    if entity.upper() not in emotions:
      emotions[entity.upper()] = [sentiment]
    else:
      emotions[entity.upper()].append(sentiment) 


for i in emotions:        
  emotions[i] = sum(emotions[i])/len(emotions[i])   #Compute the average of sentiments values as the final sentiment of the entity

for i in emotions:
  print(i)
  print (emotions[i])
 
