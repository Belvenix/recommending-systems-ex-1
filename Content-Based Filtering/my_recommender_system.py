import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from numpy import log as ln

ids = [63276972, 107948398, 248444377, 25096601, 65958466, 90711776, 186452037, 90033155, 50818751, 142999522]

users_df = pd.read_csv("user_info.csv")
ds = pd.read_csv("game_info.csv")

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['description'])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

    results[row['id']] = similar_items[1:]
    
print('done!')
def item(id):
    return ds.loc[ds['id'] == id]['id'].tolist()[0].split(' - ')[0]

def recommend(item_id, num):
	recs = [(0, '')]
	if item_id in results:
		recs = results[item_id][:num]
	return recs

def sort_key_recs(recs):
	return recs[1]

rec_num = 10
r_a = {}
for i_d in ids:
	print(f'Recommending for {i_d}:')
	items = users_df[users_df['player_id'] == i_d]
	not_available = []
	recommendations = {}
	for item in items.itertuples(index='False'):
		i, _, game, time_spent = item
		not_available += [game]
		recs = recommend(item_id=game, num=rec_num)
		for a in recs:
			if a is int:
				continue
			score, name = a[0], a[1]
			if name in recommendations:
				recommendations[name] += score #* max(0.0, ln(time_spent))
			else:
				recommendations[name] = score #* max(0.0, ln(time_spent))
	l = []
	for r in recommendations:
		l.append((r, recommendations[r]))
	l = sorted(list(l)[:rec_num], key=sort_key_recs, reverse=True)
	recs = []
	for rec, t in l:
		if rec not in not_available:
			print(f'{rec} - Score: {t}!')
			recs.append(rec)
	r_a[i_d] = recs
print(r_a)
		
				
		
