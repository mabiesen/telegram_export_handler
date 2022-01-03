from models.chat_message_components.parents import chatfile


class ZipFile(chatfile.ChatFile):
    
    def __init__(self, filepath, data_directory):
        super().__init__(data_directory + filepath)

