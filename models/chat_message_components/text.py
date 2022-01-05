import webbrowser

class Text(object):

    def __init__(self, text_data):
        self.text_data = text_data

    # telegram intersperses text and non text items.
    # non-text items include font-changed-strings and links
    # these come in as hashes/dicts
    # sometimes text is a string, sometimes an array
    # convert all to array
    def raw_text_array(self):
        if isinstance(self.text_data, str):
            if self.text_data == '' or self.text_data == None:
                return []
            return [self.text_data]
        else:
            return self.text_data

    # this is the chat text AS SEEN (without font)
    # no urls: we strip urls from the text array and only show text 
    # only time youll see a url is if the original message didnt mask the url
    def text(self):
        ret_arr = []
        for item in self.raw_text_array():
            if isinstance(item, str):
                ret_arr.append(item)
            if isinstance(item, dict):
                ret_arr.append(item["text"])
        return ' '.join(ret_arr)

    def open(self):
        print(self.raw_text_array)
