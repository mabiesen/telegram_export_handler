from models.chat_message_components.parents import chatfile


class PDF(chatfile.ChatFile):
    
    def __init__(self, filepath, data_directory):
        super().__init__(data_directory + filepath)

    def as_html(self):
        return '<a href="#{self.filepath}">#{self.filepath}</a>'