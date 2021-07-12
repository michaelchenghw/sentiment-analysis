# Algorithmic Crowd Sentiment Analysis (ACSA)
**This algorithm aims to perform analysis and prediction of sentiment in the financial market through the use of web-scrapping, natural language processing and statistical tools.**

The fundemental rationale behind this project is to investigate the predictability of human sentiment, in particular crowd sentiment, from a data-driven perspective, and explore the application of such phenomenon in automated algorithmic trading.

This project is still in development.

## Tools
The algorithm is mainly implemented with Python.

## Web-scrapping
The algorithm currently focuses on analysing the sentiment of amateur individual investers in Hong Kong. Our training data are obtained from Facebook posts in the past 5 years published by finance-related pages, where date-sorted comments from individual users are scraped using the `request` and `beautiful_soup` library.

A list of the Facebook pages used:
1. "https://mobile.facebook.com/AAStocks.com.Limited/",
2. "https://mobile.facebook.com/80shing/"

## Natural Language Processing
After the training data have been collected, natural language processing is performed using the NLP model by IBM Watson. Each comment is assigned a sentiment score between -1.00 to 1.00, where higher scores indicate a more positve or optimistic sentiment and 0.00 indicates neutrality. All of the comments from each single day are then weighted and compiled to generate a daily sentiment index, also ranging between -1.0 to 1.0.

Currently, the evaluation procedure is implemented using the NLP model by IBM Watson

## Maximum Likelihood Estimation
After all the training data have been processed, the sentiment indices from every 2 consecutive days are joint to form a data pair (x,y), with x being the sentiment index on the first day and y being that on the second day. A probability distribution model is then developed using multinomial maximum likelihood estimation, where the sentiment indices are considered as random variables, with independent variable being x and dependent variable being y. The distribution model is represented with a 10×10 matrix.

## Markov Chain
The final test and prediction is achieved by the use of markov chain, where the evolution of the daily sentiment index is assumed to be a stochastic process that only depends on the index on the previous day. The sentiment on the present day is collected and processed in a way similar to that of the training data, except that the variation among the comments is taken into account, and the data is represented as a probability vector instead to represent the uncertainty.

After recursively transforming the vector with the probability distribution matrix, 7 vectors that represent the probability distribution of the sentiment index on the next 7 days are generated. This output may then be applied to other algorithmic trading models for further analysis.

## Results



## Conclusion and Insights

Below are several reasons that we believe led to low accuracy predictions by the model
1)	We assumed that sentiment scores of any 2 consecutive days must have a constant pattern which is very unlikely
2)	We assumed that the sentiment of the 2nd day only depends on the day before which is also unlikely
3)	There can always be more data used in training !! 


Insights:
From our research, we found out that sentiment scores range from -0.2 to 0.2. We believe this phenomenon arises because people view price changes differently. For example: when stock price increases, people who own Apple stock will gain, but for those who just sold their stock, they will feel bad or regretful. This contradictory emotion reflected in comments results in a neutral sentiment value.
Most importantly, we believe this poses a huge challenge in using NLP and sentiment analysis in stock price prediction as it requires biased and one-sided comments to give meaningful insight on future price movements.


## References and Documentation
1. https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all
2. https://requests.readthedocs.io/en/master/api/#requests.Response
3. https://docs.python.org/3/library/re.html#match-objects
4. https://docs.python.org/3/library/datetime.html
5. https://python.gotrained.com/scraping-facebook-posts-comments/
6. https://www.nltk.org/
7. https://www.w3schools.com/
8. https://ocw.mit.edu/courses/mathematics/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/lecture-notes/
9. https://www.cs.cornell.edu/courses/cs4780/2018fa/
