'''
You will be making an anagram app. You will take some letters as input from the user like eowm
and then you will find all words that can be spelled using those letters
to do this you will go through the words.txt file and store all of the words based on the letters they have.
so bat and tab would be stored in the same dictionary key. You should just use the sorted letters for the
dictionary key, so the dictionary would look like:
{"abt": ["bat", "tab"]}

''.join(sorted(word))

'''


f = open("words.txt","r")
lines = f.readlines()
dict = {}
for word in lines:
    word = word.strip()
    letters = ''.join(sorted(word))
    if letters in dict:
        dict[letters] = dict[letters] + [word]
    else:
        dict[letters] = [word]

while True:
    word = input("Enter some letters: ")
    letters = ''.join(sorted(word))
    if letters in dict:
        print(dict[letters])
