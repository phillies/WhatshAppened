import sys
from WALog import WALog
from WAStats import WAStats

if __name__ == '__main__':
    if len(sys.argv) == 1:
        log = WALog('example.txt')
        log.parse(verbose=True)
        
        stat = WAStats(log)
        stat.show_stats()