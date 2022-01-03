import webbrowser
import hashlib


class ChatFile():

    def __init__(self, filepath):
        self.filepath = filepath.replace(" ","\\ ")
    
    def hashssum(self):
        hashlib.md5(self.filepath).hexdigest(9)

    def open(self):
        webbrowser.open(self.filepath)

    def __eq__(self, other):
        if self.filepath == other.filepath:
            return True
        if self.hashsum == other.hashsum:
            return True
        return False
