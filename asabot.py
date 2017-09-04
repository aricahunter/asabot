import asynctwitch
import asyncio
import random
import threading
from twitch import TwitchClient
import pickle
import urllib.request, json
import time
import html
import re

users = pickle.load(open("users.p", "rb"))
clientId = "68j3ah92fh1w0mcplw3uub7qpf1mby"
clientSecret = "0e4yq0gxaf5o7t558bd1rq8o3r10aw"
oauth = "f4jch2wzx8jc4xhkoy2neqlsr952fk"
chatoauth = "oauth:cpbspovyrt2s9hrny5a3p1slrtbktm"
channel = "asevera"
followersDict = {}

#500 feed freya
#special bot command?
#2000 pick a sitcker to go on asa
#4000 asa will write your name or other small phrase in calligraphy
#8000 asa will dance a dance of your choosing
#YMCA, Macarena, watch me whip, thriller, chicken dance, the hustle

#####################
######CONSTANTS######
#####################
color = "BlueViolet"
instagramUrl = "https://www.instagram.com/asevera_twitch/?hl=en"
twitterUrl = "https://twitter.com/aseveragaming"
amazonUrl = "https://www.amazon.com/gp/registry/wishlist/MRWZBVJZNF0T"
initialQuestionDelay = 60*5
initialInstagramDelay = 60*30
initialTwitterDelay = 60*10
initialAmazonDelay = 60*20
questionDelay = 60*15
answerDelay = int(60*1.5)
instagramDelay = 60*30
twitterDelay = 60*30
amazonDelay = 60*30
subMultiplier = 1.25
checkFollowersDuration = 60
commentPoints = .1
minutePoints = 2
gambleOdds = 1.0/3
gambleRewardMultiplier = 2
bitValue = .5
client = TwitchClient(client_id=clientId, oauth_token=oauth)
user = client.users.translate_usernames_to_ids([channel])[0]
meow = client.users.translate_usernames_to_ids([channel])[0]
subscribers = client.channels.get_subscribers(user.id)
subNames = []
for sub in subscribers:
    subNames.append(sub["user"]["name"])
followers = client.channels.get_followers(user.id)
for follower in followers:
    followersDict[follower["user"]["name"]] = ""

chatQuestions = []
with urllib.request.urlopen("https://opentdb.com/api.php?amount=100&category=15&type=multiple") as url:
    data = json.loads(url.read().decode())
    questions = data["results"]
    for question in questions:
        chatQuestions.append([html.unescape(question["question"]),html.unescape(question["correct_answer"])])

def makeUser(name):
    userDict = {}
    userDict["name"] = name
    userDict["comments"] = 0
    userDict["minutes"] = 1
    userDict["bits"] = 0
    userDict["points"] = minutePoints
    userDict["totalPoints"] = minutePoints
    return userDict



# Use the pre-made CommandBot, to handle messages yourself, use asynctwitch.Bot and handle event_message.
bot = asynctwitch.CommandBot(
    user = "Brave_Little_Bot",
    oauth = chatoauth,
    channel = "asevera",
    prefix = "!",
)
def sendMessage(message):
    for i in (bot.say(channel,"/me "+message)):
        continue


@asyncio.coroutine
def event_subscribe(self, message, tags):
    userName = message.author.name
    subNames.append(userName)
    sendMessage(userName + ", thanks for the sub. Asevera really appreciates the support. Much love <3")

