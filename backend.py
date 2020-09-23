import database, gspread, json

winelo = {}
losselo = {}
with open('winelo.json') as f:
  winelo = json.load(f)
with open('losslo.json') as f:
  losselo = json.load(f)

#Determines how much ELO should change based on rank
#Input: 'rank' result-T(Win)/F(Lost) imp-True(imp)/False(crew) place-True(in placements)/False(not)
#Output: elochange
def getEloChange(rank, result, imp, place):
    elochange = 0
    if result:
        elochange = winelo[rank]
        if imp:
            elochange *= 2
    else:
        elochange = losselo[rank]
        if not imp:
            elochange *= 2
    if place:
        elochange *= 2
    return elochange

#Adds a loss to the player
#Input: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
#Output: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def addLoss(entry, imp):
    if imp:
        entry[7] = str(int(entry[7]) + 1)
    else:
        entry[8] = str(int(entry[8]) + 1)
    entry[4] = str(int(entry[4]) + 1)
    return entry

#Adds a win to the player
#Input: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
#Output: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def addWin(entry, imp):
    if imp:
        entry[5] = str(int(entry[5]) + 1)
    else:
        entry[6] = str(int(entry[6]) + 1)
    return addLoss(entry, imp)

#Adjusts elo based on win, imp, and rank
#Input: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
#Output: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def adjustElo(entry, result, imp):
    elochange = getEloChange(entry[2], result, imp, int(entry[4]) <= 5)
    newelo = int(entry[3]) + elochange
    entry[3] = str(newelo if newelo > 0 else 0)
    return entry

#The base entry for a new player
baseentry = ['0', '', 'Silver 1', '300', '0', '0', '0', '0', '0', '0']

#A function to add a game to the database
#Input: [names of players] [names of imps] result-True(Crew win)/False(Imp win)
#Output: T/F
def addGame(names, imps, result):
    gc = gspread.service_account(filename='client_secret.json')
    entries = database.getRows(names, gc)
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
                if not result:
                    addWin(entry, True)
                    adjustElo(entry, True, True)
                else:
                    addLoss(entry, True)
                    adjustElo(entry, False, True)
            else:
                if result:
                    addWin(entry, False)
                    adjustElo(entry, True, False)
                else:
                    addLoss(entry, False)
                    adjustElo(entry, False, False)
    for entry in entries:
        if entry[1] in imps:
            if not result:
                addWin(entry, True)
                adjustElo(entry, True, True)
            else:
                addLoss(entry, True)
                adjustElo(entry, False, True)
        else:
            if result:
                addWin(entry, False)
                adjustElo(entry, True, False)
            else:
                addLoss(entry, False)
                adjustElo(entry, False, False)
    database.addEntries(newentries, gc)
    database.updateEntries(entries, gc)
    return True