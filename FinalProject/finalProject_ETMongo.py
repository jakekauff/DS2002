"""
Jakob Kauffmann 
DS 2002
Final Project: upload data to mongo
"""
import pandas as pd
import pymongo
import json

movie_by_year = pd.read_csv("Best Movie by Year Netflix.csv", header=0, index_col=False)

movie_by_year = movie_by_year.drop(labels=0,axis=0)
movie_by_year = movie_by_year.drop(columns="index")
movie_by_year = movie_by_year.drop(columns='MAIN_PRODUCTION')
movie_by_year = movie_by_year.set_index("TITLE")

shows_by_year = pd.read_csv("Best Show by Year Netflix.csv", header=0 ,index_col=False)
shows_by_year = shows_by_year.drop(labels=0,axis=0)
shows_by_year = shows_by_year.drop(columns="index")
shows_by_year = shows_by_year.drop(columns='MAIN_PRODUCTION')
shows_by_year = shows_by_year.set_index("TITLE")

movie_json = movie_by_year.to_json(orient='index')
movie_dict = json.loads(movie_json)

shows_json = shows_by_year.to_json(orient='index')
shows_dict = json.loads(shows_json)

host_name = "localhost"
port = "27017"

atlas_cluster_name = "sandbox"
atlas_default_dbname = "local"

conn_str = {
    "local" : f"mongodb://{host_name}:{port}/"
}

client = pymongo.MongoClient(conn_str["local"])

db = client["FinalProject"]
client.list_database_names()
posts = db.posts

post_id_movies = posts.insert_one(movie_dict).inserted_id
post_id_shows = posts.insert_one(shows_dict).inserted_id

