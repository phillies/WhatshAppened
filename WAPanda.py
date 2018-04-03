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
