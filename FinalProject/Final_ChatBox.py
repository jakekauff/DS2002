"""
Jakob Kauffmann 
DS 2002
Final Project: import data from mongo and answer questions with chatbox
"""

import nltk 
nltk.download('punkt')

from nltk import word_tokenize,sent_tokenize

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
#read more on the steamer https://towardsdatascience.com/stemming-lemmatization-what-ba782b7c0bd8
import numpy as np 
import tensorflow
import tflearn

import random
import json
import pickle
import pandas as pd
from pymongo import MongoClient

client = MongoClient()

#point the client at mongo URI
client = MongoClient('localhost', 27017)
#select database
db = client['FinalProject']
#select the collection within the database

cur = db["posts"].find()
movies_dict = cur[0]
shows_dict = cur[1]

movies = pd.DataFrame(movies_dict).transpose()
movies = movies.drop(labels = "_id", axis = 0)
shows = pd.DataFrame(shows_dict).transpose()
shows = shows.drop(labels = "_id",axis = 0)

#question 1
q1 = movies.groupby('MAIN_GENRE')['SCORE'].mean()['comedy']

#question 2
q2 = movies.groupby('MAIN_GENRE')['SCORE'].mean()
q2str = q2.to_string()

#question 3
q3 = shows.groupby('MAIN_GENRE')['SCORE'].mean()
q3str = q3.to_string()

#question4
q4df = shows[(shows['RELEASE_YEAR'] > 2017)]
q4 = q4df[q4df.SCORE == q4df.SCORE.max()].index[0]

#question5
q5df = movies[(movies['MAIN_GENRE'] == "thriller")]
q5 = q5df[q5df.SCORE == q5df.SCORE.max()].index[0]

#question6
q6df = movies[(movies['RELEASE_YEAR'] > 2017)]
q6 = q6df[q6df.SCORE == q6df.SCORE.max()].index[0]

#question7
q7df = shows[(shows['MAIN_GENRE'] == "comedy")]
q7 = q7df[q7df.SCORE == q7df.SCORE.max()].index[0]

#question8
q8df = movies[(movies['MAIN_GENRE'] == "drama")]
q8 = q8df[q8df.SCORE == q8df.SCORE.max()].index[0]

#question9
q9 = movies.groupby('MAIN_GENRE')['SCORE'].mean()['drama']

#question10
q10 = shows.groupby('MAIN_GENRE')['SCORE'].mean()['drama']


with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
               bag.append(1)
            else:
              bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)



net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=30, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)



def chat():
    print("Start talking with the bot! (type quit to stop)")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        result = model.predict([bag_of_words(inp, words)])[0]
        result_index = np.argmax(result)
        tag = labels[result_index]
        
        #if result[result_index] > 0.7:
        if(tag == 'greeting'):
            responses = data["intents"][0]["responses"]
            print(random.choice(responses))
        elif(tag == "question 2"):
            print(q2str)
        elif(tag == "question 3"):
            print(q3str)
        elif(tag=="question 1"):
            print(q1)
        elif(tag=="question 4"):
            print(q4)
        elif(tag=="question 5"):
            print(q5)
        elif(tag=="question 6"):
            print(q6)
        elif(tag=="question 7"):
            print(q7)
        elif(tag=="question 8"):
            print(q8)
        elif(tag=="question 9"):
            print(q9)
        elif(tag=="question 10"):
            print(q10)
        elif(tag=="goodbye"):
            responses = data["intents"][11]["responses"]
            print(random.choice(responses))

        else:
            print("I didnt get that. Can you explain or try again.")
chat()
