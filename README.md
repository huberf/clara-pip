# Clara Pip Package

Enables easy inclusion of the Clara system. For full customizability, setup from
the [main GitHub](https://github.com/huberf/clara-bot).

## Setup (With Pip)
* Run `pip install clara`
* Create a new directory and enter it such as `mkdir clara`
* Run `clara` and you can now run `python3 chat.py` to begin.

## Convo File Formats
All json files from the `convos/` directory are automatically loaded at startup.
Therefore, you can break your convo files into an infinite number of individual
convo files. All such files contain an array of objects with the following keys:
* `starters` - This is an array of possible things a user could say to initiate
  the responses mentioned directly below this.
* `replies` - This is an array of possible replies which are selected at random
  based upon the `weight` key for each reply value. Replies can also be reserved
  for only certain states such as a happiness level greater than 0. To use this
  functionality one need only include the `qualifiers` key which is an array of
  objects with the keys `name` and then either `{"$lt": 0}`, `{"$gt": 0}`, or
  `{"$eq": 0}` except with 0 being whatever value you wish the response to
  activate at against the less than, greater than, or equal to operators.
Here is an example JSON response file:
```
[
  {
    "starters": ["this is a test", "i am testing you"],
    "replies": [
      {"text": "Hello very happy world!", "weight": 1, "modifiers": 
        [
          {"name": "happy_level", "$gt": 2}
        ]
      },
      {"text": "Hello world!", "weight": 1, "modifiers": 
        [
          {"name": "happy_level", "$lte": 2}
        ]
      }
    ]
  }
]
```
A new simplified format in development is signified with the `.convo` suffix. It
uses newlines combined with a letter, colon and space to divide up the data.
Ex:
```
Q: Who are you?; What are you?; Tell me what you are.
R: I am an artificial intelligence bot.
Q: I enjoy programming.
R: Wow! I do too!; Programming is the best thing in the world.
```
It is much easier to add to than the JSON, but with a much more limited feature
set and doesn't include the ability to add conditional responses requiring
certain moods or modifying data inside the "brain".
Therefore, this convo format is meant for quickly adding new conversation info
that isn't expected to be commonly used. It is also planned to be used in future
machine learning response generation, where Clara could consume and process the
data from such a file and then generate brand new responses with what the system
learned. Therefore, in the future, the interpreter will support including chunks
of conversation that has a flow. For example:
```
X:
Q: Hello?
R: Hi! What are you up to?
Q: I am working on a coding project.
R: That is very neat. What language are you using?
Q: I am using JavaScript.
R: Very neat!
Q: I have to go now. Bye!
\X:
```
As this is still in development, the format will continue to update and morph,
and the JSON spec is still planned to be the main format for scripted responses.

## Server Mode

Clara can be run on a server with requests queued and then retreived.
To enable server mode add `{"iomode": "server"}` to your `config.json` file.
* POST `/api/v1/send/<session_id>` - Send a JSON object containing the field `input` such as
  `{"input": "What can you do?"}`.
* GET `/api/v1/get/<session_id>` - It returns a JSON object with the fields `new` and
  `message`. If `new` is `"true"`, this means a new response has been added to the
  queue and the field `message` contains this new message. At this point, this
  message has now been removed from the queue and subsequent calls will retreive
  the responses next in line.
* GET `/api/v1/io/blocking/<session_id>` - Send a JSON object containing the
  field `input` in the same fashion as the `\send` endpoint and it will return a JSON response
  identical to the `\get` endpoint with all responses in the queue for the given
  session.

## Contributing

Feel free to open an issue if you have an idea or feature request. To contribute
code or additional convos simply open a pull request.
