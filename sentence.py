import random

article = ["the", "my", "your", "our", "that", "this", "every", "the only"]
adjective = ["naked", "mysterious", "ugly", "happy", "negative", "grumpy", "poopy", "sexy", "handsome", "beautiful", "creative", "majestic", "stinky", "evil", "good", "mischevious", "tricky", "confused", "intellectual", "courageous", "brave", "gruesome", "scary"]
noun = ["fairy", "zombie", "kitten", "ghost", "dragon", "xbox", "PS4", "gamer", "nerd", "chicken", "unicorn", "tiger", "mom", "mermaid", "ballerina", "pig", "computer", "pizza", "taco", "pancake", "waffle", "puppy", "pony", "monkey"]
preposition = ["under", "in front of", "above", "behind", "near", "inside of", "beneath"]
place = ["the moon", "the universe", "the galaxy", "Wonderland", "Hyrule", "heaven", "hell", "the ocean", "the spaceship", "the moon"]
adverb = ["slowly", "accidentally", "always", "almost", "barely", "cautiously", "elegntly", "fiercely",  "foolishly", "gently", "gracefully", "lazily", "lovingly", "mysteriously", "playfully", "randomly", "suddenly", "surprisingly", "swiftly"]
verb = ["sings with", "serenades", "dances with", "runs", "attacks", "eats", "drinks", "destroys", "haunts", "blames", "begs", "enchants", "surprises", "loves", "blows up", "devours", "dreams about", "longs for", "battles", "craves", "despises", "believes in", "hates", "focuses on", "follows"]

def makeWhy(names):
    b = "Because "+random.choice(article)+" "
    if random.uniform(0,1) < 0.3333:
        b += random.choice(adjective)+" "

    if len(names) > 0 and random.uniform(0,1) < .5:
        b += random.choice(names)+" "
    else:
        b += random.choice(noun)+" "

    if random.uniform(0,1) < 0.33333:
        b += random.choice(adverb)+" "
    b += random.choice(verb)+" "
    b += random.choice(article)+" "
    if random.uniform(0,1) <0.3333:
        b += random.choice(adjective)+" "
    b += random.choice(noun)+" "
    if random.uniform(0,1) <= .5:
        b += "from"+" "+random.choice(place)
    return b