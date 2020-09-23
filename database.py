import gspread

#Gets rows containing names passed
#Inputs: list of names, google connection
#Outputs: list of rows containing names
#Format of output: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def getRows(names, gc):
    database = gc.open("Among Us Ranks")
    sheet = database.sheet1
    entries = sheet.get_all_values()
    return [entry for entry in entries if entry[1] in names]

#Updates entries on google sheet
#Inputs: list of entries, google connection
#Outputs: succeeds
#format of an entry: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def updateEntries(entries, gc):
    database = gc.open("Among Us Ranks")
    sheet = database.sheet1
    start = 'B'
    startstats = 'D'
    end = 'I'
    update = []
    for entry in entries:
        update.append({'range': start + entry[0] + ':' + start + entry[0], 'values': [[entry[1]]]})
        update.append({'range': startstats + entry[0] + ':' + end + entry[0], 'values': [entry[3:-1]]})
    sheet.batch_update(update, value_input_option='USER_ENTERED')
    return True

#Adds entries to google sheet
#Inputs: list of entries, google connection
#Outputs: succeeds
#format of an entry: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def addEntries(entries, gc):
    database = gc.open("Among Us Ranks")
    sheet = database.sheet1
    update = sheet.get_all_values()
    update = [entry for entry in update if entry[1] == '']
    update = update[:len(entries)]
    update = [[row[0]] + entry[1:9] + [row[-1]] for entry, row in zip(entries, update)]
    updateEntries(update, gc)
    return True