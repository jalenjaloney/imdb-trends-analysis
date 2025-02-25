"""
Final Project: IMDb Data Analysis

Dependencies: matplotlib

Authors: Jalen
Date: 11/25/2024
"""

import matplotlib.pyplot as plt

def parse_csv_line(line):
    """
    Parses a line from the CSV file and extracts attributes as a structured list.

    :param line: (str) A single line from the CSV file.
    :return: A list of attributes including title, year, rating, and genres.
    """
    attributes = [[''] for _ in range(7)]  # Initialize placeholders for attributes
    attribute_index = 0
    genre_index = 0
    in_quotes = False

    for char in line:
        if attribute_index != 3:
            if char == '"' and not in_quotes:
                in_quotes = True
            elif char == '"':
                in_quotes = False
            if char not in [",", '"']:
                attributes[attribute_index][0] += char
            elif char == "," and not in_quotes:
                attribute_index += 1
        else:
            if char == '"' and not in_quotes:
                in_quotes = True
            elif char == '"':
                in_quotes = False
            if char not in ['"', ',', ' ']:
                attributes[3][genre_index] += char
            elif char == "," and in_quotes:
                genre_index += 1
                attributes[3].append("")
            elif char == ",":
                attribute_index += 1

    # Strip trailing newline from the last attribute
    attributes[6][0] = attributes[6][0].strip()

    return attributes

def read_csv(filename):
    """
    Reads a CSV file and processes it line by line.

    :param filename: (str) Path to the CSV file.
    :return: A list of parsed lines from the file.
    """
    with open(filename, "r") as file_in:
        file_in.readline()  # Skip the header line
        return [parse_csv_line(line) for line in file_in]

def yearly_ratings(filename):
    """
    Calculates the average movie ratings for each year from the dataset.

    :param filename: (str) Path to the CSV file.
    :return: Two lists: years and their corresponding average ratings.
    """
    total_ratings = {}
    count_ratings = {}

    with open(filename, 'r') as file:
        for line in file:
            row = parse_csv_line(line)
            year = row[6][0]
            rating = row[4][0]

            # Ensure valid numeric year and rating
            if year.isdigit() and (rating.count(".") == 1 or rating.isdigit()):
                year = int(year)
                rating = float(rating)

                # Initialize data for a new year
                if year not in total_ratings:
                    total_ratings[year] = 0
                    count_ratings[year] = 0

                total_ratings[year] += rating
                count_ratings[year] += 1

    # Generate lists of years and their average ratings
    years = []
    avg_ratings = []
    for year in range(1900, 2026):
        if year in total_ratings:
            years.append(year)
            avg_ratings.append(total_ratings[year] / count_ratings[year])

    return years, avg_ratings

def genre_ratings(filename):
    """
    Aggregates ratings for specific genres and title types (movies and TV series).

    :param filename: (str) Path to the CSV file.
    :return: A dictionary containing ratings grouped by title type and genre.
    """
    genres_analysis = {"Drama", "Documentary", "Comedy"}
    ratings_data = {
        "movie": {"Drama": [], "Documentary": [], "Comedy": []},
        "tvSeries": {"Drama": [], "Documentary": [], "Comedy": []},
    }

    with open(filename, 'r') as file:
        for line in file:
            row = parse_csv_line(line)
            title_type = row[2][0]
            genres = row[3]
            rating = row[4][0]

            try:
                rating = float(rating)

                if title_type in ratings_data:
                    for genre in genres:
                        if genre in genres_analysis:
                            ratings_data[title_type][genre].append(rating)
            except ValueError:
                continue

    return ratings_data

def calculate_statistics(ratings_data):
    """
    Calculates the mean ratings for each genre and title type.

    :param ratings_data: (dict) A dictionary of ratings grouped by genre and title type.
    :return: A dictionary containing the mean rating for each genre and title type.
    """
    calculated_mean = {}
    for title_type in ratings_data:
        calculated_mean[title_type] = {}
        for genre in ratings_data[title_type]:
            ratings = ratings_data[title_type][genre]
            if len(ratings) > 0:
                mean_value = sum(ratings) / len(ratings)
                calculated_mean[title_type][genre] = {"mean": mean_value}
            else:
                calculated_mean[title_type][genre] = {"mean": 0}
    return calculated_mean

