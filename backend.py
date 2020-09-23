#Determines how much ELO should change based on rank
#Input: 'rank' result-T(Win)/F(Lost) imp-T(imp)/F(crew) place-T(in placements)/F(not)
#Output: elochange
def getEloChange(rank, result, imp, place):
    winelo = {'Bronze 1': 35, 'Bronze 2': 30, 'Bronze 3': 30, 'Silver 1': 30, 'Silver 2': 25, 'Silver 3': 25, 'Gold 1': 25, 'Gold 2': 20, 'Gold 3': 20, 'Diamond 1': 20, 'Diamond 2': 15, 'Diamond 3': 15, 'Legend': 15}
    losselo = {'Bronze 1': -10, 'Bronze 2': -10, 'Bronze 3': -15, 'Silver 1': -15, 'Silver 2': -20, 'Silver 3': -20, 'Gold 1': -25, 'Gold 2': -25, 'Gold 3': -25, 'Diamond 1': -25, 'Diamond 2': -25, 'Diamond 3': -30, 'Legend': -30}
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
    return addLoss(entry)

#Adjusts elo based on win, imp, and rank
#Input: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
#Output: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def adjustElo(entry, result, imp):
    elochange = getEloChange(entry[2], result, imp, int(entry[4]) <= 10)
    entry[3] = str(int(entry[3]) + elochange)
    return entry