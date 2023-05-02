import requests  # Import the requests library for making HTTP requests
import time  # Import the time library for sleep function
import json  # Import the json library for working with JSON data
import socket  # Import the socket library for socket programming

# Define the API key and port number as constants
API_KEY = '80798de4fad04b5583a808a00442ab54'
PORT_NUMBER = 9998


# Create a new server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the server socket to the specified address and port
server.bind(('localhost', PORT_NUMBER))
# Listen for incoming connections
server.listen(1)
print("Waiting...")

# Accept the incoming connection and get the client socket
client, address = server.accept()
print("Spark Streaming application connected to the server!")

# Infinite loop
while True:
    # Construct the API URL using the API key
    api_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey={}".format(API_KEY)
    # Make an HTTP GET request to the API URL
    api_response = requests.get(api_url)
    # Parse the JSON response and return the 'articles' list
    json_data = api_response.json()

    fetched_articles = json_data['articles']
    # Iterate through the articles
    for single_article in fetched_articles:
        print(single_article)
        # Convert the article to a JSON string
        json_message = json.dumps(single_article)
        # Send the JSON string to the client
        client.send((json_message + '\n').encode('utf-8'))
        print("Message sent :\n", json_message)
        # Wait for 1 second before sending the next message
        time.sleep(1)

    # Wait for 2 minutes before fetching the articles again
    time.sleep(120)

