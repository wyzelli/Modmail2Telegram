import praw
# import praw.util.token_manager
import time
import configparser
import requests
VERSION = 0.01

# Load the OAuth information from the modmail.ini file - make your own from the included sample.ini
config = configparser.ConfigParser()
config.read("modmail.ini")
client_id = config.get("reddit", "client_id")
client_secret = config.get("reddit", "client_secret")
refresh_token = config.get("reddit", "refresh_token")
username = config.get("reddit", "username")
password = config.get("reddit", "password")
user_agent = config.get("reddit", "user_agent")

# Set up the PRAW Reddit API wrapper
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    refresh_token=refresh_token,
    #username=username,
    #password=password,
    user_agent=user_agent,
)

# Set the subreddit and modmail folder to monitor
subreddit_name = "r/sudoku"
modmail_folder = "mod"
subreddit = reddit.subreddit(subreddit_name)
modmail = subreddit.modmail

# Set the loop delay to 10 minutes (in seconds)
loop_delay = 10 * 60

telegram_token = config.get("telegram", "bot_token")
telegram_chat_id = config.get("telegram", "chat_id")

# Start the loop
while True:
    # if modmail.num_messages > 0:

    for modmail_conversation in subreddit.mod.stream.modmail_conversations(state='new'):
        author=str(modmail_conversation.authors[0])

        # TODO :Loop through the modmail threads in the specified folder # these properties might be wrong
        #for thread in modmail.replies(folder=modmail_folder):

            # Check if the thread has any new messages since the last time we checked
            #if thread.last_unread is not None:

            # Send a Telegram message with the thread's subject and permalink
        message = f"New modmail in {subreddit_name} from {author}"
            #- {thread.subject}\n\n{thread.permalink}"
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}&text={message}"
        print(requests.get(url).json())
                
            # Mark the thread as read so we don't get duplicate notifications
            #thread.mark_read()

        # Wait for the specified delay before running the loop again
        time.sleep(loop_delay)