print('Enter the file title you want to add to.')
name = input('file: ')
convoFile = open('convos/' + name + '.convo', 'w')

shouldEnd = False
while not shouldEnd:
    print('Enter the possible queries separated by ;')
    queries = input('> ')

    print('Enter the response separated by ;')
    response = input('> ')

    out = 'Q: ' + queries + '\n'
    out += 'R: ' + response
    convoFile.write(out)

convoFile.close()
