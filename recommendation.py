#a dictionary of movie critics and their rating on set of movies

critics= {'Lisa Rose':{'Lady in the water':2.5,'Snakes on plane':3.5,'Just My luck':3.0,'Superman Return':3.5,'You,Me and Dupee':2.5,'The night listener':3.0},
          'Gene Seymour':{'Lady in the water':3.0,'Snakes on plane':3.5,'Just My luck':1.5,'Superman Return':5.0,'You,Me and Dupee':3.5,'The night listener':3.0},
          'Michael Phillips':{'Lady in the water ':2.5,'Snakes on plane':3.0,'Superman Return':3.5,'You,Me and Dupee':2.5,'The night listener':4.0},
          'Claudia Puig':{'Lady in the water ':2.5,'Snakes on plane':3.5,'Just My luck':3.0,'Superman Return':4.0,'You,Me and Dupee':2.5,'The night listener':4.5},
          'Mick Lasalle':{'Lady in the water ':3.0,'Snakes on plane':4.0,'Just My luck':2.0,'Superman Return':3.0,'You,Me and Dupee':2.0,'The night listener':3.0},
          'Jack Matthews':{'Lady in the water ':3.0,'Snakes on plane':4.0,'Superman Return':5.0,'You,Me and Dupee':3.5,'The night listener':3.0},
          'Toby':{'Lady in the water ':2.5,'Snakes on plane':4.5,'Superman Return':4.0,'You,Me and Dupee':1.0}}

from math import sqrt

#Returns a similarity score based on person 1 and person 2 score

def sim_distance(prefs,person1,person2):
    #Get the list of Shared Item
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    #if they have no rating in common return 0
    if len(si)==0:
        return 0
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                        for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sum_of_squares)


#Returns a pearson correlation

def sim_pearson(prefs,p1,p2):
    #Get list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    n=len(si)

    if n==0:
        return 0

    #Add up all the preferences

    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    #sum of squares
    sum1sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2sq=sum([pow(prefs[p2][it],2) for it in si])


    #sum of products

    sump=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    #calculate pearson score

    num = sump-(sum1*sum2/n)
    den=sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
    if den==0:
        return 0

    r=num/den

    return r


#Ranking the critics

def topMatches (prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other)
            for other in prefs if other!=person]

    #sort

    scores.sort()
    scores.reverse()
    return scores[0:n]


#Get recommendation for a person using weighted avg
def getRecommendation (prefs,person,similarity=sim_pearson):
    total={}
    simsum={}

    for other in prefs:
        if other==person:
            continue
        sim=similarity(prefs,person,other)
        #Igonre negative values
        if sim<0:
            continue
        for item in prefs[other]:

            #only score movies that i havent seen
            if item not in prefs[person] or prefs[person][item]==0:
            
                total.setdefault(item,0)
                total[item]+=prefs[other][item]*sim

                simsum.setdefault(item,0)
                simsun[item]+=sim

        #Create normalised list
        rankings=[(total/simsum[item],item) for item,total in total.item()]

        #return sorted list
        rankings.sort()
        rankings.reverse()
        return ranking

#Matching products
def transformprefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            #flip item to person
            result[item][person]=prefs[person][item]
    return result

        

#load a data set

def loadMovielens(path='ml-100k'):
    #get movie titles
    movies={}
    for line in open(path+'/u.item'):
        
        (id,title)=line.split('|')[0:2]
        movies[id]=title

    #load data
    prefs={}
    for line in open(path+'/u.data'):
        
        (user,movieid,rating,ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs

    
        

        



    
            
    
