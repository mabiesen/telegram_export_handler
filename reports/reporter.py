


class Reporter:

    def __init__(self, chat_message_manager, should_write=False, outfile = None):
        self.cmm = chat_message_manager
        self.should_write = should_write
        if outfile:
            self.outfile = outfile
        else:
            self.outfile = self.cmm.DEFAULT_WRITE_PATH

    def call(self, report_name):
        func = getattr(self, report_name)
        data = func()
        if self.should_write: 
            self.chat_message_manager.write_messages(self.outfile) 

    def heart_conditions(self):
        keywords = ['myocarditis','pericardiitis','chest pain', 'heart', 'acs']
        return self.cmm.messages.having_text_like(keywords).uniq_on('text', 'text')

    def studies(self):
        keywords = ['study', 'studies', 'nih.gov', 'medrx']
