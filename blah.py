import shelve
users = shelve.open('users.db', writeback=True)
for k in users.keys():
    print(k)
    print(users[k])