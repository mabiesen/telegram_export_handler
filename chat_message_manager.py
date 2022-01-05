from models import chat_message as chat_msg
from interactors import reporter
from interactors import chat_message_collection as chat_collection
from pathlib import Path
import json

with open('config/config.json', 'rb') as f:
    CONFIG=json.load(f)

DEFAULT_BASE = CONFIG["base_directory"]
DEFAULT_DES = CONFIG["designated_directory"]
DEFAULT_READ_FILE = CONFIG["json_file"]
DEFAULT_WRITE_PATH = CONFIG["output_filepath"]
DEFAULT_STATIC_DIR = CONFIG["static_directory"]

class ChatMessageManager:
    # THE THEORY
    # base directory represents a time where I saved all messages in one location
    # I eventually realized this was not scalable over time, I started to save smaller 'time-designated' chats 
    # A comprehensive view of saved messages requires base + designated

    def __init__(self, base_directory=DEFAULT_BASE, desginated_directory=DEFAULT_DES, json_filename=DEFAULT_READ_FILE, static_dir=DEFAULT_STATIC_DIR):
        self.base_directory = base_directory
        self.designated_directory = desginated_directory
        self.json_file_name = json_filename

        self.static_dir = static_dir #this is for serving files in flask

        # load some variables via method for easy reloads
        self.messages = []

    # At times we may want to write filtered files out
    # Or run reports on a subset of data
    # To that end, allowing the loading of any collection
    # but this should be viewed as advanced usage
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
    # defaulting msgs to none is dumb, but I want optional input
    def write_messages(self, msgs=None, output_filepath=DEFAULT_WRITE_PATH):
        if not msgs:
            msgs = self.messages
        hash_array = []
        for msg in msgs:
            hash_array.append(msg.msg_hsh)
        json_hsh = {"messages": hash_array}
        with open(output_filepath, 'w') as outfile:
            json.dump(json_hsh, outfile, indent=4)
            print(f'Messages have ben written to {outfile.name}')

    # Runs reports using the reporter interactor
    # reporter interactor accepts a ChatMessageCollection
    # NOTE: this method must remain agnostic as regards custom-objects/lists/etc
    # -- a report should be free to report in any format.
    def run_report(self, report_name, write=False):
        rep = reporter(self.messages)
        func = getattr(rep, report_name)
        data = func()
        if write:
            print(f'Writing report {report_name} to file')
            print('File will be written as json, with "messages" as the top key')
            self.write_messages(data)
        return data
