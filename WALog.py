"""

"""
import datetime, regex, random, string, warnings

class WALog:
    """WhatshAppened Logging class
    Reads the .txt file exported from WhatsApp, merges multi-line messages into one message object,
    and splits the messages into timestamp, sender, message body, and message type.

    Message types are:
    message - regular message
    picture - group chat picture was changes
    topic - group chat topic was changed
    add - person was added
    remove - person was removed
    quit - person left
    security - seurity number has changed
    unknown - message that could not be identified
    """

    def __init__(self, logfile=None, parse=False, language='de', exporter_name='Phil'):
        self._logfile = logfile
        self.data = {'timestamp':[], 'who':[], 'message':[], 'type': []}
        self._language = language
        self._regexp = {
            'language': 'de',
            'timestamp': r'[\u200e]?[0-3][0-9][.][0-1][0-9][.][0-2][1-9] um [0-2][0-9][:][0-5][0-9]',
            'datetime format': '%d.%m.%y um %H:%M',
            'no colon': r'[^:]*',
            'topic': r'has?t den Betreff ' ,
            'security': r'Die Sicherheitsnummer',
            'picture': r'has?t das Gruppenbild ',
            'add': r'has?t.*hinzugefügt',
            'quit': r'hat die Gruppe verlassen',
            'remove': r'wurde entfernt',
            'you': 'Du',
            'exporter': exporter_name,
            'stripchars': u'\u200e\u202a\u202c \n',
            'remove message content': [r'<Medien weggelassen>']

        }
        if parse:
            self.parse()

    
    def parse(self, logfile=None, verbose=False, encoding='utf-8'):
        """
        """
        if not logfile is None:
            self._logfile = logfile
        
        if self._logfile is None:
            raise ValueError('Logfile must not be empty')

        self._read_log(encoding=encoding)
        if verbose:
            print('Read', len(self._raw), 'lines from', self._logfile )

        self._merge_multiline_messages()
        if verbose:
            print('Merged into', len(self._preproc), 'messages' )

        self._parse_messages()
        if verbose:
            print('Parsing completed' )

    def _read_log(self, encoding='utf-8'):
        """Reads the content of the log file and stores it as raw data. Uses utf-8 encoding by default.
        """
        self._raw = None
        with open(self._logfile, 'r', encoding=encoding) as f:
            self._raw = f.readlines()

    def _merge_multiline_messages(self):
        """Merges multi-line messages into one string/array entry.

        Checks for each line that starts with a timestamp if the following line starts with a timestamp, too. If not it adds the line to the current one
        and repeats until a timestamp is found ot the eand of the lines is reached.
        """
        if self._raw is None:
            raise ValueError('Raw data not loaded')

        self._preproc = []
        i = 0
        while i < len(self._raw):
            msg = self._raw[i]
            while i < (len(self._raw)-1) and regex.search(self._regexp['timestamp'], self._raw[i+1]) is None:
                i += 1
                msg += self._raw[i]
            self._preproc.append(msg)
            i += 1
        self._raw = None

    def _parse_messages(self):
        if self._preproc is None:
            raise ValueError('Data not loaded')

        data = {'timestamp':[], 'who':[], 'message':[], 'type': []}
        for i in range(len(self._preproc)):
            line = self._preproc[i]

            #TODO: refactor start
            match = regex.search(self._regexp['timestamp'], line)
            if match is None:
                raise ValueError('Cannot find timestamp in ' + line)
            
            #For the conversion to datetime the leading unicode char for RTL must be stripped
            timestamp = datetime.datetime.strptime(line[:match.end()].strip(self._regexp['stripchars']), self._regexp['datetime format'])
            data['timestamp'].append(timestamp)
            
            msg = line[match.end():]
            if not regex.search(self._regexp['no colon']+self._regexp['topic'], msg) is None:
                pos = regex.search(self._regexp['topic'], msg)
                name = msg[:pos.start()].strip(self._regexp['stripchars'])
                if name == self._regexp['you']:
                    name = self._regexp['exporter']
                data['who'].append(name.strip(self._regexp['stripchars']))
                data['message'].append(msg)
                data['type'].append('topic')
                
            elif not regex.search(self._regexp['no colon']+self._regexp['security'], msg) is None:
                data['who'].append('System')
                data['message'].append(msg)
                data['type'].append('security')
                
            elif not regex.search(self._regexp['no colon']+self._regexp['picture'], msg) is None:
                pos = regex.search(self._regexp['picture'], msg)
                name = msg[:pos.start()].strip(self._regexp['stripchars'])
                if name == self._regexp['you']:
                    name = self._regexp['exporter']
                data['who'].append(name.strip(self._regexp['stripchars']))
                data['message'].append(msg)
                data['type'].append('picture')
                
            elif not regex.search(self._regexp['no colon']+self._regexp['add'], msg) is None:   
                data['who'].append('System')
                data['message'].append(msg)
                data['type'].append('add')      
                
            elif not regex.search(self._regexp['no colon']+self._regexp['quit'], msg) is None:   
                data['who'].append('System')
                data['message'].append(msg)
                data['type'].append('quit')  
            
            elif not regex.search(self._regexp['no colon']+self._regexp['remove'], msg) is None:   
                data['who'].append('System')
                data['message'].append(msg)
                data['type'].append('remove')   
            
            elif msg.find(':') >= 0: 
                name, txt = msg.split(':', maxsplit=1)
                data['who'].append(name.strip(self._regexp['stripchars']))
                data['message'].append(txt.strip(self._regexp['stripchars']))
                data['type'].append('message')      

            else:
                data['who'].append('???')
                data['message'].append(msg)
                data['type'].append('unknown')

            #TODO: refactor end
        self.data = data
        self._preproc = None


    def rename_sender(self, from_name, to_name, verbose=False):
        """Rename a person in the message log, e.g. if someone changed his/her
        number and you need to merge both numbers to one name.
        """
        num_occurences = self.data['who'].count(from_name)
        
        if verbose:
            print('Number of matches for', from_name, ':', num_occurences)
        
        index = 0
        for _ in range(num_occurences): 
            index = self.data['who'].index(from_name, index)
            self.data['who'][index] = to_name
            index += 1

    def anonymize(self, last_peek=False):
        """Anonymizes the data set by replacing all sender names by random names
        and searches for sender names in message content.
        Attention: this is not a data security sufficient anonymization. If the
        sender is named "John Doe" it will not replace occurences like "Mr. Doe",
        "John", or nicknames like "Johnny" or abbreviations like "JD".

        last_peek : prints which name is replaced by which random string
        """
        sender = set(self.data['who'])
        new_sender = []
        for _, from_name in enumerate(sender):
            to_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(10))
            while to_name in new_sender:
                to_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(10))
            if last_peek:
                print(from_name, to_name)
            self.rename_sender(from_name, to_name)
    
    def remove_unwanted_content(self, drop_matching_mesages=False):
        """ Removes text as defined in _regexp['remove message content'], optionally
        drops message completely.
        """

        if self.data is None:
            raise ValueError('data cannot be None, please parse logfile first.')

        for regexpr in self._regexp['remove message content']:
            for index, item in enumerate(self.data['message']):
                match = regex.search(regexpr, item)
                if not match is None:
                    if drop_matching_mesages:
                        self._drop_message(index)
                    else:
                        self.data['message'][index] = item[:match.start()] + item[match.end():]
        
    
    def _drop_message(self, index):
        """Deletes a message from the log
        """
        
        if index < len(self.data['who']):
            self.data['who'].pop(index)
            self.data['timestamp'].pop(index)
            self.data['message'].pop(index)
            self.data['type'].pop(index)
        else:
            warnings.warn('Tried to delete a message with index out of bounds.')


    