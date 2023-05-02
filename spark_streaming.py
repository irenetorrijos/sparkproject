import sys
import json
import re
import os
import pandas as pd
from textblob import TextBlob
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.mllib.clustering import StreamingKMeans
from pyspark.mllib.linalg import Vectors


# Function to get sentiment from the text
def sentiment_analysis(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return [polarity, subjectivity]

# Function to process the message and get sentiment scores
def analyze_sentiments(message):
    message = json.loads(message.strip(), strict=False)
    try:
        title = message['title']
        content = message['content']

        sentiment = sentiment_analysis(title + '. ' + content)
    except:
        title = message['title']
        sentiment = sentiment_analysis(title)
    return {'title': title, 'sentiment': sentiment}

# Function to process the stream and get sentiment data
def process_stream_data(stream):
    windowed_stream = stream.window(60, 1)
    sentiments = windowed_stream.map(analyze_sentiments)
    vectorized_sentiments = sentiments.map(lambda x: ((x['title'], x['sentiment']), Vectors.dense(x['sentiment'])))
    return vectorized_sentiments
    
# Function to save predictions to a CSV file
def save_predictions_to_csv(rdd):
    rdd_data = rdd.collect()
    data = [[title, sentiment[0], sentiment[1], prediction] for (title, sentiment), prediction in rdd_data]
    df = pd.DataFrame(data, columns=['title', 'polarity', 'subjectivity', 'prediction'])
    df.to_csv('output.csv', index=False)

# Function to clean the text message
def clean_message(text):
    text = re.sub(r'@[\S]+', '', text)
    text = re.sub(r':[a-z]+:', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: spark_streaming.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)

    spark_context = SparkContext(appName="NewsAnalysis")
    spark_context.setLogLevel("ERROR")
    streaming_context = StreamingContext(spark_context, 1)

    input_stream = streaming_context.socketTextStream(sys.argv[1], int(sys.argv[2]))

    sentiments = process_stream_data(input_stream)

    kmeans_model = StreamingKMeans(k=3, decayFactor=0.1).setRandomCenters(2, 0.01, 2023)
    training_data = sentiments.map(lambda x: x[1])
    kmeans_model.trainOn(training_data)

    kmeans_predictions = kmeans_model.predictOnValues(sentiments)

    kmeans_predictions.foreachRDD(save_predictions_to_csv)

    streaming_context.start()
    streaming_context.awaitTermination()