@bot.override
async def event_message(message):
    text = message.content.lower()
    userName = message.author.name
    if userName not in users.keys():
        users[userName] = makeUser(userName)

    bits = re.findall('cheer(\d+)', text)
    for bit in bits:
        print("found bits")
        users[userName]["bits"] += int(bit)
        users[userName]["points"] += int(bit)*bitValue
        users[userName]["totalPoints"] += int(bit)*bitValue

    multiplier = 1
    if userName == subNames:
        multiplier = subMultiplier

    users[userName]["points"] += commentPoints * multiplier
    users[userName]["totalPoints"] += commentPoints * multiplier
    users[userName]["comments"] += 1
    if (text == "!points" or text == "!moonies"):
        sendMessage(userName + " has "+str(int(users[userName]["points"]))+" moonies")
    elif (text == "!totalpoints" or message == "!totalmoonies"):
        sendMessage(userName + " has "+str(int(users[userName]["totalPoints"]))+" total moonies")
    elif (text == "!leaderboard" or text == "!leaders"):
        values = []
        for u in users.keys():
            values.append([int(users[u]["totalPoints"]), u])
        values.sort(key=lambda x: x[0], reverse=True)
        printValue = ""
        for v in values[0:10]:
            printValue += v[1] + "|" + str(v[0])+" - "
        sendMessage(printValue)
    elif (text == "!comments"):
        sendMessage(userName + " has sent "+str(int(users[userName]["comments"]))+" messages")
    elif (text == "!minutes"):
        sendMessage(userName + " has spent " + str(int(users[userName]["minutes"])) + " minutes on this channel")
    elif (text == "!bits"):
        sendMessage(userName + " has given " + str(int(users[userName]["bits"])) + " bits")
    elif (text.startswith("!give") and userName.lower() == "asevera"):
        parts = text.split(" ")
        if len(parts) == 3:
            try:
                points = int(parts[2])
                name = parts[1]
                if name[0] == "@":
                    name = name[1:]
                users[name]["points"] += points
                users[name]["totalPoints"] += points
            except ValueError:
                pass
    pickle.dump(users, open("users.p", "wb"))


def giveChatPointsHelper():
    stream = client.streams.get_stream_by_user(meow.id, stream_type='all')
    if stream != None:
        with urllib.request.urlopen("https://tmi.twitch.tv/group/user/"+channel+"/chatters") as url:
            data = json.loads(url.read().decode())
            chatters = data["chatters"]["viewers"]
            moderators = data["chatters"]["moderators"]
            if "moobot" in moderators: moderators.remove("moobot")
            if "brave_little_bot" in moderators: moderators.remove("brave_little_bot")
            total = chatters + moderators
            for user in total:
                user = str(user)
                if user not in users.keys():
                    userEntry = makeUser(user)
                    users[user] = userEntry
                else:
                    users[user]["points"] += minutePoints
                    users[user]["totalPoints"] += minutePoints
                    users[user]["minutes"] += 1
            pickle.dump(users, open("users.p", "wb"))
    threading.Timer(checkFollowersDuration, giveChatPointsHelper).start()

def askQuestion():
    question = chatQuestions[0]
    sendMessage(question[0])
    threading.Timer(questionDelay, askQuestion).start()
    threading.Timer(answerDelay, sendAnswer).start()
def sendAnswer():
    question = chatQuestions.pop(0)
    sendMessage(question[1])

def checkFollowersHelper():
    followers = client.channels.get_followers(user.id)
    for follower in followers:
        followerName = follower["user"]["name"]
        if followerName not in followersDict.keys():
            sendMessage("Hey "+follower["user"]["name"]+"!!! Thanks for the follow :)")
            followersDict[followerName] = ""
    threading.Timer(checkFollowersDuration, checkFollowersHelper).start()
def twitterHelper():
    sendMessage("Follow Asevera's Twitter for stream notifications!  "+twitterUrl)
    threading.Timer(twitterDelay, twitterHelper).start()
def instagramHelper():
    sendMessage("Check out Asevera's instagram. She appreciates the support :)  "+instagramUrl)
    threading.Timer(instagramDelay, instagramHelper).start()
def amazonHelper():
    sendMessage("You can support Asevera by getting her a little something from her Amazon wishlist. Every bit helps <3  "+amazonUrl)
    threading.Timer(amazonDelay, amazonHelper).start()
def setColorHelper():
    for i in bot.say(channel, "/color "+color):
        continue
def twitter():
    threading.Timer(initialTwitterDelay, twitterHelper).start()
def instagram():
    threading.Timer(initialInstagramDelay, instagramHelper).start()
def checkFollowers():
    threading.Timer(checkFollowersDuration, checkFollowersHelper).start()
def giveChatPoints():
    threading.Timer(checkFollowersDuration, giveChatPointsHelper).start()
def amazon():
    threading.Timer(initialAmazonDelay, amazonHelper).start()
def setColor():
    threading.Timer(30, setColorHelper).start()
def postQuestion():
    threading.Timer(initialQuestionDelay, askQuestion).start()

postQuestion()
instagram()
twitter()
amazon()
giveChatPoints()
checkFollowers()
setColor()

bot.start()