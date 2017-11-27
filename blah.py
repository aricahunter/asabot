with open('./test.txt', 'r') as content_file:
    content = content_file.read()
    for char in content:
        print(char)
