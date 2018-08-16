# Clara Pip Package

Conversational UI? Digital companion? The clara system can act as a stand alone chitchat framework or can easily be used to augment an existing chatbot by handling general small talk or non-command based queries. Clara uses JSON conversation files containing possible inputs and corresponding responses to match the best response to the user's query using the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) so even if they make a typo or type a query not included, it will still deliver a proper response. The system also has a dynamic emotional state which can affect the responses the system gives if made use of.

This is an early version, and has only recently graduated from being a fun experiment. However, it has worked very well in my systems and tests, and could prove to be immensenly useful to chatbot developers or those trying to build their own artificial companion.

## Setup (With Pip)
* Run `pip install clara`
* Create a new directory and enter it such as `mkdir clara`
* Type `clara create` and you can now run `python3 chat.py` to begin.

## Setup (Technical)

1. Run `git clone https://github.com/huberf/clara-pip`
2. Now `cd` into the `clara-pip` directory.
3. Run `pip3 install clara` and then run `clara create`. Now, try running `python3 brain.py`. If you get requirement errors, `pip3` them
   into your instance.
4. If the command didn't return an error, try typing `Hello!` into the input box
   that should be present on the command line.
5. All messages and accompanying responses are located in the `convos/`
   directory. You can easily add conversation scripts others made by simply
   copying them into this directory. On startup, the program will load all data
   from any JSON file in that directory.
6. This is messy so pulling from the pip setup is recommended for any use case
   not requiring customizing the package code.

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

## Modifiers and Context in Convo Files
After a single reply option (which are separated by the `;` character), one can
use a `\` to signify the inclusion of modifiers and context which are then
separated by the `.` character. For example,
`This is an example reply.\exampleContext.useful=3; Why should I give an example
reply.\useful=-2.aggravatedResponse`
Modifiers can then be used when qualifying responses (such as only reply
with `I'm glad I could help` if `useful>1`.

#### Context Logic
If a response is selected with a given context this context is saved in a
recency hash table. If the next thing a user types includes another response
with the exact same context as a context in the last response, that response
will be selected. This provides continuity. For example if one context for the
response `Type in ABC Publishing to your favorite GPS app` is
`askingForDirections`, and the user then says `What do you mean?` you could then
have a follow up response with the assigned context of `askingForDirections` and
provide a more detailed reply.

## Knowledge Files
Knowledge allows the Clara system to connect words or phrases with classes of
information. For example, `Hello, Hey, Hi` are all `Greetings` so with the new
system you can now respond to all greetings by creating a file such as
`test.knowledge` in the `knowledge/` directory of your Clara bot.
In it, you would write.
```
Hello|greeting
Hey|greeting
Hi|greeting
Hello there|greeting
```
And then to respond setup a convo file with:
```
Q: %{greeting}
R: Hi! How are you?
```
In any `.knowledge` file the list following the word or phrase is a comma
separated list of classifications the word or phrase falls under.

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
