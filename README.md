# Spark Project

## Overview

The aim of this project is to tackle the challenge of real-time analysis of data streams and enhance our practical skills in handling and analyzing streaming data. Our focus is on integrating Apache Spark Streaming, a fault-tolerant stream processing framework, with TextBlob, a Python-based natural language processing toolkit, to perform sentiment analysis on a data stream in real-time.

## Participants
- Ragi Bhatt
- Haolin Chen
- Irene Torrijos Robles

## Project structure
- `connect_newsapi_socket.py`: sends US top news headlines in JSON format to a Spark Streaming app every 2 minutes using the News API over a socket connection
- `spark_streaming.py`: performs the senitment anlysis, clustering into 3 groups
- `plot.ipynb`: visualizes the results using a scatter plot updated every second
- `output.csv`: stores the sentiment analysis results of the news articles and their corresponding cluster prediction labels

## Instructions

### Step 1: Acces to NewsAPI
To be able to access NewsAPI, you will need to create an account on NewsAPI following this link: https://newsapi.org/account. After this you will recieve an API key
![token](https://user-images.githubusercontent.com/37112474/235745202-43bb1135-5380-4aec-9cae-fee6d400c6c2.png)


### Step 2: Connecting to the API
Replace API_KEY in `connect_newsapi_socket.py` with your personal API key, this provides a user interface that guides you through the process of adding your credentials. After completing these steps for the first time, your credentials will be saved in.


### Step 3: Set up docker
Run this in the terminal:
`docker run --name sparklab -it --rm --user root -e GRANT_SUDO=yes \
-p 8888:8888 -p 4040:4040 -p 4041:4041 \
jupyter/pyspark-notebook`
Then, you have to connect via bash to the container:
`docker exec -it sparklab bash`


### Step 4: Start streaming 
Then copy the file `spark_streaming.py` to the image using command docker cp.

Then you just run the task in one terminal:
`% spark-submit spark_streaming.py localhost 9998`

## Methodology flow
![diagram-analysis](https://user-images.githubusercontent.com/37112474/235746437-61c83971-5fba-4f5d-b6a9-f5f4c0c08abe.png)

## Results
In addition to the obtained results, Spark Streaming and TextBlob work together to create a solid framework for real-time sentiment analysis of news data that has the potential to offer insightful analysis of evolving public sentiment patterns.

However, the clustered articles can not be considered as good clusters because the features used for clustering might not be enough. In addition to that ambiguous titles of news can heighten different emotions which are subjective to the user when exposed to the content.
