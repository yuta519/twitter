# coding: utf-8
import tweepy
import mysql.connector
import twitter_account

def main():
    # Twitter 情報収集
    twitter_account = setTwitterAccount()
    twitter_api = createTwitterObj(twitter_account[0], twitter_account[1], twitter_account[2], twitter_account[3])
    account_list = setSecTwitterSpecialist()
    sec_tweetdata = []
    for sec_account in account_list:
        aquireTweetDataByApi(twitter_api, sec_account, sec_tweetdata)
    
    # MySQLデータ挿入
    conn = mysql.connector.connect(user='root', password='{password}', host='localhost', database='tweetdata')
    cur = conn.cursor()
    query = '''
        INSERT IGNORE INTO sec_tweetdata 
        (id, user_name, tweeted_at, tweeted_contents, favo, retweet) 
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cur.executemany(query, sec_tweetdata)
    conn.commit()
    cur.close()
    conn.close() # ここでDBへのコネクション切断


def setTwitterAccount():
    CK  = twitter_account.consumer_key
    CS  = twitter_account.consumer_secret
    AT  = twitter_account.access_token
    ATS = twitter_account.access_token_secret
    return CK, CS, AT, ATS


def createTwitterObj (CK, CS, AT, ATS):
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, ATS)
    twitter_api = tweepy.API(auth)
    return twitter_api


def setSecTwitterSpecialist():
    account_list = ['JVNiPedia','jpcert','jvnjp']
    return account_list


def aquireTweetDataByApi (twitter_api, account_id, tweetdata):
    # 各アカウントごとにリツイートやリプライ以外のツイート内容を取得し、2次元配列に追加
    [tweetdata.append([tweet.id, tweet.user.screen_name, str(tweet.created_at), tweet.text, tweet.favorite_count, tweet.retweet_count])
    for tweet in tweepy.Cursor(twitter_api.user_timeline, id=account_id).items(10) 
    if (list(tweet.text)[:2]!=['R', 'T']) & (list(tweet.text)[0]!='@')]
    return tweetdata


if __name__ == "__main__":
    main()
