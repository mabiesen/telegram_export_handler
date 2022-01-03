from models.chat_message_components.parents import chatfile


class Video(chatfile.ChatFile):

    def __init__(self, filepath, data_directory):
        super().__init__(data_directory + filepath)

    def as_html(self):
        return '<video controls><source src="#{self.filepath}" type="video/mp4"></video>'
