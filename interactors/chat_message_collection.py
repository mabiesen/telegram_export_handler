
# Holds array of messages, provides methods to filter/sort
class ChatMessageCollection:

    def __init__(self, chat_messages):
        # all collections sort messages on date
        self.chat_messages = chat_messages
        self.chat_messages.sort()

    # for accessing messages via index
    # returns message or list of messages
    def __getitem__(self, key):
        return self.chat_messages[key]

    def __len__(self):
        return len(self.chat_messages)

    def append(self, msg):
        self.chat_messages.append(msg)
        return self

    def having_image(self):
        ret_arr = []
        for msg in self.chat_messages:
            if msg.image():
                ret_arr.append(msg)
        return ChatMessageCollection(ret_arr)

    def having_thumbnail(self):
        ret_arr = []
        for msg in self.chat_messages:
            if msg.thumbnail():
                ret_arr.append(msg)
        return ChatMessageCollection(ret_arr)

    def having_video(self):
        ret_arr = []
        for msg in self.chat_messages:
            if msg.video():
                ret_arr.append(msg)
        return ChatMessageCollection(ret_arr)

    def having_pdf(self):
        ret_arr = []
        for msg in self.chat_messages:
            if msg.pdf():
                ret_arr.append(msg)
        return ChatMessageCollection(ret_arr)

    def having_files(self):
        ret_arr = []
        for msg in self.chat_messages:
            if any(value for value in msg.files().values()):
                ret_arr.append(msg)
        return ChatMessageCollection(ret_arr)

    # these are files that were not identified as pdf/video/thumbnail/image
    # presence indicated the need for additional chat message components
    # or an update to our file identification methodology in the chat message model
    def having_unidentified_files(self):
        ret_arr = []
        for msg in self.having_files():
            if "unidentified_file_path" in msg.files().keys():
                ret_arr.append(msg)
        return ChatMessageCollection(ret_arr)

    def having_links(self):
        ret_arr = []
        for msg in self.chat_messages:
            if msg.links() != []:
                ret_arr.append(msg)
        return ChatMessageCollection(ret_arr)

    # finds messages containing text
    # TODO: allow regex
    def having_links_like(self, txt):
        ret_arr = []
        for msg in self.having_links():
            has_link = False
            for link in msg.links():
                if txt in msg.url:
                    has_link = True
            if has_link:
                ret_arr.append(msg)
        return ChatMessageCollection(ret_arr)
                    
    def having_text(self):
        ret_arr = []
        for msg in self.chat_messages:
            if msg.text():
                ret_arr.append(msg)
        return ChatMessageCollection(ret_arr)

    # finds messages containing text
    # TODO: allow regex
    def having_text_like(self, text):
        ret_msgs = []
        for msg in self.having_text():
            if text in msg.text().text():
                ret_msgs.append(msg)
        return ChatMessageCollection(ret_msgs)

    # filter for uniq values on messages
    # method2 is used to access message components
    # none values are NOT included
    def uniq_on(self, method, method_2=False):
        msg_val_arr = [] 
        msgs_arr = []
        for msg in self.chat_messages:
            func = getattr(msg, method)
            msg_val = func()
            if method_2 and msg_val:
                func = getattr(msg, method_2)
                msg_val = func()
            if msg_val in msg_val_arr:
                pass
            else:
                msgs_arr.append(msg)
                msg_val_arr.append(msg_val)
        return ChatMessageCollection(msgs_arr)


    # get specific objects/values from collection
    # the return is an array NOT a collection
    # none values ARE included
    def pluck(self, method, method_2=False):
        msg_val_arr = []
        for msg in self.chat_messages:
            func = getattr(msg, method)
            msg_val = func()
            if method_2:
                func = getattr(msg, method_2)
                msg_val = func()
            if isinstance(msg_val, list):
                for item in msg_val:
                    msg_val_arr.append(item)
            else:
                msg_val_arr.append(msg_val)

        return msg_val_arr
        

    # returns a hash with arbitrary ids, comp val and msgs
    # OR returns an array of collections
    # grouping can be refined via the having_count method
    # method2 is used to access message components
    # none values are NOT included
    def group_by(self, method, method_2=False, exclude_nones=False, having_min_count=False, as_array = False):
        msgs_hsh = {}
        ctr = 0
        for msg in self.chat_messages:
            func = getattr(msg, method)
            msg_val = func()
            if method_2 and msg_val:
                func = getattr(msg, method_2)
                msg_val = func()
            hsh_key = self.find_msg_key_from_hsh(msgs_hsh, "group_by_val", msg_val)
            # exclude nones if we should exclude
            if (not msg_val) and exclude_nones:
                pass
            elif hsh_key != None:
                msgs_hsh[hsh_key]['msgs'].append(msg)
            else:
                msgs_hsh[str(ctr)] = {}
                msgs_hsh[str(ctr)]['group_by_val'] = msg_val
                msgs_hsh[str(ctr)]['msgs'] = ChatMessageCollection([msg])
                ctr = ctr + 1

        final_hsh = msgs_hsh
        # filtering for groups having count
        if having_min_count:
            total_dup_count = 0
            final_hsh = {}
            for k,v in msgs_hsh.items():
                if len(v['msgs']) > having_min_count:
                    final_hsh[k] = v
                    total_dup_count += len(v['msgs'])
            print(str(len(final_hsh)) + " duplicated found")
            print("across a total of " + str(total_dup_count) + " chats")

        # returning array or hash as requested
        if as_array:
            ret_arr = []
            for k,v in final_hsh.items():
                ret_arr.append(v['msgs'])
            return ret_arr
        else:
            return final_hsh

    # private method for group by
    def find_msg_key_from_hsh(self, hsh, field, val):
        for k,v in hsh.items():
            if v[field] == val:
                return k
        return None

