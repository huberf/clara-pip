def handle_modifiers(modifiers):
    for i in modifiers:
        VAR_REGISTRY[i['name']] += i['val']

def calc_qualifiers(qualifier):
    registryValue = VAR_REGISTRY[qualifier['name']]
    try:
        if registryValue > qualifier['$gt']:
            return True
        else:
            return False
    except:
        # Not a greater than qualifier
        doNothing = True
    try:
        if registryValue == qualifier['$eq']:
            return True
        else:
            return False
    except:
        # Not an equal to qualifier
        doNothing = True
    try:
        if regsitryValue < qualifier['$lt']:
            return True
        else:
            return False
    except:
        # Not a less than qualifier
        doNothing = True
    # Legacy qualifier types
    try:
        if registryValue == qualifier['val']:
            return True
        else:
            return False
    except:
        # Not a less than qualifier
        doNothing = True
    # if supplied info doesn't fit any of the above qualifier types reject
    return False