def plot_yearly_ratings(years, avg_ratings):
    """
    Plots average ratings by release year.

    :param years: (list) List of years.
    :param avg_ratings: (list) Average ratings corresponding to the years.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(years, avg_ratings, marker="o", linestyle="-", color="blue")
    plt.title("Average Rating by Release Year (1900 to Present)", fontsize=14)
    plt.xlabel("Release Year", fontsize=12)
    plt.ylabel("Average Rating", fontsize=12)
    plt.xticks(range(1900, 2026, 10))
    plt.grid(True)
    plt.ylim(0, 10)
    plt.savefig('visualization1.png')
    plt.show()

def plot_genre_mean(means):
    """
    Plots the mean ratings of specified genres for movies and TV series.

    :param means: (dict) A dictionary containing mean ratings for each genre by type.
    """
    genres = ["Drama", "Documentary", "Comedy"]
    types = ["movie", "tvSeries"]
    mean_value = "mean"
    colors = {"movie": "blue", "tvSeries": "orange"}  # Assign colors for each title type

    plt.figure(figsize=(10, 6))

    # Loop through the title types (movies and TV series)
    for title_type in types:
        values = []
        labels = []

        # Extract values and labels for the bar chart
        for genre in genres:
            values.append(means[title_type][genre][mean_value])
            labels.append(genre + " (" + title_type + ")")

        # Plot bars for each type
        plt.bar(
            labels,
            values,
            color=colors[title_type],
            label=title_type.capitalize(),
        )

    # Add chart title, labels, and legend
    plt.title("Mean Ratings by Genre for Movies and TV Series", fontsize=14)
    plt.ylabel("Mean Rating", fontsize=12)
    plt.ylim(0, 10)
    plt.legend()
    plt.xticks(rotation=10)
    plt.savefig('visualization2.png')
    plt.show()

def insertion_sort(arr):
    """
    Sorts a list in ascending order using the insertion sort algorithm.

    :param arr: (list) A list of comparable elements to sort.
    :return: (list) The sorted list in ascending order.
    """
    # Iterate through the list starting from the second element
    for i in range(1, len(arr)):
        key = arr[i]  # Current element to be placed in the correct position
        j = i - 1     # Start comparing with the previous element

        # Shift elements greater than 'key' one position to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        # Place 'key' in its correct position
        arr[j + 1] = key

    return arr

def genre_occurrences(array):
    """
    Counts the occurrences of each genre in the provided dataset.

    :param array: (list) A list of parsed CSV lines where each entry contains genres.
    :return: A dictionary with genres as keys and their counts as values.
    """
    genre_count = {}  # Dictionary to store genres and their counts

    # Iterate through the data rows
    for row in array:
        for genres in row[3]:  # Access the genre attribute
            if genres not in genre_count.keys() and genres != "":
                genre_count[genres] = 1  # Add new genre with a count of 1
            elif genres != "":
                genre_count[genres] += 1  # Increment count for existing genre

    return genre_count

def yearly_genre_occurrences(filename, year_start, year_end):
    """
    Calculates yearly genre occurrences for a specified range of years.

    :param filename: (str) The name of the CSV file containing the data.
    :param year_start: (int) Start year of the range.
    :param year_end: (int) End year of the range.
    :return: A sorted dictionary of yearly genre occurrences.
    """
    yearly_num_genres = {}

    # Parse the file and filter rows by year range
    for row in read_csv(filename):
        if row[6][0].isdigit() and year_start <= int(row[6][0]) <= year_end:
            year = int(row[6][0])
            if year not in yearly_num_genres:
                yearly_num_genres[year] = []
            yearly_num_genres[year].append(row)

    # Count genres for each year
    for year in yearly_num_genres.keys():
        yearly_num_genres[year] = genre_occurrences(yearly_num_genres[year])

    # Sort yearly data
    sorted_years = insertion_sort(list(yearly_num_genres.keys()))
    sorted_yearly_num_genres = {year: yearly_num_genres[year] for year in sorted_years}

    return sorted_yearly_num_genres

def all_time_genre_occurrences(filename):
    """
    Calculates and sorts the total occurrences of all genres in the dataset.

    :param filename: (str) The name of the CSV file containing the data.
    :return: A sorted dictionary of genres and their total occurrences.
    """
    unsorted_genre_occurrences = genre_occurrences(read_csv(filename))

    # Creates and sorts a list of each genre's associated occurrence values
    sorted_occurrences = []
    for genres in unsorted_genre_occurrences.keys():
        sorted_occurrences.append(unsorted_genre_occurrences[genres])
    sorted_occurrences = insertion_sort(sorted_occurrences)

    # Creates a dictionary of each genre in descending order based on occurrence values
    sorted_genre_popularity = {}
    for occurrences in sorted_occurrences[::-1]:
        for genres in unsorted_genre_occurrences.keys():
            if unsorted_genre_occurrences[genres] == occurrences:
                sorted_genre_popularity[genres] = occurrences

    return sorted_genre_popularity

def plot_genres_over_time(filename, genre_list, year_start, year_end):
    """
    Plots the popularity of specified genres over a range of years.

    :param filename: (str) The name of the CSV file containing the data.
    :param genre_list: (list) List of genres to track over time.
    :param year_start: (int) Start year of the range.
    :param year_end: (int) End year of the range.
    """
    occurrences = yearly_genre_occurrences(filename, year_start, year_end)

    years = list(occurrences.keys())  # Extract years
    genre_popularity = []

    # Extract yearly popularity for each genre
    for genre in genre_list:
        yearly_genre_popularity = []
        for release_year in occurrences.keys():
            if genre in occurrences[release_year].keys():
                yearly_genre_popularity.append(occurrences[release_year][genre])
            else:
                yearly_genre_popularity.append(0)
        genre_popularity.append(yearly_genre_popularity)

    plt.figure(figsize=(12, 6))

    # Plot the popularity of each genre
    genre_count = 0
    for x in genre_popularity:
        y_values = x
        x_values = years
        plt.plot(x_values, y_values, label=str(genre_list[genre_count]))  # Add legend label for each genre
        genre_count += 1

    # Add chart title, grid, and legend
    plt.title("Number of Movies/TV Series Released Each Year by Genre (" + str(year_start) + " to " + str(year_end) + ")", fontsize=14)
    plt.grid(True)
    plt.legend()
    plt.savefig('visualization3.png')
    plt.show()

def main():
    """
    Main function to analyze movie and TV series data from iMDB CSV file and generate visualizations.
    - Computes and plots yearly average ratings.
    - Computes and plots mean ratings for specific genres by type.
    - Identifies top genres and plots their popularity over time.
    """
    # Question 1: Compute and plot yearly average ratings
    years, avg_ratings = yearly_ratings("MovieData.csv")
    plot_yearly_ratings(years, avg_ratings)

    # Question 2: Compute and plot mean ratings by genre for movies and TV series
    ratings_data = genre_ratings("MovieData.csv")
    means = calculate_statistics(ratings_data)
    plot_genre_mean(means)

    # Question 3: Identify the top 5 genres and plot their popularity over time
    top_5_genres = list(all_time_genre_occurrences("MovieData.csv").keys())[0:5]
    plot_genres_over_time("MovieData.csv", top_5_genres, 1900, 2024)

    # Test Case: Identifying the top 10 genres and plotting their popularity from 1950 to 2023
    #top_10_genres = list(all_time_genre_occurrences("MovieData.csv").keys())[0:10]
    #plot_genres_over_time("MovieData.csv", top_10_genres, 1950, 2023)

if __name__ == "__main__":
    main()
