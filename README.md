# telegram_export_handler
Program to more easily work with exported (as-json) telegram messages

This program aims to:

1. offer multiple methods to display telegram data
2. offer many methods of filtering telegram data

## REQUIREMENTS

Python3 for sure

Probably need linux - not tested in windows

Uncertain what external libraries - need to check

## SETUP

At this stage, I didn't properly virtualize my environment.... should viritualize 

The user should update the config file to express their directories

## USAGE

Program presently has two display methodologies:

1. Flask app
2. Usage of the 'ChatMessageManager' - this can be easily invoked from script.py 

### FLASK

Take a look at flask_app.py for available routes 

Spin up the flask server, have fun!

```
python3 flask_app.py
```

### ChatMessageManager

#### Architecture

ChatMessageManager expresses how data is loaded, how it is written, and high level reporting. ALL INTERACTION WITH TELEGRAM DATA IS CONDUCTED THROUGH THE MANAGER

The ChatMessageManager stores telegram json data in the instance variable 'messages'.  Each message is a ChatMessage class object, and they  are stored in a ChatMessageCollection class - this class provides methods for filtering/grouping/sorting data.  Convenience methods allow one to treat the ChatMessageCollection class as if it were a list.

The ChatMessage class is comprised of components (i.e. video/pdf/image/text/links/etc).  The class itself stores a dict derived from the json we loaded/parsed in the ChatMessageManager class.  If a change is to be made to the data it should be made to the dict itself.

#### Using

1. Instantiating a ChatMessageManager class and loading json

```
from chat_message_manager import ChatMessageManager


CMM = ChatMessageManager()
CMM.load_messages_from_base_and_designated()  # uses base/designated directories form config file to load json data from

# Alternative Loads:
# 1. load from file
CMM.load_messages_from_file(<directory>, <filename>)

# 2. from directory
CMM.load_messages_from_directory(<directory>, <filename>)

# 3. from existing chat message collection
CMM.load_messages_from_collection(<collection>)

```

2. Accessing your loaded 'messages' (ChatMessageCollection) and playing with the class methods

```
len(CMM.messages) # get the count of messages

CMM.messages.having_text_like('covid')  # retries a new collection of messages containing the word 'covid' in text

CMM.messages.having_links_like('nih.gov').having_text_like('mask') #chained filtering

# There are many other methods, please review interactors/chat_message_collection.py for more information
```

3. Drilling into the individual message level

```
CMM.messages[0]  # access to retrieve a specific message

CMM.messages[0] > CMM.messages[1] # determines greater-than/less-than based on date

CMM.messages[0] == CMM.messages[1] # true if files have same hash and text is same

CMM.messages[3].date() # get the date of the post

CMM.messages[3].links() # retrieve a list of Link class objects

CMM.messages[3].files() # retriieve a dict of all files for the message and their identified type

# for other methods, see models/chat_message.py
```

4. Drilling into the component layer (i.e. the text, each link, etc)

```
CMM.messages[0].links()[0].open()  # opens the link in default browser (applies to all file-like components)

CMM.messages[0].pdf().hashsum()  # compute file hashsum for same-file comparison(applies to all file-like components)

CMM.messages[0].image().filepath  # (applies to all file like objects)

# for more method information, check out the components in models/chat_message_components
# file objects inherit from a parent, others may also; check out the models/chat_message_components/parents folder for detail on parents
```

## CONTRIBUTING


YES! DO IT!!

I don't care that you are new, I don't care that your git experience is limited and you might screw up.  Dirty secret: every programmer was new once and even the 'experienced' programmers barely know what they are doing; google is still an ally. If you are willing to help me make this better fork this repository and make a pull request.  

