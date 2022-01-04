# File to launch EITHER ChatMessageManager class only OR run flask with the manager
from chat_message_manager import ChatMessageManager
import sys

CMM = ChatMessageManager()
CMM.load_messages_from_base_and_designated()
print("Chat Message Manager Loaded To Global Variable 'CMM'")


# when run directly we serve flask 
if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'serve':
        pass
        # import flask_app

