#!/usr/bin/env python
# coding: utf-8

# ### Import Required Libraries and Set Up Environment Variables

# In[48]:


# Dependencies
import requests
import time
import os
import pandas as pd
import json
from dotenv import load_dotenv


# In[49]:


# Load environment variables from .env file
load_dotenv()


# In[50]:


# Set environment variables from the .env in the local environment

nyt_api_key = os.environ.get("nyt_api_key")
tmdb_api_key = os.environ.get("tmdb_api_key")


# ### Access the New York Times API

# In[51]:


# Set the base URL
url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"

# Filter for movie reviews with "love" in the headline
# section_name should be "Movies"
# type_of_material should be "Review"
filter_query = 'headline:("love") AND section_name:("Movies") AND type_of_material:("Review")'

# Use a sort filter, sort by newest
sort = "newest"

# Select the following fields to return:
# headline, web_url, snippet, source, keywords, pub_date, byline, word_count
field_list = "headline,web_url,snippet,source,keywords,pub_date,byline,word_count"

# Search for reviews published between a begin and end date
begin_date = "20130101"
end_date = "20230531"

# Build URL
query_url = f"{url}api-key={nyt_api_key}&q=&fq={filter_query}&sort={sort}&fl={field_list}&begin_date={begin_date}&end_date={end_date}"


# In[52]:


# Create an empty list to store the reviews


# loop through pages 0-19

    # create query with a page number
    # API results show 10 articles at a time

    
    # Make a "GET" request and retrieve the JSON

    
    # Add a twelve second interval between queries to stay within API query limits

    
    # Try and save the reviews to the reviews_list

        # loop through the reviews["response"]["docs"] and append each review to the list

        # Print the page that was just retrieved


        # Print the page number that had no results then break from the loop

# Create an empty list to store the reviews
reviews_list = []

# Loop through pages 0-19
for page in range(20):
    # Create query with a page number
    page_query_url = query_url + f"&page={page}"

    try:
        # Make a "GET" request and retrieve the JSON
        response = requests.get(page_query_url)
        reviews = response.json()

        # Print the structure of the first page response
        if page == 0:
            print(json.dumps(reviews, indent=4))

        # Check if 'docs' are present in the response
        if 'docs' in reviews['response']:
            # Loop through the reviews["response"]["docs"] and append each review to the list
            for doc in reviews['response']['docs']:
                reviews_list.append(doc)
                print("Added a review to the list.")
            print(f"Page {page} retrieved successfully.")
        else:
            print(f"No 'docs' found in response on page {page}.")
            break

        # Add a twelve second interval between queries to stay within API query limits
        time.sleep(12)

    except Exception as e:
        print(f"Error on page {page}: {e}. Breaking from loop.")
        break

# Print the total number of reviews retrieved
print(f"Total reviews retrieved: {len(reviews_list)}")




# In[53]:


# Test the API response for the first page
test_response = requests.get(query_url + "&page=0")
print(json.dumps(test_response.json(), indent=4))

# Check if the 'docs' key contains data
if 'docs' in test_response.json()['response']:
    print("Data found in 'docs'")
else:
    print("No data found in 'docs'")


# In[54]:


# Preview the first 5 results in JSON format
# Use json.dumps with argument indent=4 to format data

print(json.dumps(reviews_list[:5], indent=4))


# In[55]:


# Convert reviews_list to a Pandas DataFrame using json_normalize()

reviews_df = pd.json_normalize(reviews_list)

# Display the first few rows of the DataFrame to verify
print(reviews_df.head())


# In[56]:


# Extract the title from the "headline.main" column and
# save it to a new column "title"
# Title is between unicode characters \u2018 and \u2019. 
# End string should include " Review" to avoid cutting title early

# Extract the title from "headline.main" and save it to a new column "title"
reviews_df['title'] = reviews_df['headline.main'].apply(
    lambda st: st[st.find("\u2018")+1 : st.find("\u2019 Review")] if "\u2019 Review" in st else st
)

# Display the first few rows of the DataFrame
print(reviews_df.head())


# In[57]:


# Extract 'name' and 'value' from items in "keywords" column
def extract_keywords(keyword_list):
    extracted_keywords = ""
    for item in keyword_list:
        # Extract 'name' and 'value'
        keyword = f"{item['name']}: {item['value']};" 
        # Append the keyword item to the extracted_keywords list
        extracted_keywords += keyword
    return extracted_keywords

# Fix the "keywords" column by converting cells from a list to a string
# Apply the extract_keywords function to the "keywords" column
reviews_df['keywords'] = reviews_df['keywords'].apply(extract_keywords)

# Display the first few rows to verify the changes
print(reviews_df[['keywords']].head())


# In[58]:


# Create a list from the "title" column using to_list()
# These titles will be used in the query for The Movie Database
# Create a list from the "title" column
titles_list = reviews_df['title'].to_list()

# Display the first few titles to verify
print(titles_list[:5])


# In[ ]:





# ### Access The Movie Database API

# In[59]:


# Prepare The Movie Database query
url = "https://api.themoviedb.org/3/search/movie?query="
tmdb_key_string = "&api_key=" + tmdb_api_key


