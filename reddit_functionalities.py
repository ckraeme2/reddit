import sys
import codecs
import string
import requests
from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
import pandas_datareader.data as web

if sys.stdout.encoding != 'utf-8':
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'utf-8':
  sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

api = PushshiftAPI()

def check_for_ticker(word):
    start = dt.datetime(2021, 4, 16)
    end = dt.datetime(2021, 4, 17)
    try:
        df = web.DataReader(word, 'yahoo', start, end)
        return True
    except:
        return False

def get_comments(limit=1000):
    comments = list(api.search_comments(subreddit='wallstreetbets', limit=limit))
    return comments

def get_submissions(limit = 1000):
    start_epoch = int(dt.datetime(2021, 4, 16).timestamp())

    submissions = list(api.search_submissions(after=start_epoch,
                            subreddit='wallstreetbets',
                            filter=['url', 'author', 'title', 'subreddit'],
                            limit=limit))

    return submissions

def get_relevant_submission_info(submissions):
    parsed_submissions = []
    for submission in submissions:
        temp = []
        temp.append(submission.author)
        temp.append(submission.created_utc)
        temp.append(submission.title)
        temp.append(get_karma(submission.author))
        parsed_submissions.append(temp)
    return parsed_submissions

def get_karma(author):
    res = requests.get('https://www.reddit.com/user/' + author + '/about.json', headers = {'User-agent': 'wsb-bot'})
    if res.status_code == 200:
        data = res.json()
        return data['data']['total_karma']
    else:
        return 0


def get_relevant_comment_info(comments):
    parsed_comments = []
    for comment in comments:
        temp = []
        temp.append(comment.author)
        temp.append(comment.body)
        temp.append(get_karma(comment.author))
        parsed_comments.append(temp)
    return parsed_comments

def get_only_comments_with_ticker(parsed_comments):
    relevant_comments = []
    tickers = []
    for item in parsed_comments:
        for word in item[1].split():
            if len(word) < 5 and len(word) > 2 and word.isupper():
                isTicker = check_for_ticker(word)
                if isTicker:
                    tickers.append(word)
        if len(tickers) > 0:
            tickers_set = set(tickers)
            tickers_list = list(tickers_set)
            item.append(tickers_list)
            relevant_comments.append(item)
            tickers = []
    return relevant_comments

def get_only_submissions_with_ticker(parsed_submissions):
    relevant_submissions = []
    tickers = []
    for item in parsed_submissions:
        for word in item[2].split():
            if len(word) < 5 and len(word) > 2 and word.isupper():
                isTicker = check_for_ticker(word)
                if isTicker:
                    tickers.append(word)
        if len(tickers) > 0:
            tickers_set = set(tickers)
            tickers_list = list(tickers_set)
            item.append(tickers_list)
            relevant_submissions.append(item)
    return relevant_submissions

def create_mappings(comments, submissions):
    mappings = {}
    for comment in comments:
        for ticker in comment[3]:
            mappings[ticker] = mappings.get(ticker, 0) + 1
    for submission in submissions:
        for ticker in submission[4]:
            mappings[ticker] = mappings.get(ticker, 0) + 1
    return mappings


def main():
    comments = get_comments(10)
    parsed_comments = get_relevant_comment_info(comments)
    relevant_comments = get_only_comments_with_ticker(parsed_comments)
    submissions = get_submissions(10)
    parsed_submissions = get_relevant_submission_info(submissions)
    relevant_submissions = get_only_submissions_with_ticker(parsed_submissions)
    tickerMappings = create_mappings(relevant_comments, relevant_submissions)
    print(tickerMappings)

if __name__ == '__main__':
    main()