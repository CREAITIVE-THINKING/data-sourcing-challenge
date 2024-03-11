
# Movie Data Sourcing Project

## Project Overview
This project involves extracting movie reviews and details from two prominent sources: The New York Times API and The Movie Database (TMDb) API. The objective is to prepare data for a recommendation system aimed at helping users find movie reviews and related movies. Through this project, we access, merge, and clean data obtained from these APIs, setting the foundation for future natural language processing tasks.

## Getting Started

### Prerequisites
- Python 3.x
- Requests library for API requests
- Pandas library for data manipulation
- Dotenv library for loading API keys from .env files

### API Keys
- You need to obtain API keys for both The New York Times and The Movie Database (TMDb).
- Store your API keys in a `.env` file with the following format:
  ```plaintext
  NYT_API_KEY=your_new_york_times_api_key_here
  TMDB_API_KEY=your_tmdb_api_key_here
  ```

### Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/CREAITIVE-THINKING/data-sourcing-challenge.git
   ```

2. **Navigate to the Project Directory**
   ```bash
   cd data-sourcing-challenge
   ```

3. **Install Required Python Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Script**
   Execute the Python script to retrieve movie data.
   ```bash
   python retrieve_movie_data.py
   ```

## Parts of the Project

- **Part 1: Access The New York Times API**: Extract movie reviews that contain "love" in the headline from the "Movies" section.
- **Part 2: Access The Movie Database API**: Using titles extracted from The New York Times reviews, fetch corresponding movie details from TMDb.
- **Part 3: Merge and Clean the Data**: Combine data from both sources and prepare it for export, focusing on cleaning and structuring for easy use in recommendation systems.

## Data Exploration and Cleaning
- Merging data based on movie titles.
- Cleaning lists within DataFrame columns to ensure data is in a user-friendly string format.
- Dropping duplicates and unnecessary columns for clarity.
- Exporting the cleaned and merged data to a CSV file for further use.

## Contributing
Contributions to improve the project are welcome. Please fork the repository and submit a pull request with your changes.

Repository Link: https://github.com/CREAITIVE-THINKING/data-sourcing-challenge
