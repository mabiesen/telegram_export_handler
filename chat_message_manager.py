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

    # defaulting to parent directory
    DEFAULT_OUTPUT_FILEPATH = PARENT_DIRECTORY + JSON_FILE


    def __init__(self, base_directory=BASE_DIRECTORY, desginated_directory=DESIGNATED_DIRECTORY, json_filename=JSON_FILE):
        self.base_directory = base_directory
        self.designated_directory = desginated_directory
        self.json_file_name = json_filename

        # load some variables via method for easy reloads
        self.messages = []

    # At times we may want to write filtered files out
    # To that end, allowing the loading of any collection
    def load_messages_from_collection(self, collection):
        self.messages = collection

    def load_messages_from_file(self, directory, filename):
        msgs = []
        with open(directory + filename, 'r') as f:
            ljson = json.load(f)
            msg_hshs = ljson["messages"]
            print(f'Loading base messages: {f.name}')
            for msg in msg_hshs:
                msgs.append(chat_msg.ChatMessage(msg, directory))
        self.messages = chat_collection.ChatMessageCollection(msgs)
        return self.messages

    def load_messages_from_directory(self, directory, filename):
        msgs = []
        pathlist = Path(directory).rglob(filename)
        for path in pathlist:
            this_dir = str(path.parents[0])
            with open(str(path), 'r') as f:
                tmp_json = json.load(f)
                msg_hshs = tmp_json["messages"]
                if len(msg_hshs) == 0:
                    raise Exception(f'Could not get hashes from {str(path)}')
                for msg in msg_hshs:
                    msgs.append(chat_msg.ChatMessage(msg, self.designated_directory))
        self.messages = chat_collection.ChatMessageCollection(msgs)
        return self.messages

    # use to load OR reload after changes
    def load_messages_from_base_and_designated(self):
        msgs = self.load_messages_from_file(self.base_directory, self.json_file_name)
        msgs2 = self.load_messages_from_directory(self.designated_directory, self.json_file_name)
        for msg in msgs2:
            msgs.append(msg)
        self.messages = msgs


    # Will NOT copy files, that would be ridiculously expensive
    # We are merely creating a new results file
    # We can then safely whiddle down the results file for dupes/etc
    def write_messages(self, output_filepath=DEFAULT_OUTPUT_FILEPATH):
        hash_array = []
        for msg in self.messages:
            hash_array.append(msg.msg_hsh)
        json_hsh = {"messages": hash_array}
        with open(output_filepath, 'w') as outfile:
            json.dump(json_hsh, outfile, indent=4)
            print(f'Messages have ben written to {outfile.name}')


    # returns array of urls
    def fetch_uniq_urls(self):
        links = self.messages.having_links().pluck('links')
        ret_arr = []
        for link in links:
            if link.url not in ret_arr:
                ret_arr.append(link.url)
        return ret_arr
