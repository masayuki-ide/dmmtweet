import urllib.request
from requests_oauthlib import OAuth1Session
from bs4 import BeautifulSoup
from TwitterAPI import TwitterAPI
import requests
import tweepy
import os


#認証を行う
consumer_key = "TrWhvaA3Wtq9iZolfF7GOqCvr"
consumer_secret = "wxxxVs58dA04dY8x7Q9cIhfeEPHf7xMNgO9x7AfiSugk5omess"
access_token = "911220352046395392-2kqMRJfS1kjKUM35HyvaGNvVAiqdytO"
access_secret = "RyIZwMTjqZE4NxRcNETL34TyTwcqoJb96f9pUM46WcadT"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update_with_media.json"

APPID = "YHhCqqXCAF6zCGAWd9WK"
AFFILIATEID = "deeei-999"
# 新人
# KEYWORD = "%E6%96%B0%E4%BA%BA&rlz=1C5CHFA_enJP684JP686&oq=%E6%96%B0%E4%BA%BA"
# 紗倉まな
KEYWORD = "%E7%B4%97%E5%80%89%E3%81%BE%E3%81%AA&rlz=1C5CHFA_enJP684JP686&oq=%E7%B4%97%E5%80%89%E3%81%BE%E3%81%AA"


html = urllib.request.urlopen("https://api.dmm.com/affiliate/v3/ItemList?api_id=" + APPID + "&affiliate_id=" + AFFILIATEID + "%20&site=DMM.R18&service=digital&floor=videoa&hits=10&sort=date&keyword=" + KEYWORD + "&output=xml")
soup = BeautifulSoup(html, "html5lib")

print("所得したデータを表示します")
print(soup.prettify())

#タイトル・女優・画像URL・動画URLを追加

items = soup.items
print("取得したitems数:{}".format(len(items.item)))
for item in items:
    print("-------------")
    title = item.title.string
    title = (title[:40] + "..動画はこちら→")if len(title) > 75 else title #タイトル４０字過ぎたら省略
    print("title:{}".format(title))
    photoURL = item.imageurl.large.string
    print("photoURL:{}".format(photoURL))

    try:
        videoURL = item.samplemovieurl.size_476_306.string
        print("videoURL:{}".format(videoURL))

        #ツイート内容
        content = title + "|" + videoURL
        print("ツイート内容：{}".format(content))

        request = requests.get(photoURL, stream=True)
        filename = "temp.jpg"
        if request.status_code == 200:
            print("status_code == 200")
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            api.update_with_media(filename, status= content)
            print("ツイートに成功")
            os.remove(filename)
        else:
            print("画像のダウンロード失敗")
    except Exception as e:
        print(e)
print("プログラム終了")
