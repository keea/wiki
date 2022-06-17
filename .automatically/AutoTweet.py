import sys
import os
import frontmatter
import tweepy
import urllib.parse

def OAuth():
    API_KEY = os.environ.get('TWITTER_API_KEY')
    API_KEY_SECRET = os.environ.get('TWITTER_API_SECRET')
    ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')
    ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    client = tweepy.Client(consumer_key= API_KEY,consumer_secret= API_KEY_SECRET,access_token= ACCESS_TOKEN,access_token_secret= ACCESS_SECRET)
    return client

def GetTweetText(file):
    site_url = os.environ.get('SITE_DOMAIN')
    file_name = file.replace('.md','')
    post_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"+file)
    post = frontmatter.load(post_path)
    post_text = "New Post : " + post['title'] +"\n" + site_url + urllib.parse.quote(file_name)
    return post_text


def main():
    file = " ".join(sys.argv[1:len(sys.argv)])
    print(file)
    if not file:
        return
    
    client = OAuth()
    client.create_tweet(text = GetTweetText(file))

if __name__ == "__main__":
    main()
