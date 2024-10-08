import praw
import time
import pandas as pd
import matplotlib.pyplot as plt
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
import emoji
import re
import string

SUBS = ['wallstreetbets']
POST_FLAIRS = {'Daily Discussion', 'Weekend Discussion', 'Discussion'}
GOOD_AUTHORS = {'AutoModerator'}
IGNORE_AUTHORS_POST = {'example'}
IGNORE_AUTHORS_COMMENT = {'example'}
UPVOTE_RATIO = 0.70
UPVOTES_POST = 20
UPVOTES_COMMENT = 2
PICKS = 10
PICKS_ANALYSIS = 5

vader = SentimentIntensityAnalyzer()

def extract_data(reddit):
    posts, comments_analyzed, tickers, titles, all_comments = 0, 0, {}, [], {}
    
    for sub in SUBS:
        subreddit = reddit.subreddit(sub)
        hot_posts = subreddit.hot()
        
        for submission in hot_posts:
            flair = submission.link_flair_text
            author = submission.author.name if submission.author else None
            
            if (submission.upvote_ratio >= UPVOTE_RATIO and 
                submission.ups > UPVOTES_POST and 
                (flair in POST_FLAIRS or flair is None) and 
                author not in IGNORE_AUTHORS_POST):
                
                submission.comment_sort = 'new'
                titles.append(submission.title)
                posts += 1
                try:
                    submission.comments.replace_more(limit=1)
                    for comment in submission.comments:
                        if comment.author:
                            comment_author = comment.author.name
                        else:
                            continue
                        
                        comments_analyzed += 1
                        
                        if comment.score > UPVOTES_COMMENT and comment_author not in IGNORE_AUTHORS_COMMENT:
                            words = comment.body.split()
                            for word in words:
                                word = word.replace("$", "")
                                if word.isupper() and len(word) <= 5:
                                    if word in tickers:
                                        tickers[word] += 1
                                        all_comments[word].append(comment.body)
                                    else:
                                        tickers[word] = 1
                                        all_comments[word] = [comment.body]
    
                except Exception as e:
                    print(f"Error extracting comments: {e}")
                    
    return posts, comments_analyzed, tickers, titles, all_comments

def print_summary(tickers, comments_analyzed, posts):
    sorted_tickers = dict(sorted(tickers.items(), key=lambda item: item[1], reverse=True))
    top_picks = list(sorted_tickers.keys())[:PICKS]
    
    print(f"\nAnalyzed {comments_analyzed} comments in {posts} posts.")
    print(f"\nTop {PICKS} mentioned tickers:")
    for ticker in top_picks:
        print(f"{ticker}: {sorted_tickers[ticker]}")
        
    return sorted_tickers, top_picks

def analyze_sentiment(all_comments, sorted_tickers):
    scores = {}
    
    picks_for_analysis = list(sorted_tickers.keys())[:PICKS_ANALYSIS]
    
    for symbol in picks_for_analysis:
        stock_comments = all_comments[symbol]
        total_score = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
        word_count = 0
        
        for comment in stock_comments:
            emojiless = emoji.get_emoji_regexp().sub(u'', comment)
            text_cleaned = "".join([char for char in emojiless if char not in string.punctuation])
            text_cleaned = re.sub('[0-9]+', '', text_cleaned)
            
            tokenizer = RegexpTokenizer('\w+')
            tokens = tokenizer.tokenize(text_cleaned.lower())
            
            for token in tokens:
                score = vader.polarity_scores(token)
                for key in total_score:
                    total_score[key] += score[key]
                word_count += 1
                
        if word_count > 0:
            for key in total_score:
                total_score[key] /= word_count
                total_score[key] = "{:.3f}".format(total_score[key])
            scores[symbol] = total_score
            
    return scores

def visualize_analysis(scores):
    df = pd.DataFrame(scores).T
    df.index = ['Bearish', 'Neutral', 'Bullish', 'Total/Compound']
    
    print("\nSentiment analysis of top picks:")
    print(df)
    
    colors = ['red', 'orange', 'green', 'blue']
    df.plot(kind='bar', color=colors, title="Sentiment analysis of top picks:")
    plt.show()

def main():
    start_time = time.time()
    
    reddit = praw.Reddit(
        user_agent="Comment Extraction",
        client_id="",  
        client_secret="",  
        username="",  
        password=""  
    )
    
    posts, comments_analyzed, tickers, titles, all_comments = extract_data(reddit)
    sorted_tickers, top_picks = print_summary(tickers, comments_analyzed, posts)
    sentiment_scores = analyze_sentiment(all_comments, sorted_tickers)
    visualize_analysis(sentiment_scores)
    
    print(f"\nExecution time: {time.time() - start_time:.2f} seconds")

if __name__ == '__main__':
    main()
