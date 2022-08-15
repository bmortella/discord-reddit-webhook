import os
import textwrap
import praw
from discord_webhook import DiscordWebhook, DiscordEmbed

def main():
    reddit = praw.Reddit(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        user_agent=os.environ['USER_AGENT'],
        username=os.environ['USERNAME'],
        password=os.environ['PASSWORD'],
    )

    subreddit = reddit.subreddit(os.environ['SUBREDDIT'])
    for submission in subreddit.stream.submissions(skip_existing=True):
        process_submission(submission)
    
def process_submission(submission):
    webhook = DiscordWebhook(url=os.environ['WEBHOOK_URL'], username=f'reddit • r/{submission.subreddit.display_name}', rate_limit_retry=True)
    embed = DiscordEmbed(title=f'New {"self" if submission.is_self else "link"} post')
    embed.set_author(name=submission.author.name)
    embed.set_url(f'https://redd.it/{submission.id}')
    embed.set_color("43B581")
    
    selftext = textwrap.shorten(submission.selftext, width=250, placeholder='...')
    if not submission.is_self:
        embed.set_color("44DDBF")
        selftext = submission.url
        if submission.url.endswith(".jpg") or submission.url.endswith(".png"):
            embed.set_image(url=submission.url)
    
    embed.add_embed_field(name=textwrap.shorten(submission.title, width=256, placeholder='...'),
                          value=selftext)
    
    
    webhook.add_embed(embed)
    webhook.execute()

if __name__ == "__main__":
    main()