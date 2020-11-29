import gspread
import json

import backend.database as database
from backend import document
from backend import datafolder

winelo = {}
losselo = {}
with open(datafolder / 'winelo.json') as f:
  winelo = json.load(f)
with open(datafolder / 'losselo.json') as f:
  losselo = json.load(f)

#Determines how much ELO should change based on rank
#Input: 'rank' isCrewWin , isImp, isPlace
#Output: elochange
def elo_change(rank, isCrewWin, isImp, isPlace):
    elochange = 0
    if isCrewWin:
        elochange = winelo[rank]
        if isImp:
            elochange *= 2
    else:
        elochange = losselo[rank]
        if not isImp:
            elochange *= 2
    if isPlace:
        elochange *= 2
    return elochange

#Adds a loss to the player
#Input: ['row', 'id', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%', 'crewwl%', 'impwl%'], isImp
#Output: ['row', 'id', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%', 'crewwl%', 'impwl%']
def add_loss(entry, isImp):
    if isImp:
        entry[8] = str(int(entry[8]) + 1)
    else:
        entry[9] = str(int(entry[9]) + 1)
    entry[5] = str(int(entry[5]) + 1)
    return entry

#Adds a win to the player
#Input: ['row', 'id', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%', 'crewwl%', 'impwl%'], isImp
#Output: ['row', 'id', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%', 'crewwl%', 'impwl%']
def add_win(entry, isImp):
    if isImp:
        entry[6] = str(int(entry[6]) + 1)
    else:
        entry[7] = str(int(entry[7]) + 1)
    return add_loss(entry, isImp)

#Adjusts elo based on win, imp, and rank
#Input: ['row', 'id', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%', 'crewwl%', 'impwl%'], isCrewWin, isImp
#Output: ['row', 'id', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%', 'crewwl%', 'impwl%']
def adjust_elo(entry, isCrewWin, isImp):
    elochange = elo_change(entry[3], isCrewWin, isImp, int(entry[5]) <= 5)
    newelo = int(entry[4]) + elochange
    entry[4] = str(newelo if newelo > 0 else 0)
    return entry

#The base entry for a new player
baseentry = ['', '', 'Bronze 3', '200', '0', '0', '0', '0', '0']

#A function to add a game to the database
#Input: [names of players] [names of imps] isCrewWin
#Outputs: succeeds
def add_game(ids, names, imps, isCrewWin):
    entries = database.get_rows(ids)
    entrynames = [names[ids.index(entry[0])] for num, entry in enumerate(entries) if entry[0] in ids]
    entryids = [entry[0] for entry in entries]
    newentrynames = [name for name in names if not name in entrynames]
    newentryids = [id for id in ids if not id in entryids]
    newentries = [baseentry.copy() for name in newentryids]
    if newentries:
        for num, entry in enumerate(newentries):
            entry[0] = newentryids[num]
            entry[1] = newentrynames[num]
            if entry[0] in imps:
                if not isCrewWin:
                    add_win(entry, True)
                    adjust_elo(entry, True, True)
                else:
                    add_loss(entry, True)
                    adjust_elo(entry, False, True)
            else:
                if not isCrewWin:
                    add_loss(entry, False)
                    adjust_elo(entry, False, False)
                else:
                    add_win(entry, False)
                    adjust_elo(entry, True, False)
    for num, entry in enumerate(entries):
        entry[1] = entrynames[num]
        if entry[0] in imps:
            if not isCrewWin:
                add_win(entry, True)
                adjust_elo(entry, True, True)
            else:
                add_loss(entry, True)
                adjust_elo(entry, False, True)
        else:
            if not isCrewWin:
                add_loss(entry, False)
                adjust_elo(entry, False, False)
            else:
                add_win(entry, False)
                adjust_elo(entry, True, False)
    database.add_entries(newentries)
    database.update_entries(entries)
    return True

#Adds an elo loss to a given player equal to that of a crew loss
#Inputs: 'id'
#Outputs: succeeds
def elo_loss(id):
    entries = database.get_rows([id])
    entry = entries[0]
    if entry:
        elochange = elo_change(entry[2], False, True, False)
        newelo = int(entry[3]) + elochange
        entry[3] = str(newelo if newelo > 0 else 0)
        database.update_entries([entry])
    return True

#Adds an elo gain to a player equal to a crew win
#Input: 'id'
#Output: succeeds
def elo_gain(id):
    entries = database.get_rows([id])
    entry = entries[0]
    if entry:
        elochange = elo_change(entry[2], True, False, False)
        newelo = int(entry[3]) + elochange
        entry[3] = str(newelo if newelo > 0 else 0)
        database.update_entries([entry])
    return True


def get_elo(id):
    entries = database.get_rows([str(id)])
    if entries:
        entry = entries[0]
        if entry:
            return int(entry[3])
    return -1


#DEPRECEATED!!
def add_ids(players):
"""     gc = gspread.service_account(filename='client_secret.json')
    names = [player[0] for player in players]
    entries = database.get_rows_by_name(names, gc)
    new_entries = []
    for entry in entries:
        info = list(filter(lambda x: entry[2] in x, players))
        player = info[0]
        new_entry = entry.copy();
        new_entry[1] = str(player[1])
        new_entries.append(new_entry)
    database.update_entries(new_entries, gc) """
    return True

    
