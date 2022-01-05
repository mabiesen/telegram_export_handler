import webbrowser
from PIL import Image as PILImage
import imagehash
from models.chat_message_components.parents import chatfile



class Thumbnail(chatfile.ChatFile):

    def __init__(self, filepath, data_directory):
        super().__init__(data_directory + filepath)

    def hashsum(self):
        return imagehash.average_hash(PILImage.open(self.filepath))

    def __eq__(self, other):
        if self.filepath == other.filepath:
            return True
        if self.hashsum() == other.hashsum():
            return True
        return False
