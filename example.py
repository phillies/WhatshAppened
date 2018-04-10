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
    
    log.anonymize(last_peek=True)

    print('Loading stats')
    stat = WAStats(log)
    stat.show_stats()

    print('Loading pandas')
    pan = WAPanda(log)
    pan.show_stats()

    print('Loading emojis\n')
    pan.emoji_stats()
    pan.top_emojis(number_top=10, compact=True)