# Spark Project

## Overview

The aim of this project is to tackle the challenge of real-time analysis of data streams and enhance our practical skills in handling and analyzing streaming data. Our focus is on integrating Apache Spark Streaming, a fault-tolerant stream processing framework, with TextBlob, a Python-based natural language processing toolkit, to perform sentiment analysis on a data stream in real-time.

## Participants
- Ragi Bhatt
- Haolin Chen
- Irene Torrijos Robles

## Project structure
- 'connect_newsapi_socket.py': sends US top news headlines in JSON format to a Spark Streaming app every 2 minutes using the News API over a socket connection
- `spark_streaming.py`: performs the senitment anlysis, clustering into 3 groups
- `plot.ipynb`: visualizes the results using a scatter plot updated every second
- `output.csv`: stores the sentiment analysis results of the news articles and their corresponding cluster prediction labels
