class Reporter:

    def __init__(self, msg_collection):
        self.collection = msg_collection

    def heart_conditions(self):
        keywords = ['myocarditis','pericardiitis','chest pain', 'heart', 'acs']
        return self.cmm.messages.having_text_like(keywords).uniq_on('text', 'text')

    def studies(self):
        keywords = ['study', 'studies', 'nih.gov', 'medrx']
