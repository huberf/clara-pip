import json
import uuid

STORY_INDEX = {}

def load_story(file_name):
    contents = json.loads(open(file_name).read())
    convos = recursive_build(contents, None)

def recursive_build(json_cont, parent_id):
    to_return = []
    this_convo = {}
    this_id = str(uuid.uuid1())
    this_convo['starters'] = json_cont['starters']
    try:
        if this_convo['target']:
            this_convo['replies'] = []
            for i in STORY_INDEX[this_convo['target']]['replies']:
                this_convo += [this_convo[0]] # FORCE FAILURE
    except:
        this_convo['replies'] = [{
            'text': json_cont['response'],
            'context': [{'name': this_id, 'starting': True},{'name': parent_id, 'starting': False} if not parent_id == None else {'name': this_id, 'starting': True}]
        }]
        to_return += [this_convo]
        try:
            STORY_INDEX[json_cont['id']] = this_convo
        for i in json_cont['next']:
            to_return += recursive_build(i, this_id)
    return to_return