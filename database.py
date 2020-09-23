import gspread

#getRows containing names passed
#input: list of names, google connection
#output: list of rows containing names
#Format of output: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def getRows(names, gc):
    database = gc.open("Among Us Ranks")
    sheet = database.sheet1
    entries = sheet.get_all_values()
    return [entry for entry in entries if entry[1] in names]

#addEntries updates entries on google sheet
#input: list of entries, google connection
#output: None
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

#addEntries adds entries to google sheet
#input: list of entries, google connection
#output: None
#format of an entry: ['row', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew', 'wl%']
def addEntries(entries, gc):
    database = gc.open("Among Us Ranks")
    sheet = database.sheet1
    update = sheet.get_all_values()
    update = [entry for entry in update if entry[1] == '']
    update = update[:len(entries)]
    update = [[row[0], entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], row[-1]] for entry, row in zip(entries, update)]
    updateEntries(update, gc)


if __name__ == '__main__':
    gc = gspread.service_account(filename='client_secret.json')
    updateEntries([['3', 'Dale', 'Bronze 2', 900, 10, 2, 1, 5, 5, 0]], gc)