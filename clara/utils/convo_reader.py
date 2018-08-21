import json

def convert_to_json(raw):
    # Setup variable to return at end
    convo = []
    formatted = raw.split('Q: ')
    for a in formatted:
        if len(a) > 0:
            actual_data = a.split('\nR: ')
            # Separate out queries and generate multiple if ; exists
            queries = actual_data[0].split('; ')
            # Strip all newlines
            actual_data[1] = actual_data[1].replace('\n', '')
            replies = []
            for i in actual_data[1].split('; '):
                data = i.split('|')
                refined = data[0].split('\\')
                modifiers = [] # These are things that modify the systems emotions and make changes that would kick off events
                response_states = [] # These merely gives context to the response and enables one to have conversation flow
                try:
                    mods = refined[1].split('.')
                    for z in mods:
                        parts = z.split('=')
                        if len(parts) == 2:
                            modifiers += [ {'name': parts[0], 'val': int(parts[1])} ]
                        elif len(parts) == 1:
                            starting = False
                            name = parts[0]
                            if parts[0][0] == '^':
                                starting = True
                                name = parts[0][1:]
                            response_states += [ { 'name': name, 'starting': starting} ]
                except:
                    doNothing = True
                to_add = {'text': refined[0], 'weight': 1}
                to_add['modifiers'] = modifiers
                to_add['context'] = response_states
                try:
                    converted = json.loads(data[1])
                    try:
                        to_add['image'] = converted['image']
                    except:
                        do_nothing = True
                except:
                    do_nothing = True
                replies += [to_add]
            convo += [{
                'starters': queries,
                'replies': replies
                }]
    return convo
