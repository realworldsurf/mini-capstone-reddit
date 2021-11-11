# Mini-Capstone Python API

# For Heroku to deploy I had to create a new repository on github, a requirements.txt, Procfile and optional python-getting-started.
import praw 

reddit = praw.Reddit(
    user_agent="Comment Extraction (by u/USERNAME)",
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    username="USERNAME",
    password="PASSWORD",
)









messages = reddit.inbox.stream() # creates an iterable for your inbox and streams it
for message in messages: # iterates through your messages
  try:
    if message in reddit.inbox.mentions() and message in reddit.inbox.unread(): # if this messasge is a mention AND it is unread...
        message.reply("hello") # reply with this message
        message.mark_read() # mark message as read so your bot doesn't respond to it again...
  except praw.exceptions.APIException: # Reddit may have rate limits, this prevents your bot from dying due to rate limits
    print("probably a rate limit....")


    subr = r.subreddit('copypasta') # this chooses a subreddit you want to get comments from
for comment in subr.stream.comments(skip_existing=True): # this iterates through the comments from that subreddit as new ones are coming in
  try:
    if "!bot" in comment.body: # "!bot" is the keyword in this case. replace "bot" with your keyword
      comment.reply("hello world...") # this is what your bot replies to the comment that has the keyword
  except praw.exceptions.APIException: # Reddit may have rate limits, this prevents your bot from dying due to rate limits
    print("probably a rate limit...")