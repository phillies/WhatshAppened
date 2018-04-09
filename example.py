import sys
from WALog import WALog
from WAStats import WAStats
from WAPanda import WAPanda

if __name__ == '__main__':
    if len(sys.argv) == 1:
        log = WALog('example.txt')
    else:
        log = WALog(sys.argv[1])
    log.parse(verbose=True)
    
    stat = WAStats(log)
    stat.show_stats()

    pan = WAPanda(log)
    pan.show_stats()
        #print(pan._df)
        #print(log.data)