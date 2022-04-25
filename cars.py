import numpy as np
from operator import itemgetter
import json

NUMBER_OF_CARS_TO_RECOMMEND = 2

#Read variables from JSON files
users_liked = json.load(open('user_ratings.json', 'r'))

#price, year, mileage, engine size.
properties_of_cars = json.load(open('properties_of_cars.json', 'r'))

recommendations = {}


def disimilarity_function(a, b):
    return np.linalg.norm(np.array(a)-np.array(b))

#iterate in order to provide a recommondation for each user
for user, liked_list in users_liked.items():
    #Initialise recommendations as an empty list
    recommendations[user] = []

    #Once a user has alreadt liked a car, this prevents it being recommended again
    set_of_cars_liked_or_recommended = set()
    for car_liked in liked_list:
        set_of_cars_liked_or_recommended.add(car_liked[0])
    #while there's not enough recommendations
    while len(recommendations[user]) < NUMBER_OF_CARS_TO_RECOMMEND:
        #add the most similar car to ones that have been liked
        for car_liked in liked_list:
            car_id, ratings = car_liked
            car_vector = properties_of_cars[car_id]

            #contains cars that can be recommended
            possible_matches = []
            for id_other, vector_other in properties_of_cars.items():
                if id_other in set_of_cars_liked_or_recommended:
                    continue

                disimilarity = disimilarity_function(car_vector, vector_other)
                #add to list with id and value
                possible_matches.append( [id_other, disimilarity] )
                #sort items by the value
                sorted_matches = sorted(possible_matches, key=itemgetter(1))
                #get the best car(s) to recommend
                best = 0
                set_of_cars_liked_or_recommended.add(sorted_matches[best][0])
                #add car to the recommendations
                recommendations[user].append(sorted_matches[best][0])
                #stop the loop if there are enough cars
                if len(recommendations[user]) == NUMBER_OF_CARS_TO_RECOMMEND:
                    break


#save the output to the JSON file
fd = open('output.json', 'w')
json.dump(recommendations, fd)
fd.close()
print (f' {recommendations[user]}')
