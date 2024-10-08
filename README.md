# Reddit Sentiment Analysis

This project performs sentiment analysis on Reddit comments using Natural Language Processing (NLP) techniques. It scrapes comments from specified Reddit threads, analyzes their sentiment, and visualizes the results.

## Contents
- About
- Setup
- Usage
- Results
- Improvements & Future Work
- Acknowledgments

## About

The **Reddit Sentiment Analysis** project aims to analyze user sentiment in comments on Reddit. By leveraging NLP libraries, the project provides insights into user opinions and trends based on the sentiment of comments. The main goals are to identify positive, negative, and neutral sentiments and visualize the findings.

## Setup

To get started, follow these steps:

1. **Install Dependencies**: Ensure you have Python installed, then install the required libraries-

   The required libraries include:
   - `requests`
   - `praw`
   - `nltk`
   - `matplotlib`
   - `pandas`

2. **Run the Application**: Execute the main script to start the sentiment analysis:

    ```bash
    python scripts/sentiment_analysis.py
    ```

## Usage

1. **Data Collection**: 
   - The script uses the Reddit API via the PRAW library to collect comments from specified Reddit threads. Make sure to provide the necessary credentials to access the Reddit API.

2. **Data Preprocessing**: 
   - The comments are preprocessed to remove noise and prepare them for analysis. This includes tokenization, removing stop words, and stemming.

3. **Sentiment Analysis**: 
   - The sentiment of each comment is analyzed using a predefined sentiment analysis model. The results are stored in a dataframe.

4. **Data Visualization**: 
   - The results are visualized using Matplotlib to present the distribution of sentiments.

## Results

Visualizations generated from the analysis will provide insights into the sentiment distribution of Reddit comments. 

*Note: An example of the sentiment visualization is available in the `images` folder.*

## Improvements & Future Work

1. **Model Improvements**: 
   - Future versions could integrate advanced models like BERT for better sentiment classification.

2. **Enhanced Visualizations**: 
   - Implement additional visualizations for better insights, such as word clouds for frequent words in positive or negative comments.

## Acknowledgments

- **PRAW**: For providing an easy way to scrape data from Reddit.
- **NLTK**: For its robust NLP capabilities.
- **Matplotlib**: For enabling intuitive visualizations.

