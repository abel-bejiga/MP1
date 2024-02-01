from user import User
from utils import distance_km

def cp2_1_simple_inference(dictUsers):
    dictUsersInferred = dict()

    for user_id, user in dictUsers.items():
        if user.home_shared:
            dictUsersInferred[user_id] = User(user)
        else:
            f = [dictUsers[friend_id] for friend_id in user.friends if dictUsers[friend_id].home_shared]
            if f:
                home_locations = [(friend.home_lat, friend.home_lon) for friend in f]
                median_lat = sum(home[0] for home in home_locations) / len(home_locations)
                median_lon = sum(home[1] for home in home_locations) / len(home_locations)
                dictUsersInferred[user_id] = User(user.id, median_lat, median_lon, True)
            else:
                dictUsersInferred[user_id] = User(user)

    return dictUsersInferred

def cp2_2_improved_inference(dictUsers):
    dictUsersInferred = dict()

    for user_id, user in dictUsers.items():
        if user.home_shared:
            dictUsersInferred[user_id] = User(user)
        else:
            friends_of_friends = set()
            for friend_id in user.friends:
                friends_of_friends.update(dictUsers[friend_id].friends)

            shared_home_locations = [
                (dictUsers[friend_id].home_lat, dictUsers[friend_id].home_lon)
                for friend_id in friends_of_friends
                if dictUsers[friend_id].home_shared
            ]

            if shared_home_locations:
                sorted_home_locations = sorted(shared_home_locations)
                n = len(sorted_home_locations)
                mid = n // 2
                if n % 2 == 0:
                    median_lat = (sorted_home_locations[mid - 1][0] + sorted_home_locations[mid][0]) / 2
                    median_lon = (sorted_home_locations[mid - 1][1] + sorted_home_locations[mid][1]) / 2
                else:
                    median_lat, median_lon = sorted_home_locations[mid]

                dictUsersInferred[user_id] = User(user.id, median_lat, median_lon, True)
            else:
                f = [dictUsers[friend_id] for friend_id in user.friends if dictUsers[friend_id].home_shared]
                if f:
                    home_locations = [(friend.home_lat, friend.home_lon) for friend in f]
                    median_lat = sum(home[0] for home in home_locations) / len(home_locations)
                    median_lon = sum(home[1] for home in home_locations) / len(home_locations)
                    dictUsersInferred[user_id] = User(user.id, median_lat, median_lon, True)
                else:
                    dictUsersInferred[user_id] = User(user)

    return dictUsersInferred

def cp2_calc_accuracy(truth_dict, inferred_dict):
    if len(truth_dict) != len(inferred_dict) or len(truth_dict) == 0:
        return 0.0
    sum = 0
    for i in truth_dict:
        if truth_dict[i].home_shared:
            sum += 1
        elif truth_dict[i].latlon_valid() and inferred_dict[i].latlon_valid():
            if distance_km(truth_dict[i].home_lat, truth_dict[i].home_lon, inferred_dict[i].home_lat,
                           inferred_dict[i].home_lon) < 25.0:
                sum += 1
    return sum * 1.0 / len(truth_dict)
