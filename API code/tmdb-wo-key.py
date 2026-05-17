#!/usr/bin/env python
# coding: utf-8

# In[69]:


#import tmdb API key

tmdb_api_key = #insert personal TMDB API key here#

import requests

api_key = tmdb_api_key 
url = f"https://api.themoviedb.org/3/movie/550?api_key={api_key}"

response = requests.get(url)
data = response.json()

print(data)


# In[70]:


#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from pandas import json_normalize 
import networkx as nx
import datetime


# In[71]:


#Test
query = "https://api.themoviedb.org/3/movie/" + "438631" + "/credits?api_key=" + api_key + "&language=en-US"
response =  requests.get(query)
array = response.json()
temp_cast = json_normalize(array, 'cast')
temp_cast.head()


# In[82]:


#Read csv
movies = pd.read_csv("films_tmdb.csv")
movies = movies.drop_duplicates()
movies.to_csv('cleaned_output.csv', index=False)


# In[97]:


#new csv with film details
import csv
import requests
import time

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = #inset personal TMDB API key here#

def get_movie_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error getting credits for {movie_id}: {response.status_code}")
        print(response.text)
        return None
    return response.json()

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error getting details for {movie_id}: {response.status_code}")
        print(response.text)
        return None
    return response.json()

def extract_director(crew_list):
    directors = [c["name"] for c in crew_list if c["job"] == "Director"]
    return ", ".join(directors)

def extract_top_cast(cast_list, n=15):
    return ", ".join([c["name"] for c in cast_list[:n]])

def extract_genres(details):
    if "genres" in details:
        return ", ".join([g["name"] for g in details["genres"]])
    return ""

def process_csv(input_file, output_file):
    with open(input_file, newline="", encoding="utf-8") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ["tmdb_id", "title", "director", "top_cast", "genres", "release_date", "budget"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            movie_id = row["id"].strip()
            if not movie_id:
                continue

            # Fetch data
            credits = get_movie_credits(movie_id)
            details = get_movie_details(movie_id)

            if not credits or not details:
                print(f"⚠️ Skipping movie ID {movie_id}")
                continue

            # Extract info
            title = details.get("title", "")
            director = extract_director(credits["crew"])
            cast = extract_top_cast(credits["cast"])
            genres = extract_genres(details)
            release_date = details.get("release_date", "")
            budget = details.get("budget", "")

            # Write to CSV
            writer.writerow({
                "tmdb_id": movie_id,
                "title": title,
                "director": director,
                "top_cast": cast,
                "genres": genres,
                "release_date": release_date,
                "budget": budget
            })

            time.sleep(0.25)  # avoid rate limits

if __name__ == "__main__":
    process_csv("cleaned_output.csv", "film_details.csv")


# In[98]:


#new csv with film details with corrected movie ID
import csv
import requests
import time

BASE_URL = "https://api.themoviedb.org/3"
API_KEY = #insert personal TMDB API Key here#

def get_movie_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error getting credits for {movie_id}: {response.status_code}")
        print(response.text)
        return None
    return response.json()

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error getting details for {movie_id}: {response.status_code}")
        print(response.text)
        return None
    return response.json()

def extract_director(crew_list):
    directors = [c["name"] for c in crew_list if c["job"] == "Director"]
    return ", ".join(directors)

def extract_top_cast(cast_list, n=15):
    return ", ".join([c["name"] for c in cast_list[:n]])

def extract_genres(details):
    if "genres" in details:
        return ", ".join([g["name"] for g in details["genres"]])
    return ""

def process_csv(input_file, output_file):
    with open(input_file, newline="", encoding="utf-8") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ["tmdb_id", "title", "director", "top_cast", "genres", "release_date", "budget"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            movie_id = row["id"].strip()
            if not movie_id:
                continue

            # Fetch data
            credits = get_movie_credits(movie_id)
            details = get_movie_details(movie_id)

            if not credits or not details:
                print(f"⚠️ Skipping movie ID {movie_id}")
                continue

            # Extract info
            title = details.get("title", "")
            director = extract_director(credits["crew"])
            cast = extract_top_cast(credits["cast"])
            genres = extract_genres(details)
            release_date = details.get("release_date", "")
            budget = details.get("budget", "")

            # Write to CSV
            writer.writerow({
                "tmdb_id": movie_id,
                "title": title,
                "director": director,
                "top_cast": cast,
                "genres": genres,
                "release_date": release_date,
                "budget": budget
            })

            time.sleep(0.25)  # avoid rate limits

if __name__ == "__main__":
    process_csv("cleaned_output_v2.csv", "film_details_v2.csv")


# In[5]:


# Load your CSV
df = pd.read_csv("film_details_v2.csv")

# REMOVE commas after suffixes like "Jr.," 
df['top_cast_clean'] = df['top_cast'].str.replace(
    r'(Jr\.|Sr\.|III|IV|Ph\.D\.)\s*,',
    r'\1',  # remove the comma
    regex=True
)

# Split the column into multiple columns
cast_split = df['top_cast_clean'].str.split(',', expand=True)

# Strip whitespace from each entry
cast_split = cast_split.apply(lambda col: col.str.strip())

# Rename columns dynamically
cast_split.columns = [f"Cast {i+1}" for i in range(cast_split.shape[1])]

# Combine back with original dataframe
df = df.drop(columns=['top_cast', 'top_cast_clean']).join(cast_split)

# Save result (optional)
df.to_csv("film_details_v3.csv", index=False)


# In[ ]:




