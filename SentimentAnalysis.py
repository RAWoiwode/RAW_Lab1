import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='odxohzyZoug0Cg',
                     client_secret='663wlMI87-2bmf_w9SVQ-otCCQQ',
                     user_agent='my user agent'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()
    return submission.comments

def process_comments(comments, neg_comments, neu_comments, pos_comments,
                     neg_threshold=0.33, neu_threshold=0.33, pos_threshold=0.33):
    '''
    This function recursively traverses a 'comment_forest' and runs each comment through a
    SentimentIntensityAnalyzer() to determine what kind of comment it is
    i.e. negative, neutral, or positive

    :param comments: The current comment/reply tree being traversed
    :param neg_comments: List to hold negative comments
    :param neu_comments: List to hold neutral comments
    :param pos_comments: List to hold positive comments
    :param neg_threshold: The minimum value to be considered a negative comment
    :param neu_threshold: The minimum value to be considered a neutral comment
    :param pos_threshold: The minimum value to be considered a positive comment
    :return: none
    '''

    for i in range(comments.__len__()):
        replies_to_comment = list(comments[i].replies)
        '''
        Test 1:
        Print out the end of a branch. Verify by checking the subreddit and
        looking at the end of reply branches
        '''
        # if not replies_to_comment:
        #     print(comments[i].body)
        # End of Test 1

        # See if the comment/reply has replies
        if replies_to_comment:
            process_comments(comments[i].replies, neg_comments, neu_comments, pos_comments)
        neg = get_text_negative_proba(comments[i].body)
        neu = get_text_neutral_proba(comments[i].body)
        pos = get_text_positive_proba(comments[i].body)
        if neg >= neg_threshold:
            neg_comments.append(comments[i].body)
        elif neu >= neu_threshold:
            neu_comments.append(comments[i].body)
        elif pos >= pos_threshold:
            pos_comments.append(comments[i].body)


def main():
    negative_comments_list, neutral_comments_list, positive_comments_list = list(), list(), list()
    print('What is recursion thread')
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    '''
    Test 2:
    Try the code with a different subreddit thread and see if it functions
    properly.
    '''
    # print('Python Cheat Sheet thread')
    # comments = get_submission_comments('https://www.reddit.com/r/Python/comments/7mwgtw/python_cheet_sheet_for_begineers/')
    # End of Test 2
    process_comments(comments, negative_comments_list, neutral_comments_list, positive_comments_list)
    print('Negative - ', negative_comments_list)
    print('Neutral - ', neutral_comments_list)
    print('Positive - ', positive_comments_list)

main()
