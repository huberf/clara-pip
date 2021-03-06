import json
import uuid

STORY_INDEX = {}

def space_indenting(lines):
    indents = 0
    for i in lines:
        if len(i) > 0:
            if i[0] == '\t':
                indents = 0
                break
            if i[0] == ' ':
                for j in i:
                    if j == ' ':
                        indents += 1
                    else:
                        break
                break
    return indents

def indents_in(line, indents):
    head_count = 0
    for i in line:
        if indents == 0:
            if i == '\t':
                head_count += 1
            else:
                break
        else:
            if i == ' ':
                head_count += 1
            else:
                break
    if indents == 0:
        return head_count
    else:
        return int(head_count/indents)

def break_to_groups(lines):
    groups = []
    last = []
    for i in lines:
        for j in i:
            if not j == '\t' and not j == ' ':
                if j == 'Q':
                    groups += [last]
                    last = []
                break
        last += [i]
    return groups[1:]

def groups_to_children(groups, indents):
    if len(groups) == 0:
        return []
    top_indent = indents_in(groups[0][0], indents)
    branches = []
    building_branch = []
    for i in groups:
        if indents_in(i[0], indents) == top_indent: # New branch start
            branches += [building_branch]
            building_branch = [None, None]
            building_branch[0] = i
            building_branch[1] = []
        else:
            building_branch[1] += [i]
    branches += [building_branch] # Add last branch
    branches = branches[1:] # First item is dud
    return branches

def load_storyfile(file_name):
    lines = open(file_name).read().split('\n')
    showresponses = False
    tick = -1 # will cause default of no line removal
    # look for header modifiers
    if lines[0] == 'HEADERSTART':
        tick = 1
        while not lines[tick] == 'HEADEREND':
            if lines[tick] == 'SHOWRESPONSES':
                showresponses = True
            tick += 1
    lines = lines[tick+1:]
    indents = space_indenting(lines)
    groups = break_to_groups(lines)
    json_cont = recursive_story_to_json(groups, indents, showresponses)
    clean_parent_ids(json_cont[0])
    if len(json_cont) > 0:
        convos = recursive_build(json_cont[0], None) # Stories always have a root start
    else:
        convos = []
    return convos


def convo_from_raw_lines(lines, formatted_next, showresponse=False):
    new_convo = {}
    found_reply = False
    for i in lines:
        remove_indent = i.strip(' ')
        # Get starters
        if remove_indent[0:2] == 'Q:':
            new_convo['starters'] = remove_indent[3:].split(';')
        # Try to get replies
        if remove_indent[0:2] == 'R:':
            new_convo['response'] = remove_indent[3:]
            found_reply = True
        if remove_indent[0:7] == 'TARGET:':
            new_convo['target'] = remove_indent[8:]
        # Add ID if exists
        if remove_indent[0:3] == 'ID:':
            new_convo['id'] = remove_indent[4:]
        # Now check if autoresponse addition is activated
        if remove_indent[0:12] == 'SHOWRESPONSE':
            showresponse = True
        if remove_indent[0:6] == 'PARENT':
            values = remove_indent.split(' ')
            num_up = int(values[1])
            new_convo['target'] = 'PARENT-{0}'.format(num_up)
    if showresponse:
        if len(formatted_next) > 0:
            suffix = '('
            for i in formatted_next:
                suffix += i['starters'][0] + ', '
            suffix = suffix[:-2]
            suffix += ')'
            new_convo['response'] += ' ' + suffix
    if found_reply and 'target' in new_convo.keys():
        del new_convo['target']
    new_convo['next'] = formatted_next
    return new_convo

def recursive_story_to_json(groups, indents, showresponses):
    if len(groups) == 0:
        return []
    top_indent = indents_in(groups[0][0], indents)
    convos = []
    branches = groups_to_children(groups, indents)
    for i in branches:
        root = i[0]
        children = recursive_story_to_json(i[1], indents, showresponses)
        new_convo = convo_from_raw_lines(root, children, showresponses)
        convos += [new_convo]
    '''
    last_convo = {}
    sub_groupings = []
    # Add processing of groups
    for i,val in enumerate(groups):
        if curr_indent(val[0]) == top_indent:
            last_convo['next'] = recursive_story_to_json(sub_groupings, indents)
            convos += [last_convo]
            last_convo = {}
            sub_groupings = []
            last_convo = { 'starters': val[0][2:].split(';'),
                            'response': val[1][2:] }
        else:
            sub_groupings += [val]
    '''
    return convos

def load_story(file_name):
    contents = json.loads(open(file_name).read())
    clean_parent_ids(contents)
    convos = recursive_build(contents, None)
    return convos

def clean_parent_ids(parsed_convos):
    # Takes PARENT macro and replaces with proper IDs
    return _recursive_clean_parent_ids([], parsed_convos)

def _recursive_clean_parent_ids(ids, convo_tree):
    try:
        if convo_tree['target'][0:6] == 'PARENT':
            num_up = int(convo_tree['target'][7:])
            convo_tree['target'] = ids[-(1+num_up)]
    except KeyError:
        pass
    my_id = ''
    try:
        my_id = convo_tree['id']
    except KeyError:
        my_id = str(uuid.uuid1()) # generate an ID
        convo_tree['id'] = my_id
    try:
        for i in convo_tree['next']:
            _recursive_clean_parent_ids(ids + [my_id], i)
    except KeyError: # reached end of branch
        pass

def recursive_build(json_cont, parent_id):
    to_return = []
    this_convo = {}
    this_id = str(uuid.uuid1())
    this_convo['starters'] = json_cont['starters']
    try:
        if json_cont['target']:
            this_convo['replies'] = []
            for i in STORY_INDEX[json_cont['target']]['replies']:
                this_convo['replies'] += [{'text': i['text'],
                    'context': [{'name': this_id, 'starting': True},{'name': parent_id, 'starting': False} if not parent_id == None else {'name': this_id, 'starting': True}]
                    }]
                #this_convo += [this_convo[0]] # FORCE FAILURE
            to_return += [this_convo]
    except:
        this_convo['replies'] = [{
            'text': json_cont['response'],
            'context': [{'name': this_id, 'starting': True},{'name': parent_id, 'starting': False} if not parent_id == None else {'name': this_id, 'starting': True}]
        }]
        to_return += [this_convo]
        try:
            STORY_INDEX[json_cont['id']] = this_convo
        except:
            pass
        try:
            for i in json_cont['next']:
                to_return += recursive_build(i, this_id)
        except:
            pass # This line has ended
    return to_return
