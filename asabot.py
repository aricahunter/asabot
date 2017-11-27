import asynctwitch
import asyncio
import sentence
import random
import threading
from twitch import TwitchClient
import pickle
import urllib.request, json
import html
import re



try:
    prizes = pickle.load(open("prizes.p", "rb"))
except (FileNotFoundError) as e:
    prizes = {}
    prizes["giveaway"] = {}
    prizes["raffle"] = {}
    prizes["giveaway"]["details"] = "There is currently no giveaway happening"
    prizes["raffle"]["details"] = "There is currently no lottery happening"
    prizes["giveaway"]["fee"] = 0
    prizes["raffle"]["fee"] = 0
    prizes["giveaway"]["users"] = {}
    prizes["raffle"]["users"] = {}

    pickle.dump(prizes, open("prizes.p", "wb"))

ranks = [("Crawler",0), ("Land Soldier",130), ("Sky Warrior",650), ("Space Captain",2000), ("Moon King",5000), ("Solar Guardian",10000), ("Galactic Overlord",20000), ("Universe Conquerer",50000), ("Master of the Multiverse",100000), ("Freya",1000000)]
users = pickle.load(open("users.p", "rb"))
clientId = "68j3ah92fh1w0mcplw3uub7qpf1mby"
clientSecret = "0e4yq0gxaf5o7t558bd1rq8o3r10aw"
oauth = "f4jch2wzx8jc4xhkoy2neqlsr952fk"
chatoauth = "oauth:cpbspovyrt2s9hrny5a3p1slrtbktm"
channel = "asevera"
followersDict = {}
peopleInChat = []

#300 feed freya
#2500 pick a costume
#5000 asa will write your name or other small phrase in calligraphy
#10000 asa will dance a dance of your choosing
#YMCA, Macarena, watch me whip, thriller, chicken dance, the hustle

#####################
######CONSTANTS######
#####################
color = "BlueViolet"
instagramUrl = "https://www.instagram.com/asevera_twitch/?hl=en"
twitterUrl = "https://twitter.com/aseveragaming"
amazonUrl = "https://www.amazon.com/gp/registry/wishlist/MRWZBVJZNF0T"
initialQuestionDelay = 60*18
initialInstagramDelay = 60*30
initialTwitterDelay = 60*10
initialAmazonDelay = 60*20
questionDelay = 60*18
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
feedFreyaPoints = 250
costumePoints = 2000
calligraphyPoints = 5000
dancePoints = 10000

client = TwitchClient(client_id=clientId, oauth_token=oauth)
user = client.users.translate_usernames_to_ids([channel])[0]
subscribers = client.channels.get_subscribers(user.id)
subNames = []
print(len(subscribers))
for sub in subscribers:
    subNames.append(sub["user"]["name"])

offset = 0
followers = client.channels.get_followers(user.id, limit=100, offset=offset)
while len(followers) > 0:
    for follower in followers:
        followersDict[follower["user"]["name"]] = ""
    offset += 100
    followers = client.channels.get_followers(user.id, limit=100, offset=offset)

chatQuestions = []
with urllib.request.urlopen("https://opentdb.com/api.php?amount=20&category=15") as url:
    data = json.loads(url.read().decode())
    questions = data["results"]
    for question in questions:
        answers = [html.unescape(question["correct_answer"])]
        for ans in question["incorrect_answers"]:
            answers.append(html.unescape(ans))
        chatQuestions.append([html.unescape(question["question"]),
                              answers])
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

    bits = re.findall('cheer(\d+)', text) + \
           re.findall('bday(\d+)', text) + \
           re.findall('ripcheer(\d+)', text) + \
           re.findall('kappa(\d+)', text) + \
           re.findall('trihard(\d+)', text) + \
           re.findall('kreygasm(\d+)', text) + \
           re.findall('4head(\d+)', text) + \
           re.findall('swiftrage(\d+)', text) + \
           re.findall('notlikethis(\d+)', text) + \
           re.findall('failfish(\d+)', text) + \
           re.findall('yohiyo(\d+)', text) + \
           re.findall('pjsalt(\d+)', text)
    for bit in bits:
        users[userName]["bits"] += int(bit)
        users[userName]["points"] += int(bit)*bitValue
        users[userName]["totalPoints"] += int(bit)*bitValue

    multiplier = 1
    if userName in subNames:
        multiplier = subMultiplier

    users[userName]["points"] += commentPoints * multiplier
    users[userName]["totalPoints"] += commentPoints * multiplier
    users[userName]["comments"] += 1
    if (text == "!points" or text == "!moonies"):
        sendMessage(userName + " has "+str(int(users[userName]["points"]))+" moonies")
    elif (text == "!totalpoints" or text == "!totalmoonies"):
        sendMessage(userName + " has "+str(int(users[userName]["totalPoints"]))+" total moonies")
    elif (text == "!leaderboard" or text == "!leaders"):
        values = []
        for u in users.keys():
            if u != channel and u != 'bagelsandmalt' and u != '4r1c':
                values.append([int(users[u]["totalPoints"]), u])
        values.sort(key=lambda x: x[0], reverse=True)
        printValue = ""
        for v in values[0:10]:
            printValue += v[1] + "|" + str(v[0])+" - "
        sendMessage(printValue)
    elif (text == "!commands"):
        res = "!comments !moonies !totalmoonies !minutes !bits !why !leaders !ranks !rank !feedfreya (300 moonies) !costume (2500 moonies) !calligraphy (5000 moonies)"
        sendMessage(res)
    elif (text == "!comments"):
        sendMessage(userName + " has sent "+str(int(users[userName]["comments"]))+" messages")
    elif (text == "!minutes"):
        sendMessage(userName + " has spent " + str(int(users[userName]["minutes"])) + " minutes on this channel")
    elif (text == "!why"):
        sendMessage(sentence.makeWhy(peopleInChat))
    elif (text == "!bits"):
        sendMessage(userName + " has given " + str(int(users[userName]["bits"])) + " bits")
    elif (text == "!feedasevera"):
        sendMessage("Hey Asevera!!! "+userName + " would liek you to eat some yummies :)")
    elif (text == "!feedfreya" and users[userName]["points"] > feedFreyaPoints):
        users[userName]["points"] -= feedFreyaPoints
        sendMessage("@asevera. "+ userName + " has requested that you feed Lady Freya")
    elif (text == "!ranks"):
        res = ""
        for rank in ranks:
            res += rank[0] + "-" + str(rank[1]) + " "
        sendMessage(res)
    elif (text == "!rank"):
        i = 0
        points = users[userName]["totalPoints"]
        while i < len(ranks):
            if ranks[i][1] >  points:
                break
            i += 1
        i = i-1
        sendMessage(ranks[i][0])
    elif (text == "!costume" and users[userName]["points"] > costumePoints):
        users[userName]["points"] -= costumePoints
        sendMessage("@asevera. " + userName + " has requested that you adorn a costume")
    elif (text == "!calligraphy" and users[userName]["points"] > calligraphyPoints):
        users[userName]["points"] -= calligraphyPoints
        sendMessage("@asevera. " + userName + " has requested masterful calligraphy")
    elif (text == "!dance"):
        users[userName]["points"] -= dancePoints
        sendMessage("@asevera. " + userName + " has requested a whimsical boogie")
    elif (text.startswith("!give ") and userName == channel):
        parts = text.split(" ")
        if len(parts) == 3:
            try:
                points = int(parts[2])
                name = parts[1]
                if name[0] == "@":
                    name = name[1:]
                users[name]["points"] += points
                users[name]["totalPoints"] += points
                sendMessage("Asa has given "+name+" "+str(points)+" points")
            except ValueError:
                pass
    elif (text.startswith("!giveaway ") and userName == channel):
        parts = text.split(" ",2)
        print(parts)
        if (len(parts) == 3):
            try:
                prizes["giveaway"]["details"] = parts[2]
                prizes["giveaway"]["fee"] = int(parts[1])
                prizes["giveaway"]["users"] = {}
                sendMessage("Asevera has created a give away. Get details with !giveaway and enter with !entergiveaway")
            except Exception:
                pass
    elif (text.startswith("!raffle ") and userName == channel):
        parts = text.split(" ", 2)
        if (len(parts) == 3):
            try:
                prizes["raffle"]["details"] = parts[2]
                prizes["raffle"]["fee"] = int(parts[1])
                prizes["raffle"]["users"] = {}
                sendMessage("Asevera has created a raffle. Get details with !raffle and enter with !raffle")
            except Exception:
                pass
    elif (text == "!giveaway"):
        sendMessage(prizes["giveaway"]["details"] + " - " + str(prizes["giveaway"]["fee"]) + " moonies. Use !entergiveaway to enter.")
    elif (text == "!raffle"):
        sendMessage(prizes["raffle"]["details"] + " - " + str(prizes["raffle"]["fee"]) + " moonies. Use !enterraffle to enter.")
    elif (text == "!entergiveaway" and users[userName]["points"] >= prizes["giveaway"]["fee"]):
        if (userName in prizes["giveaway"]["users"].keys()):
            sendMessage("@"+userName+" you are already entered in the giveaway")
        else:
            prizes["giveaway"]["users"][userName] = 1
            users[userName]["points"] -= prizes["giveaway"]["fee"]
    elif (text == "!enterraffle" and users[userName]["points"] >= prizes["raffle"]["fee"]):
        if (userName in prizes["raffle"]["users"]):
            prizes["raffle"]["users"][userName] = prizes["raffle"]["users"][userName]+1
        else:
            prizes["raffle"]["users"][userName] = 1
        users[userName]["points"] -= prizes["giveaway"]["fee"]
    elif (text == "!giveawaywinner" and userName == channel):
        selectWinner(prizes["giveaway"]["users"])
    elif (text == "!rafflewinner" and userName == channel):
        selectWinner(prizes["raffle"]["users"])
    pickle.dump(prizes, open("prizes.p", "wb"))
    pickle.dump(users, open("users.p", "wb"))

def selectWinner(dict):
    names = []
    points = []
    for u in dict.keys():
        names.append(u)
        points.append(dict[u])
    randNumber = random.randint(0,sum(points)-1)
    i = 0
    print(randNumber)
    while randNumber > 0:
        randNumber -= points[i]
        i += 1
    print(i)
    sendMessage("THE WINNER IS............. @"+names[i])

def giveChatPointsHelper():
    stream = client.streams.get_stream_by_user(user.id, stream_type='all')
    if stream != None:
        with urllib.request.urlopen("https://tmi.twitch.tv/group/user/"+channel+"/chatters") as url:
            data = json.loads(url.read().decode())
            chatters = data["chatters"]["viewers"]
            moderators = data["chatters"]["moderators"]
            if "moobot" in moderators: moderators.remove("moobot")
            if "brave_little_bot" in moderators: moderators.remove("brave_little_bot")
            total = chatters + moderators
            peopleInChat = total
            for u in total:
                u = str(u)
                multiplier = 1
                if u in subNames:
                    multiplier = subMultiplier
                if u == 'meowsymister':
                    multiplier = .7

                if u not in users.keys():
                    userEntry = makeUser(u)
                    users[u] = userEntry
                else:
                    users[u]["points"] += minutePoints*multiplier
                    users[u]["totalPoints"] += minutePoints*multiplier
                    users[u]["minutes"] += 1
            pickle.dump(users, open("users.p", "wb"))
    threading.Timer(checkFollowersDuration, giveChatPointsHelper).start()

def askQuestion():
    question = chatQuestions[0]
    sendMessage(question[0])
    answers = question[1][:]
    random.shuffle(answers)
    options = ""
    i = 0
    for ans in answers:
        i += 1
        options += " " + str(i)+". " + ans
    sendMessage(options)
    threading.Timer(questionDelay, askQuestion).start()
    threading.Timer(answerDelay, sendAnswer).start()
def sendAnswer():
    question = chatQuestions.pop(0)
    sendMessage(question[1][0])

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
print("hello")