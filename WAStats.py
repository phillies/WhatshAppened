"""
"""

class WAStats:
    """WhatshAppened Statistics class
    Takes a logging class object and analyzes the contained messages.
    Very simple tool to take a first look at the data without having to install
    additional packages. For versatile, fancy analytics use WAPanda.
    """

    def __init__(self, log):
        self._log = log
        
    def show_stats(self):
        if self._log is None:
            print('No log, nothing to show.')
            return
        
        print('Participants:')
        print(set(self._log.data['who']))
        print('Message types:')
        print(set(self._log.data['type']))
