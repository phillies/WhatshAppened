"""

"""
import datetime, regex

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

    def __init__(self, logfile=None, language='de'):
        self._logfile = logfile
        self.data = {}
        self._language = language
        self._regexp = {
            'language': 'de',
            'timestamp': r'[\u200e][0-3][0-9][.][0-1][0-9][.][0-2][1-9] um [0-2][0-9][:][0-5][0-9]',
            'timestamp length': 18,
            'no colon': r'[^:]*'
        }

    
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
        self._raw = None
        with open(self._logfile, 'r', encoding=encoding) as f:
            self._raw = f.readlines()

    def _merge_multiline_messages(self):
        if self._raw is None:
            raise ValueError('Raw data not loaded')

        self._preproc = []
        i = 0
        while i < len(self._raw):
            msg = self._raw[i]
            while i < (len(self._raw)-1) and regex.match(self._regexp['timestamp'], self._raw[i+1][:self._regexp['timestamp length']]) is None:
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
            data['timestamp'].append(datetime.datetime(2000+int(line[7:9]), int(line[4:6]), int(line[1:3]), int(line[13:15]), int(line[16:18])))
            
            msg = line[21:]
            if not regex.search(r'[^:]*has?t den Betreff ', msg) is None:
                pos = regex.search(r' has?t den Betreff ', msg)
                name = msg[:pos.start()].strip(u'\u200e\u202a\u202c')
                if name == 'Du':
                    name = 'Phil'
                data['who'].append(name)
                data['message'].append(msg)
                data['type'].append('topic')
                
            elif not regex.search(r'[^:]*Die Sicherheitsnummer', msg) is None:
                data['who'].append('System')
                data['message'].append(msg)
                data['type'].append('security')
                
            elif not regex.search(r'[^:]* has?t das Gruppenbild ', msg) is None:
                pos = regex.search(r' has?t das Gruppenbild ', msg)
                name = msg[:pos.start()].strip(u'\u200e\u202a\u202c')
                if name == 'Du':
                    name = 'Phil'
                data['who'].append(name)
                data['message'].append(msg)
                data['type'].append('picture')
                
            elif not regex.search(r'[^:]*has?t.*hinzugefügt', msg) is None:   
                data['who'].append('System')
                data['message'].append(msg)
                data['type'].append('add')      
                
            elif not regex.search(r'[^:]*hat die Gruppe verlassen', msg) is None:   
                data['who'].append('System')
                data['message'].append(msg)
                data['type'].append('quit')  
            
            elif not regex.search(r'[^:]*wurde entfernt', msg) is None:   
                data['who'].append('System')
                data['message'].append(msg)
                data['type'].append('remove')   
            
            elif msg.find(':') >= 0: 
                name, txt = msg.split(':', maxsplit=1)
                data['who'].append(name.strip(u'\u200e\u202a\u202c'))
                data['message'].append(txt)
                data['type'].append('message')      

            else:
                data['who'].append('???')
                data['message'].append(msg)
                data['type'].append('unknown')

            #TODO: refactor end
        self.data = data
        self._preproc = None


    