import gspread
import json
import backend.database as database
from backend import data_folder

winelo = {}
losselo = {}
with open(data_folder / 'winelo.json') as f:
  winelo = json.load(f)
with open(data_folder / 'losselo.json') as f:
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
#Input: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%'], isImp
#Output: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def add_loss(entry, isImp):
    if isImp:
        entry[7] = str(int(entry[7]) + 1)
    else:
        entry[8] = str(int(entry[8]) + 1)
    entry[4] = str(int(entry[4]) + 1)
    return entry

#Adds a win to the player
#Input: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%'], isImp
#Output: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def add_win(entry, isImp):
    if isImp:
        entry[5] = str(int(entry[5]) + 1)
    else:
        entry[6] = str(int(entry[6]) + 1)
    return add_loss(entry, isImp)

#Adjusts elo based on win, imp, and rank
#Input: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%'], isCrewWin, isImp
#Output: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def adjust_elo(entry, isCrewWin, isImp):
    elochange = elo_change(entry[2], isCrewWin, isImp, int(entry[4]) <= 5)
    newelo = int(entry[3]) + elochange
    entry[3] = str(newelo if newelo > 0 else 0)
    return entry

#The base entry for a new player
baseentry = ['0', '', 'Silver 1', '300', '0', '0', '0', '0', '0', '0']

#A function to add a game to the database
#Input: [names of players] [names of imps] isCrewWin
#Outputs: succeeds
def add_game(names, imps, isCrewWin):
    gc = gspread.service_account(filename='client_secret.json')
    entries = database.get_rows(names, gc)
    entrynames = [entry[1] for entry in entries]
    newentrynames = []
    if not entrynames:
        newentrynames = names.copy()
    else:
        newentrynames = [name for name in names if not name in entrynames]
    newentries = [baseentry.copy() for name in newentrynames]
    if newentrynames:
        for num, name in enumerate(newentrynames):
            newentries[num][1] = name
        for entry in newentries:
            if entry[1] in imps:
                if not isCrewWin:
                    add_win(entry, True)
                    adjust_elo(entry, True, True)
                else:
                    add_loss(entry, True)
                    adjust_elo(entry, False, True)
            else:
                if isCrewWin:
                    add_win(entry, False)
                    adjust_elo(entry, True, False)
                else:
                    add_loss(entry, False)
                    adjust_elo(entry, False, False)
    for entry in entries:
        if entry[1] in imps:
            if not isCrewWin:
                add_win(entry, True)
                adjust_elo(entry, True, True)
            else:
                add_loss(entry, True)
                adjust_elo(entry, False, True)
        else:
            if isCrewWin:
                add_win(entry, False)
                adjust_elo(entry, True, False)
            else:
                add_loss(entry, False)
                adjust_elo(entry, False, False)
    database.add_entries(newentries, gc)
    database.update_entries(entries, gc)
    return True

#Changes name to a new name on database
#Inputs: 'oldname' 'newname'
#Outputs: succeeds
def change_name(oldname, newname):
    gc = gspread.service_account(filename='client_secret.json')
    entries = database.get_rows([oldname], gc)
    if entries:
        entries[0][1] = newname
        database.update_entries(entries, gc)
    return True

#Adds an elo loss to a given player equal to that of a crew loss
#Inputs: 'name'
#Outputs: succeeds
def elo_loss(name):
    gc = gspread.service_account(filename='client_secret.json')
    entry = database.get_rows([name], gc)
    if entry:
        database.update_entries(adjust_elo(entry, False, False), gc)
    return True
