import asyncio
from random import randint
from twikit import Client, TooManyRequests
from datetime import datetime, time
import csv
from configparser import ConfigParser

MINIMUM_TWEETS = 400 
QUERY = 'wybory prezydenckie lang:pl until:2025-04-28 since:2025-01-15'

async def get_tweets(client, query, tweets=None):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(query, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds...')
        await asyncio.sleep(2)
        tweets = await tweets.next()

    return tweets

async def main():
    #* login credentials
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    #* authenticate to X.com
    client = Client(language='en-US')
    await client.login(auth_info_1=username, auth_info_2=email, password=password)
    client.save_cookies('cookies.json')
    client.load_cookies('cookies.json')

    tweet_count = 0
    tweets = None

    #* create CSV file and open it once
    with open('_wybory2025_2.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count','Usename', 'Name', 'Text', 'Retweets', 'Likes'])

        while tweet_count < MINIMUM_TWEETS:
            try:
                tweets = await get_tweets(client, QUERY, tweets)

            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
                wait_time = rate_limit_reset - datetime.now()
                time.sleep(wait_time.total_seconds())
                continue

            if not tweets:
                print(f'{datetime.now()} - No more tweets found')
                break

            for tweet in tweets:
                tweet_count += 1
                tweet_data = [
                    tweet_count,
                    tweet.user.name,
                    tweet.text.replace('\n', ' ').strip(),
                    tweet.created_at,
                    tweet.retweet_count,
                    tweet.favorite_count
                ]
                writer.writerow(tweet_data)

            print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Total: {tweet_count} tweets.')

#* run the async main function
asyncio.run(main())


