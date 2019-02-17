{
  "starters": ["Let's start story time", "Let's do a story"],
  "response": "It was a dark and stormy night. Would you like to go outside? (out,in)",
  "next": [
    {
      "starters": ["in"],
      "response": "The house suddenly shudders and creaks as a wind gust buffets against it. The windows shatter as hail begins to fall. (outside,basement)",
      "next": [
        { "starters": ["outside"],
          "response": "You get struck by hail and die."
          "id": "hail-death"
        },
        { "starters": ["basement"],
          "response": "You creep downstairs as the musty odors of the basement waft up. (open basement, go back upstairs)",
          "next": [
            { "starters": "open basement",
              "response": "A ghoul leaps forward. You die."
            },
            { "starters": "go back upstairs",
              "response": "It was all an illusion. You win!"
            }
          ]
        }
      ]
    },
    { "starters": ["out"],
      "response": "The door creaks open and you emerge into the heart of the storm. (look up, look down)",
      "next": [
        { "starters": ["look up"],
          "response": "You see hail begin to fall. (run,back inside)",
          "next": [
            { "starters": ["run"], "target": "hail-death" },
            { "starters": ["back inside"], "target": "hail-death" }
            ]
        },
        { "starters": ["look down"],
          "response": "You see hail start to fall. (run,back inside)",
          "next": [
            { "starters": ["run"], "target": "hail-death" },
            { "starters": ["back inside"], "target": "hail-death" }
            ]
        }
      ]
    }
  ]
}
