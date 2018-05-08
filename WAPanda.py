import pandas as pd
import numpy as np
from WALog import WALog
from WAStats import WAStats

class WAPanda(WAStats):
    """WhatshAppened pandas class
    Data analysis class for WhatshAppened
    """

    def __init__(self, log):
        WAStats.__init__(self, log)
        self._df = pd.DataFrame(data=log.data)
        self._emojis = None

    def show_stats(self):
        if self._df is None:
            print('No DataFrame, nothing to show.')
            return
        
        is_message = self._df.type == 'message'
        print(self._df[is_message].who.value_counts())

    def _get_occurences(self, emojis, messages):
        occurences = np.zeros(len(emojis), dtype=np.int64)
        for i in emojis.index:
            index = emojis.index[i]
            try:
                occurences[i] = messages.message.str.count(emojis.emojis[index]).sum()
            except:
                occurences[i] = 0

        return pd.Series(occurences, index=emojis.index)

    def emoji_stats(self, emoji_file='emojis.txt'):
        if emoji_file is None:
            raise ValueError('emoji file name cannot be None')
        emojis = []
        with open(emoji_file, 'r', encoding='utf-8') as fin:
            emoji = fin.read(1)
            while emoji:
                emojis.append(emoji)
                emoji = fin.read(1)
        
        self._emojis = pd.DataFrame({'emojis': emojis})
        
        is_message = self._df.type == 'message'
        messages = self._df[is_message]        
        senders = messages.who.unique()

        for name in senders:
            self._emojis[name] = self._get_occurences( self._emojis, messages[messages.who == name])
        self._emojis.index = self._emojis.emojis

    def top_emojis( self, number_top=3, compact=False ):
        if self._emojis is None:
            self.emoji_stats()
        
        is_message = self._df.type == 'message'
        messages = self._df[is_message]
        senders = messages.who.unique()

        self._emojis_pretty_print( senders, number_top, compact )


    def _emojis_pretty_print(self, senders, number_top = 3, compact=False ):
        name_width = max([len(s) for s in senders])
        for sender in senders:
            sorted_emojis = self._emojis[sender].sort_values(ascending=False)
            self._emoji_pretty_print( sorted_emojis, sender, number_top, compact, name_width )

    def _emoji_pretty_print(self, emojis, sender, number_top = 3, compact=False, name_width=None ):
        if name_width is None:
            name_width = len(sender)
        if compact:
            print(('{:'+str(name_width)+'}: {}').format(sender, ' '.join(emojis.index[:min(number_top, (emojis>0).sum())])))
        else:
            print(sender)
            print('Total emojis:', emojis.sum())
            print('Total distinct emojis:', (emojis>0).sum())
            emojis /= float(emojis.sum())
            for i in range(min(number_top, (emojis>0).sum())):
                print('#{}: {}\t{:.2%}'.format(i+1, emojis.index[i], emojis[emojis.index[i]]))
            print(30*'-'+'\n')         
    
    def add_message_length(self):
        if self._df is None:
            raise ValueError('DataFrame cannot be None')
        
        self._df['message length'] = self._df.message.str.len()
    
    def add_word_count(self):
        if self._df is None:
            raise ValueError('DataFrame cannot be None')

        # This is a first approximation that only counts how many strings consisting of [a-zA-Z0-9] are included. Needs to be revamped.
        self._df['word count'] = self._df.message.str.count(r'\w+')

    def resample_messages(self, frequency='D'):
        if self._df is None:
            raise ValueError('DataFrame cannot be None')

        is_message = self._df.type == 'message'
        messages = self._df[is_message]
        spiketrain = messages.groupby('timestamp').aggregate('count').who.resample(frequency).sum()
        return spiketrain

