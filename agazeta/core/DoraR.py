
# coding: utf-8

from json_utils import json_load_byteified, json_loads_byteified, _byteify
from datetime import datetime, timedelta
from .models import apikeys, archive
from threading import Thread
import pandas as pd
import argparse
import urllib
import json
import time

class API_Error(Exception): pass
class UsernameOrToken_Error(API_Error): pass

class AppURLopener(urllib.FancyURLopener):
    version = "App/1.7"

    def prompt_user_passwd(self, host, realm):
        raise UsernameOrToken_Error ('Username or token invalid')

def test_api(username, token):
    urllib._urlopener = AppURLopener()
    ret = False
    f = None
    get = 'https://trackobot.com/profile/history.json?page={page}&username={username}&token={token}'
    try:
        response = urllib.urlopen(get.format(page=1, username=username, token=token))
        resp = response.read()
        data = json_loads_byteified(resp)
        return True if len(data['meta'].keys()) else False

    except UsernameOrToken_Error as e:
        return False

    except Exception as e:
        return None

def no_duplicate(username, token):
    return False if len(apikeys.objects.filter(username = username).filter(token = token)) else True

class DoraR ():
    def __init__(self, verbose=False, limit=0, past_days=7):
        self.limit = limit
        self.verbose = verbose
        self.from_date = datetime.today() - timedelta(days=past_days)
        self.past_days = past_days
        if self.verbose: print 'Starting Dora R.'

        urllib._urlopener = AppURLopener()

    def api_getter (self):
        sqlret = apikeys.objects.all() if not self.limit else apikeys.objects.all()[:self.limit]
        for row in sqlret:
            if self.verbose: print row.id
            yield (row.username, row.token)

    def posix_conversion(self, date = '2016-12-02T02:29:09.000Z'):
        d = datetime.strptime( date, '%Y-%m-%dT%H:%M:%S.000Z')
        return int(time.mktime(d.timetuple()))

    def datetime_conversion(self, date = '2016-12-02T02:29:09.000Z'):
        return datetime.strptime( date, '%Y-%m-%dT%H:%M:%S.000Z')

    def Maexxna(self):
        # from_date = datetime
        from_date = time.mktime(self.from_date.timetuple())
        get = 'https://trackobot.com/profile/history.json?page={page}&username={username}&token={token}'
        for username, token in self.api_getter():
            page = 1
            end = False
            try_and_error = 3
            data_history =[]

            while(True):
                try:
                    response = urllib.urlopen(get.format(page=page,
                                                username=username, token=token))
                    if self.verbose: print "reading page", page
                    try_and_error = 3
                except UsernameOrToken_Error as e:
                    print e
                    break
                except Exception as e:
                    print 'error', e
                    if try_and_error:
                        try_and_error -= 1
                        continue
                    else:
                        break

                resp = response.read()
                data = json_loads_byteified(resp)

                for n in range(len(data['history'])):
                    if self.posix_conversion(data['history'][n]['added']) < from_date:
                        del data['history'][n:len(data['history'])]
                        end = True
                        break

                data_history += data['history']

                # end of the loop
                if data['meta']['total_pages'] <= data['meta']['current_page'] or end or page > ((400*self.past_days)//25):
                    break

                page += 1

            if self.verbose:
                print 'game history', len(data_history)

            yield data_history

    def Starseeker(self):

        def _turns(data):
            a = 0
            for i in range(len(data)):
                a = data[i]['turn'] if data[i]['turn'] > a else a
            return a

        total_entries = 0
        for files in self.Maexxna():

            df = pd.DataFrame(columns=['matchid', 'date_posix', 'date', 'rank', 'hero', 'hero_deck',
                                       'opponent_hero', 'opponent_deck', 'coin', 'turns', 'result',
                                       'cards', 'opponent_cards'
                                      ])
            index = 0

            match = []
            for i in range(len(files)):
                # Only ranked games are going to be stored
                if files[i]['mode'] != 'ranked':
                    continue
                game = files[i]

                my_cards = []
                opponent_cards = []
                for card in game['card_history']:
                    if card['player'] == 'me':
                        my_cards.append(str(card['card']['id'])+":"+str(card['turn']))
                    else:
                        opponent_cards.append(str(card['card']['id'])+":"+str(card['turn']))
                my_cards = ', '.join(my_cards)
                opponent_cards = ', '.join(opponent_cards)

                df.loc[index] = [ int(game['id']), int(self.posix_conversion(game['added'])), self.datetime_conversion(game['added']),
                        None if game['rank'] is None else int(game['rank']) , game['hero'], game['hero_deck'],
                        game['opponent'], game['opponent_deck'], True if game['coin'] else False,
                        _turns(game['card_history']), True if game['result'] == 'win' else False,
                        my_cards, opponent_cards ]

                df = df.fillna(method='ffill')
                df = df.fillna(20)
                index += 1

            match = map(tuple, df.values)
            if self.verbose:
                print 'total of', len(match), 'valid ranked games'

            for entry in match:
                arc = archive.objects.filter(matchid = entry[0])
                if not len(arc):

                    a = archive( matchid = entry[0],date_posix = entry[1],
                    date = entry[2], rank = entry[3], hero = entry[4], hero_deck = entry[5],
                    opponent_hero = entry[6], opponent_deck = entry[7],
                    coin = entry[8], turns = entry[9], result = entry[10],
                    cards = entry[11], opponent_cards = entry[12] )
                    try:
                        a.save()
                    except Exception as e:
                        print entry
                        print "Was not possible to save :'("

                    total_entries += 1
            if self.verbose:
                print 'DB posting complete'

        if self.verbose:
            print 'Finished running DORA R'
        return total_entries

    def run (self):
        if self.verbose: print 'Starting RUN_should be threaded'
        Thread(target=self.Starseeker).start()
        if self.verbose: print 'Running Thread'
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='mine data from trackobot')
    parser.add_argument('-d', '--past_days', type=int, default='2',
            help='how long ago is the last relevant game played by a player')
    args = parser.parse_args()
    print "Running with CRON"
    D = DoraR(past_days=args['past_days'])
    D.run()
