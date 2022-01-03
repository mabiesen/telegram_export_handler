from models import chat_message as chat_msg
from interactors import chat_message_collection as chat_collection
from pathlib import Path
import json


class ChatMessageManager:
    # base directory is from a time where all messages were saved to one chat
    # designated directory has many chats that span just a few days
    PARENT_DIRECTORY = '/media/matt/hard_drv_wd/telegram/'
    BASE_DIRECTORY = PARENT_DIRECTORY + 'base_06_02_to_11_28/telegram_archive_11_28/'
    DESIGNATED_DIRECTORY = PARENT_DIRECTORY + 'designated_tgram_chat/'
    JSON_FILE = 'result.json'

    def __init__(self, base_directory=BASE_DIRECTORY, desginated_directory=DESIGNATED_DIRECTORY, json_filename=JSON_FILE):
        self.base_directory = base_directory
        self.designated_directory = desginated_directory
        self.json_file_name = json_filename

        # load some variables via method for easy reloads
        self.messages = []
        self.load_messages()


    # use to load OR reload after changes
    def load_messages(self):
        # get base
        print("\n\nLOADING MESSAGES")
        msgs = []
        with open(self.base_directory + self.json_file_name, 'r') as f:
            ljson = json.load(f)
            msg_hshs = ljson["messages"]
            print(f'Loading base messages: {f.name}')
            for msg in msg_hshs:
                msgs.append(chat_msg.ChatMessage(msg, self.base_directory))
        
        #for tgram directory in designated dir, add to messages 
        pathlist = Path(self.designated_directory).rglob('result.json') 
        for path in pathlist:
            this_dir = str(path.parents[0])
            with open(str(path), 'r') as f:
                tmp_json = json.load(f)
                msg_hshs = tmp_json["messages"]
                if len(msg_hshs) == 0:
                    raise Exception(f'Could not get hashes from {str(path)}')
                print(f'Loading messages from {f.name}')
                for msg in msg_hshs:
                    msgs.append(chat_msg.ChatMessage(msg, self.designated_directory))
        self.messages = chat_collection.ChatMessageCollection(msgs)
        print(f'{len(self.messages)} MESSAGES LOADED\n\n')

    # returns array of urls
    def fetch_uniq_urls(self):
        links = self.messages.having_links().pluck('links')
        ret_arr = []
        for link in links:
            if link.url not in ret_arr:
                ret_arr.append(link.url)
        return ret_arr

