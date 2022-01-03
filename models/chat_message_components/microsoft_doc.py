from models.chat_message_components.parents import chatfile


class MicrosoftDoc(chatfile.ChatFile):
    
    def __init__(self, filepath, data_directory):
        super().__init__(data_directory + filepath)

    def as_html(self):
        return "<p>Not yet implemented</p>"