# In[60]:


# Check if we need to sleep before making a request


# Add 1 to the request counter


# Perform a "GET" request for The Movie Database


# Include a try clause to search for the full movie details.
# Use the except clause to print out a statement if a movie
# is not found.

    # Get movie id


    # Make a request for a the full movie details


    # Execute "GET" request with url

    
    # Extract the genre names into a list


    # Extract the spoken_languages' English name into a list


    # Extract the production_countries' name into a list


    # Add the relevant data to a dictionary and
    # append it to the tmdb_movies_list list

    
    # Print out the title that was found

tmdb_api_key = os.environ.get("tmdb_api_key")

if tmdb_api_key is None:
raise ValueError("tmdb_api_key not found in the environment variables.")

url = "https://api.themoviedb.org/3/search/movie?query="
tmdb_key_string = "&api_key=" + tmdb_api_key


# Create an empty list to store the results
tmdb_movies_list = []

# Create a request counter to sleep the requests after a multiple
# of 50 requests
request_counter = 0

# Loop through movie titles
for title in titles_list:
# Sleep after every 50 requests
if request_counter % 50 == 0 and request_counter != 0:
    time.sleep(10)  # Sleep for 10 seconds

request_counter += 1

# Form the request URL
request_url = url + title.replace(" ", "+") + tmdb_key_string

try:
    # Get movie ID
    response = requests.get(request_url)
    movie_data = response.json()
    movie_id = movie_data['results'][0]['id']

    # Request for full movie details
    movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US"
    movie_detail_response = requests.get(movie_detail_url)
    movie_detail = movie_detail_response.json()

    # Extracting required details
    genres = [genre['name'] for genre in movie_detail['genres']]
    languages = [lang['english_name'] for lang in movie_detail['spoken_languages']]
    countries = [country['name'] for country in movie_detail['production_countries']]

    # Add data to the list
    tmdb_movies_list.append({
        'title': title,
        'genres': genres,
        'languages': languages,
        'countries': countries
    })

    # Print the title that was found
    print(f"Found and added details for: {title}")

except (IndexError, KeyError):
    print(f"Movie not found or an error occurred for title: {title}")

# Print the final list
print("TMDB Movies Data:", tmdb_movies_list)


# In[ ]:





# In[62]:


# Preview the first 5 results in JSON format
# Use json.dumps with argument indent=4 to format data
print(json.dumps(tmdb_movies_list[:5], indent=4))


# In[63]:


# Convert the results to a DataFrame
tmdb_movies_df = pd.DataFrame(tmdb_movies_list)
tmdb_movies_df


# ### Merge and Clean the Data for Export

# In[64]:


# Merge the New York Times reviews and TMDB DataFrames on title
merged_df = pd.merge(reviews_df, tmdb_movies_df, on='title', how='inner')

# Move the 'title' column to the first position
column_order = ['title'] + [col for col in merged_df if col != 'title']
merged_df = merged_df[column_order]
merged_df.head()


# In[65]:


# Create a list to store the names of columns containing lists
columns_with_lists = []

# Iterate through the columns of the DataFrame
for column in merged_df.columns:
    # Check if the data type of the column is 'list' or 'object'
    if merged_df[column].apply(type).eq(list).any() or merged_df[column].apply(type).eq(object).any():
        columns_with_lists.append(column)

# Print the columns containing lists
print("Columns containing lists:", columns_with_lists)


# In[66]:


# Remove list brackets and quotation marks on the columns containing lists
# Create a list of the columns that need fixing


# Create a list of characters to remove


# Loop through the list of columns to fix

    # Convert the column to type 'str'


    # Loop through characters to remove


# Display the fixed DataFrame

# List of columns containing lists
columns_with_lists = ['byline.person', 'genres', 'languages', 'countries']

# List of characters to remove (brackets and quotation marks)
characters_to_remove = ['[', ']', "'"]

# Loop through the list of columns to fix
for column in columns_with_lists:
    # Convert the column to type 'str' and remove characters
    merged_df[column] = merged_df[column].astype(str)
    for char in characters_to_remove:
        merged_df[column] = merged_df[column].str.replace(char, '')

# Display the fixed DataFrame
print(merged_df)
merged_df.head()


# In[67]:


# Drop "byline.person" column
# Drop the "byline.person" column from the DataFrame
merged_df.drop(columns=['byline.person'], inplace=True)

# Display the DataFrame after dropping the column
print(merged_df)


# In[68]:


# Delete duplicate rows and reset index

# Remove duplicate rows based on all columns
merged_df.drop_duplicates(inplace=True)

# Reset the index after removing duplicates
merged_df.reset_index(drop=True, inplace=True)

# Display the DataFrame after removing duplicates and resetting the index
print(merged_df)


# In[69]:


# Export data to CSV without the index


# In[70]:


csv_file_path = '/Users/mattobrien/Documents/AI_BOOTCAMP/M6_Starter_Code/output/output_data.csv'

# Export the DataFrame to a CSV file without the index
merged_df.to_csv(csv_file_path, index=False)

# Print a message to confirm the export
print(f"Data has been exported to {csv_file_path}")


# In[ ]:




