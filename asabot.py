import asynctwitch
import asyncio
import sentence
import random
import threading
from twitch import TwitchClient
import pickle
import urllib.request, json
import re
import pygame

#with urllib.request.urlopen("https://tmi.twitch.tv/group/user/"+channel+"/chatters") as url:
prizes = pickle.load(open("prizes.p", "rb"))
donationsDict = {}
req = urllib.request.Request("https://www.twitchalerts.com/api/donations?access_token=FF5B9B46DA0B6A302D83", headers={'User-Agent': 'Mozilla/5.0'})
data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
for d in data["donations"]:
    donationsDict[d["id"]] = ""

pygame.mixer.init()
ranks = [("Crawler",0), ("Land Soldier",130), ("Sky Warrior",650), ("Space Captain",2000), ("Moon King",5000), ("Solar Guardian",10000), ("Galactic Overlord",20000), ("Universe Conquerer",50000), ("Master of the Multiverse",100000), ("Freya",1000000)]
users = pickle.load(open("users.p", "rb"))
clientId = "68j3ah92fh1w0mcplw3uub7qpf1mby"
clientSecret = "0e4yq0gxaf5o7t558bd1rq8o3r10aw"
oauth = "f4jch2wzx8jc4xhkoy2neqlsr952fk"
chatoauth = "oauth:cpbspovyrt2s9hrny5a3p1slrtbktm"
channel = "asevera"
followersDict = {}
peopleInChat = []
dances = []

#####################
######CONSTANTS######
#####################
color = "BlueViolet"
discordUrl = "https://discord.gg/C736duB"
instagramUrl = "https://www.instagram.com/asevera_tv/"
twitterUrl = "https://twitter.com/asevera_tv"
amazonUrl = "https://www.amazon.com/gp/registry/wishlist/MRWZBVJZNF0T"
initialDiscordDelay = 60*40
initialInstagramDelay = 60*30
initialTwitterDelay = 60*10
initialAmazonDelay = 60*20
discordDelay = 60*40
instagramDelay = 60*40
twitterDelay = 60*40
amazonDelay = 60*40
subMultiplier = 1.25
checkFollowersDuration = 120
commentPoints = .1
minutePoints = 4
gambleOdds = 1.0/3
gambleRewardMultiplier = 2
bitValue = .5
dancePoints = 50
feedFreyaPoints = 300
beanPoints = 800
costumePoints = 2000
calligraphyPoints = 5000
dancePoints = 50
allChatters = []
client = TwitchClient(client_id=clientId, oauth_token=oauth)

duel = {}
duelPoints = 100

offset = 0
user = client.users.translate_usernames_to_ids([channel])[0]
subscribers = client.channels.get_subscribers(user.id, limit=100, offset=offset)
subNames = {}
while len(subscribers) > 0:
    for sub in subscribers:
        subNames[sub["user"]["name"]] = ""
    offset += 100
    subscribers = client.channels.get_subscribers(user.id, limit=100, offset=offset)

print(len(subNames))

offset = 0
followers = client.channels.get_followers(user.id, limit=100, offset=offset)
totalFollowers = 0
while len(followers) > 0:
    for follower in followers:
        userInfo = {}
        userInfo["order"] = totalFollowers
        userInfo["date"] = follower["created_at"]
        followersDict[follower["user"]["name"]] = userInfo
        totalFollowers = totalFollowers+1
    offset += 100
    try:
        followerss = client.channels.get_followers(user.id, limit=100, offset=offset)
    except:
        followers = []
for follower in followersDict:
    followersDict[follower]["order"] = -1*(followersDict[follower]["order"]-totalFollowers)

def makeUser(name):
    userDict = {}
    userDict["name"] = name
    userDict["comments"] = 0
    userDict["minutes"] = 1
    userDict["bits"] = 0
    userDict["points"] = minutePoints
    userDict["totalPoints"] = minutePoints
    return userDict

scarySounds = ["scary1.wav", "scary2.wav",
               "scary4.wav",
               "scary7.wav", "scary8.wav",
               "scary10.wav", "scary11.wav",
               "scary13.wav"]

def playScarySound():
    """
    effect = pygame.mixer.Sound(random.choice(scarySounds))
    effect.play()
    """

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
    amount = 0
    for bit in bits:
        amount += int(bit)
        users[userName]["bits"] += int(bit)
    if amount >= 500:
        playScarySound()

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
        res = "!comments !moonies !totalmoonies !minutes !bits !why !dr !nd !dl !leaders !ranks !rank !feedfreya (300 moonies) !bean (800 moonies) !costume (2500 moonies) !calligraphy (5000 moonies)"
        sendMessage(res)
    elif (text == "!comments"):
        sendMessage(userName + " has sent "+str(int(users[userName]["comments"]))+" messages")
    elif (text == "!discord"):
        sendMessage(discordUrl)
    elif (text == "!minutes"):
        sendMessage(userName + " has spent " + str(int(users[userName]["minutes"])) + " minutes on this channel")
    elif (text == "!mooniesforall" and userName == channel):
        for p in peopleInChat:
            users[p]["points"] += 200
            users[p]["totalPoints"] += 200
        sendMessage("Everyone enjoy your 200 moonies")
    elif (text.startswith("!duel ")):
        other = text.split(" ")[1]
        if other[0] == "@":
            other = other[1:]
        duel[userName] = other
        if other in duel and duel[other] == userName:
            duel[userName] = "nothing"
            duel[other] = "nothing"
            r = random.uniform(0,1)
            users[other]["points"] -= duelPoints
            users[other]["totalPoints"] -= duelPoints
            users[userName]["points"] -= duelPoints
            users[userName]["totalPoints"] -= duelPoints
            if (r <0.45):
                users[userName]["points"] += 2*duelPoints
                users[userName]["totalPoints"] += 2*duelPoints
                sendMessage(userName + " wins the duel")
            elif (r>.55):
                users[other]["points"] += 2*duelPoints
                users[other]["totalPoints"] += 2*duelPoints
                sendMessage(other + " wins the duel")
            else:
                sendMessage("It's a double fatality. You both lose")
    elif (text == "!pot"):
        sendMessage("The pot currently has: $"+str(prizes["pot"]))
    elif (text == "!potadd" and userName == channel):
        prizes["pot"] += 10
        sendMessage("$10 added to pot")
    elif (text == "!potempty" and userName == channel):
        prizes["pot"] = 0
        sendMessage("Pot has been emptied")
    elif (text == "!why"):
        sendMessage(sentence.makeWhy(peopleInChat))
    elif (text == "!bits"):
        sendMessage(userName + " has given " + str(int(users[userName]["bits"])) + " bits")
    elif (text == "!feedasevera"):
        sendMessage("Hey Asevera!!! "+userName + " would liek you to eat some yummies :)")
    elif (text == "!feedfreya"):
        sendMessage("R.I.P Freya cam :(")
    elif (text == "!bean" and users[userName]["points"] > beanPoints):
        users[userName]["points"] -= beanPoints
        #sendMessage("NO MORE FOR THE LOVE OF GOD")
        sendMessage("@asevera. " + userName + " wants you to test your luck with a round of bean boozled")
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
    elif (text.startswith("!dr ") and users[userName]["points"] > dancePoints):
        dances.append([text[4:], userName])
        sendMessage(dances[-1][0] + " has been added")
    elif (text == "!justdance"):
        sendMessage("!moonies to see your moonies (you get 2/min). !dr <song name> to request (costs 50 moonies). Song list: http://justdance.wikia.com/wiki/Just_Dance_Unlimited")
    elif (text == "!dl"):
        danceList = ""
        for d in dances:
            danceList += ", "+" - ".join(d)
        sendMessage(danceList[2:])
    elif (text == "!jensen"):
        sendMessage("https://bit.ly/2wEvke3")
    elif (text == "!zook"):
        sendMessage("https://bit.ly/2PUIo7Q")
    elif (text == "!ed"):
        sendMessage("https://gyazo.com/f4b54f3e6e9caecb959fa7ef864843b4")
    elif (text == "!nd" and userName == channel):
        dance = dances.pop(0)
        users[dance[1]]["points"] -= dancePoints
        sendMessage(dance[0])
    elif (text == "!freyaspam"):
        sendMessage("aseverFreya "*random.randint(0,40))
    elif (text == "!when"):
        if (userName in followersDict):
            sendMessage("You were follower #"
                        +str(followersDict[userName]["order"])
                        + " - "
                        +str(followersDict[userName]["date"]))
    elif (text.startswith("!so ")):
        shoutout(text.split(" ")[1].replace('@',''))
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
                sendMessage("Asevera has created a raffle. Get details with !raffle, get your # of tickets with !raffletickets, and enter with !enterraffle")
            except Exception:
                pass
    elif (text == "!giveaway"):
        sendMessage(prizes["giveaway"]["details"] + " - " + str(prizes["giveaway"]["fee"]) + " moonies. Use !entergiveaway to enter.")
    elif (text == "!raffle"):
        sendMessage(prizes["raffle"]["details"] + " - " + str(prizes["raffle"]["fee"]) + " moonies. Use !enterraffle to enter and !raffletickets for # of tickets")
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
        users[userName]["points"] -= prizes["raffle"]["fee"]
    elif (text == "!giveawaywinner" and userName == channel):
        selectWinner(prizes["giveaway"]["users"])
    elif (text == "!raffletickets"):
        if (userName in prizes["raffle"]["users"]):
            sendMessage(userName + " has "+str(prizes["raffle"]["users"][userName]) + " tickets")
        else:
            sendMessage(userName + " has no raffle tickets")
    elif (text == "!rafflewinner" and userName == channel):
        selectWinner(prizes["raffle"]["users"])
    pickle.dump(prizes, open("prizes.p", "wb"))
    pickle.dump(users, open("users.p", "wb"))

def shoutout(name):
    persons = client.users.translate_usernames_to_ids([name])
    if len(persons) > 0:
        person = persons[0]
        personChannel = client.channels.get_by_id(person.id)
        sendMessage(personChannel["display_name"] + " has graced us with their presence. "
                                              + "They come from the land of " + str(personChannel["game"])
                                              + ". Show them some of our unparalleled moon patrol love")
def selectWinner(dict):
    names = []
    points = []
    for u in dict.keys():
        names.append(u)
        points.append(dict[u])
    randNumber = random.randint(0,sum(points)-1)
    i = 0
    while randNumber > 0:
        randNumber -= points[i]
        i += 1
    if names[i] == "meowsymister":
        selectWinner(dict)
    else:
        sendMessage("THE WINNER IS............. @"+names[i])

def giveChatPointsHelper():
    global peopleInChat
    stream = client.streams.get_stream_by_user(user.id, stream_type='all')
    if stream != None:
        try:
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
        except:
            pass
    threading.Timer(checkFollowersDuration, giveChatPointsHelper).start()

def checkFollowersHelper():
    global donationsDict
    followers = client.channels.get_followers(user.id)
    for follower in followers:
        followerName = follower["user"]["name"]
        if followerName not in followersDict.keys():
            sendMessage("Hey "+follower["user"]["name"]+"!!! Thanks for the follow :)")
            followersDict[followerName] = ""
        req = urllib.request.Request("https://www.twitchalerts.com/api/donations?access_token=FF5B9B46DA0B6A302D83",
                                     headers={'User-Agent': 'Mozilla/5.0'})
    """data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    for d in data["donations"]:
        if d["id"] not in donationsDict:
            donationsDict[d["id"]] = ""
            if float(d["amount"]) > 5:
                pass
                playScarySound()
    """
    threading.Timer(checkFollowersDuration, checkFollowersHelper).start()
def twitterHelper():
    sendMessage("Follow Asevera's Twitter for stream notifications!  "+twitterUrl)
    threading.Timer(twitterDelay, twitterHelper).start()
def discordHelper():
    sendMessage("Come hang out on discord!!!  "+discordUrl)
    threading.Timer(discordDelay, discordHelper).start()
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
def discord():
    threading.Timer(initialDiscordDelay, discordHelper).start()
def checkFollowers():
    threading.Timer(checkFollowersDuration, checkFollowersHelper).start()
def giveChatPoints():
    threading.Timer(checkFollowersDuration, giveChatPointsHelper).start()
def amazon():
    threading.Timer(initialAmazonDelay, amazonHelper).start()
def setColor():
    threading.Timer(30, setColorHelper).start()

discord()
instagram()
twitter()
amazon()
giveChatPoints()
checkFollowers()
setColor()

bot.start()