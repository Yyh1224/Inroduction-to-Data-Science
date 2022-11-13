#import file
import csv
data = open('IMDB-Movie-Data.csv')
# store data into dict by key idx
data_dict = {}
idx = 1
for row in csv.DictReader(open('IMDB-Movie-Data.csv', 'r')):
    data_dict[idx]=row
    idx += 1
#preprocess string to list get rid of unnecessary signs
for i in data_dict:
    data_dict[i]['Genre'] = data_dict[i]['Genre'].split('|')
    data_dict[i]['Actors'] = data_dict[i]['Actors'].replace(' ','')
    data_dict[i]['Actors'] = data_dict[i]['Actors'].split('|')

def removekey(d, key):#remove item from dictionary
		r = dict(d)
		del r[key]
		return r

##Top-3 movies with the highest ratings in 2016
def Q1():
	rate = {}
	for i in data_dict:
		if data_dict[i]['Year'] == '2016':#select those in 2016
			rate[i]=data_dict[i]['Rating']
	highest_rate = []
	count = 0
	max_rate = max(rate.values())
	for key, value in rate.items():
		if count < 3:#select 3 highest
			highest_rate.append(data_dict[key]['Title'])
			rate = removekey(rate, key)#remove the highest
			count += 1
			max_rate = max(rate.values())
	return highest_rate
print("Top-3 movies with the highest ratings in 2016: ",Q1())

ls_actors = []#get actor list
for i in data_dict:
	for i in data_dict[i]['Actors'] :
		if i not in ls_actors:
			ls_actors.append(i)
## The actor generating the highest average revenue?
def Q2():
	
	rev_avg = {}#store the average revenue for each actor
	for i in ls_actors:
		count = 0
		rev_avg[i] = 0
		for j in data_dict:
			if i in data_dict[j]['Actors']:
				if data_dict[j]['Revenue (Millions)'] != '':
					count +=1
					rev_avg[i] += float(data_dict[j]['Revenue (Millions)'])
		if count != 0:
			rev_avg[i] = rev_avg[i]/count#calculate average
	max_avg = max(rev_avg.values())
	high_avg_rev = []
	for key, value in rev_avg.items():
		if value == max_avg:
			high_avg_rev.append(key)
	return high_avg_rev
print("====================================================")
print("The actor generating the highest average revenue: ",Q2())

## The average rating of Emma Watson’s movies?
def Q3():
	emma_rate = []
	for i in data_dict:#store the rate related to emma
		if 'EmmaWatson' in data_dict[i]['Actors']:
			emma_rate.append(data_dict[i]['Rating'])
	total = 0
	count = 0
	for i in emma_rate:
		count += 1
		total += float(i)
	average = total/count#calculate rating for emma's movies
	return (" average rating of Emma Watson’s movies "+str(average))
print("====================================================")
print(Q3())

def max_num(d):#return max len for each dict[key]
    max_n = 0
    for key in d.keys():
        num = len(d[key])
        if max_n<num:
            max_n = num
            temp = key
    return temp, max_n

## Top-3 directors who collaborate with the most actors?
def Q4():
	director = []
	for i in data_dict:#get director list
		if data_dict[i]['Director'] not in director:
			director.append(data_dict[i]['Director'])
	dir_col = {}#set list to library by director key
	for i in director:
		dir_col[i]=[]
	for key in dir_col.keys():
		for i in data_dict:
			if data_dict[i]['Director'] == key:
				for j in range(len(data_dict[i]['Actors'])):#get actors for each director
					if data_dict[i]['Actors'][j] not in dir_col[key]:
						dir_col[key].append(data_dict[i]['Actors'][j])
	ls_dir_most = []#top 3 directors list
	count = 0
	while count < 3:
		temp, num = max_num(dir_col)
		dir_col = removekey(dir_col, temp)#remove max to find next max
		count += 1
		ls_dir_most.append(temp)
	return (ls_dir_most)
print("====================================================")
print('Top-3 directors who collaborate with the most actors: ',Q4())

## Top-2 actors playing in the most genres of movies?
def Q5():
	actor_genres = {}
	for i in ls_actors:
		actor_genres[i]=[]
	for i in ls_actors:
		for j in data_dict:
			if i in data_dict[j]['Actors']:
				for k in range(len(data_dict[j]['Genre'])):
					actor_genres[i].append(data_dict[j]['Genre'][k])
					#drop duplicate elements in list
					actor_genres[i] = list(dict.fromkeys(actor_genres[i]))
	ls_actor_genres = []#top 2 actors genres
	count = 0
	while count < 2:
		actor, g_num = max_num(actor_genres)
		actor_genres = removekey(actor_genres, actor)#remove max to find next max
		count += 1
		ls_actor_genres.append(actor)
	return ls_actor_genres
print("====================================================")
print('Top-2 actors playing in the most genres of movies: ',Q5())

## Top-3 actors whose movies lead to the largest maximum gap of years?
def Q6():
	actor_year = {}
	for i in ls_actors:
		actor_year[i]=[]
	for i in ls_actors:
		for j in data_dict:
			if i in data_dict[j]['Actors']:
				actor_year[i].append(data_dict[j]['Year'])#get every year for each actor
	for key, value in actor_year.items():#calculate gap year
		max_year = max(actor_year[key])
		min_year = min(actor_year[key])
		actor_year[key]=(int(max_year) - int(min_year))
	ls_gap = []
	for i, value in actor_year.items():
		if actor_year[i] == max(actor_year.values()):
			ls_gap.append(i)
	return ls_gap
print("====================================================")
print('Top-3 actors whose movies lead to the largest maximum gap of years: ',Q6())

## Find all actors who collaborate with Johnny Depp in direct and indirect ways
def Q7():
	def searchrelation(ls_johnny, data):
		relation = []#related movie
		for i in ls_johnny:
			for j in data:
				if i in data[j]['Actors']:
					relation.append(j)

		for i in relation:#append related actors
			for j in range(len(data[i]['Actors'])):
				ls_johnnyDepp.append(data[i]['Actors'][j])
		ls_johnny = list(dict.fromkeys(ls_johnny))#remove duplicated actors
		num = len(ls_johnny) 
		return ls_johnny, num
	ls_johnnyDepp = []
	for j in data_dict:
		if 'JohnnyDepp' in data_dict[j]['Actors']:
			for i in range(len(data_dict[j]['Actors'])):
				ls_johnnyDepp.append(data_dict[j]['Actors'][i])
	ls_johnnyDepp = list(dict.fromkeys(ls_johnnyDepp))
	ls_johnnyDepp, n = searchrelation(ls_johnnyDepp, data_dict)
	pre_n = -1
	n = 0
	while(pre_n!= n):#search for related actors until find it all
		pre_n = n
		ls_johnnyDepp, n = searchrelation(ls_johnnyDepp, data_dict)
	return ls_johnnyDepp
print("====================================================")
print('all actors who collaborate with Johnny Depp in direct and indirect ways: ',Q7())