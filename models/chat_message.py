from datetime import datetime
from models.chat_message_components import image
from models.chat_message_components import video
from models.chat_message_components import pdf
from models.chat_message_components import thumbnail
from models.chat_message_components import zip_file
from models.chat_message_components import microsoft_doc
from models.chat_message_components import link
from models.chat_message_components import text



class ChatMessage(object):

    def __init__(self, msg_hsh, data_directory):
        self.msg_hsh = msg_hsh
        self.data_directory = data_directory

    # allow messages to be sorted on date
    def __lt__(self, other):
        return self.date() < other.date()

    def id(self):
        return self.msg_hsh["id"]

    def date(self):
        dt = self.msg_hsh["date"]
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S") 

    def links(self):
        ret_arr = []
        if isinstance(self.msg_hsh["text"], list):
            for item in self.msg_hsh["text"]:
                if isinstance(item, dict):
                    if item["type"] == "link":
                        ret_arr.append(link.Link(item["text"]))
                    if item["type"] == "text_link":
                        ret_arr.append(link.Link(item["href"]))
        return ret_arr

    def video(self):
        if ("media_type" in self.msg_hsh.keys()) and self.msg_hsh["media_type"] == 'video_file':
            return video.Video(self.msg_hsh["file"], self.data_directory)
        if "file" in self.msg_hsh.keys() and self.msg_hsh["file"].split('.')[-1] in ['mp4','mp3','mov']:
            return video.Video(self.msg_hsh["file"], self.data_directory)

    def pdf(self):
        if ("file" in self.msg_hsh.keys()) and (self.msg_hsh["mime_type"] == "application/pdf"):
            return pdf.PDF(self.msg_hsh["file"], self.data_directory)

    def thumbnail(self):
        if ("thumbnail" in self.msg_hsh.keys()) and self.msg_hsh["thumbnail"]:
            return thumbnail.Thumbnail(self.msg_hsh["thumbnail"], self.data_directory)

    def image(self):
        if ("photo" in self.msg_hsh.keys()) and self.msg_hsh["photo"]:
            return image.Image(self.msg_hsh["photo"], self.data_directory)

    def zipfile(self):
        if "file" in self.msg_hsh.keys() and self.msg_hsh["file"].split('.')[-1] == 'zip':
            return zip_file.ZipFile(self.msg_hsh["file"], self.data_directory)

    def microsoft_doc(self):
        if "file" in self.msg_hsh.keys() and self.msg_hsh["file"].split('.')[-1] in ['doc','docx']:
            return microsoft_doc.MicrosoftDoc(self.msg_hsh["file"], self.data_directory)


    def files(self):
        ret_hash = {'image': self.image(), 'thumbnail': self.thumbnail(), 'pdf': self.pdf(), 'video': self.video(), 'zipfile': self.zipfile(), 'microsoft_doc': self.microsoft_doc()}
        if all(not value for value in ret_hash.values()) and "file" in self.msg_hsh.keys() and self.msg_hsh["file"]:
            ret_hash["unidentified_file_path"] = self.msg_hsh["file"]
        return ret_hash

    def text(self):
        if self.msg_hsh["text"] == '' or self.msg_hsh["text"] == None:
            return None
        else:
            return text.Text(self.msg_hsh["text"])

    # equality of messages is defined by same text + same file name or hashes
    def __eq__(self, other):
        if other.text.text() != self.text.text():
            return False

        for k,v in self.files():
            if other.files()[k].hashsum() != v.hashsum(): 
                return False

        return True
