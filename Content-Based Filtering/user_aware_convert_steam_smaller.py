import pandas as pd

dfmain = pd.read_csv('steam-200k.csv')
dfid = pd.read_csv('steam.csv')
dfdesc = pd.read_csv('steam_description_data.csv')


dfdesc['appid'] = dfdesc['steam_appid']

df_game_info = pd.merge(left=dfid, right=dfdesc, on='appid')
df_game_info['description'] = df_game_info['developer'].str.cat(df_game_info[['publisher', 'platforms', 'categories', 'genres', 'steamspy_tags']], sep=';')
df_game_info['description'] = df_game_info['description'].str.replace(' ', '')
df_game_info['description'] = df_game_info['description'].str.replace(';', ' ')
#df_game_info['description'] = df_game_info['description'].str.cat(df_game_info['short_description'], sep=' ')
df_game_info['id'] = df_game_info['name']

lazy = dfmain[['name']].copy()
lazy['id'] = lazy['name']
lazy['description'] = lazy['name']
lazy = lazy.drop_duplicates()
result = pd.concat([df_game_info[['id', 'description']], lazy[['id', 'description']]])
result = result.drop_duplicates()
result.to_csv('game_info.csv', index=False)

dfmain['action'] = 'play'
df_main_info = dfmain
df_main_info = df_main_info.drop_duplicates(subset=['player_id', 'name'], keep='last')
df_main_info = dfmain[dfmain['amount'] >= 1.0]
result = df_main_info[['player_id', 'name', 'amount']]
result.to_csv('user_info.csv', index=False)
