from MySQLdb import _mysql as sql
from backend import document

db = sql.connect(host="localhost", db="amongus")

#Gets rows containing ids passed
#Inputs: list of ids, google connection
#Outputs: list of rows containing ids
#Format of entry: ['userid', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew']
def get_rows(ids):
    c=db.cursor()
    result = []
    for id in ids:
        c.execute("""SELECT * FROM leaderboard WHERE id = %s""", (id,))
        result.append(c.fetchone())
    c.close()
    return result

def get_rows_by_name(names):
    c=db.cursor()
    result = []
    for name in names:
        c.execute("""SELECT * FROM leaderboard WHERE player_name = %s""", (name,))
        result.append(c.fetchone())
    c.close()
    return result

#Updates entries on google sheet
#Inputs: list of entries, google connection
#Outputs: succeeds
#Format of entry: ['userid', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew']
def update_entries(entries):
    c=db.cursor()
    c.execute("""UPDATE leaderboard VALUES id = %s, player_name = %s, ranks = %s, elo = %s, total_games = %s, crew_games = %s, crew_win = %s, imp_games = %s, imp_win = %s WHERE id = %s""", [tuple(entry + [entry[0]]) for entry in entries])
    c.close()
    return True

#Adds entries to google sheet
#Inputs: list of entries, google connection
#Outputs: succeeds
#Format of entry: ['userid', 'Name', 'rank', 'elo', 'total_games', 'imp_wins', 'crew_wins', 'times_imp', 'times_crew']
def add_entries(entries):
    c=db.cursor()
    c.execute("""INSERT INTO leaderboard VALUES %s, %s, %s, %s, %s, %s, %s, %s, %s""", [tuple(entry) for entry in entries])
    c.close()
    return True