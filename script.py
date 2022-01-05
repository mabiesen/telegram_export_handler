from chat_message_manager import ChatMessageManager

import code
import sys

# Purpose of this script is to easily invoke ChatMessageManager on import
# And eventually, easily run reports/queries
# Speeds up python console testing; additionally, we almost always will use default file/directory values

CMM = ChatMessageManager()
CMM.load_messages_from_base_and_designated()

print("Chat Message Manager Loaded To Global Variable 'CMM'\n\n")
print("You will primarily be interacting with the ChatMessageManager's obtained messages - this is a ChatMessageCollection object.  This class is 'list-y', allowing one to access contained messages as-if it were a list.  See chat_message_collection interactor for further details\n\n")

if __name__ == "__main__":
    args = sys.argv
    if args[1] == 'report':
        CMM.run_report(args[2])
    elif args[1] == 'console':
        code.interact(local=dict(globals(), **locals()))
