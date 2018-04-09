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

    def show_stats(self):
        if self._df is None:
            print('No DataFrame, nothing to show.')
            return
        
        is_message = self._df['type'] == 'message'
        print(self._df[is_message]['who'].value_counts())