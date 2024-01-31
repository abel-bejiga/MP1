# cp1.py

import csv
from user import User

def cp1_1_parse_homes(f):
    dictUsers_out = dict()
    with open(f) as csv_f:
        for row in csv.reader(csv_f):
            user_id, latitude, longitude, category = row
            user_id = int(user_id)
            latitude, longitude = map(float, (latitude, longitude))
            home_shared = int(category) == 1  # Convert category to boolean
            dictUsers_out[user_id] = User(user_id, latitude, longitude, home_shared)
    return dictUsers_out



def cp1_2_parse_friends(f, dict_users):
    with open(f) as csv_f:
        for row in csv.reader(csv_f):
            user_id, friend_id = map(int, row)
            dict_users[user_id].friends.add(friend_id)

def cp1_3_answers(dict_users):
    u_cnt = len(dict_users)
    u_noloc_cnt = sum(not user.latlon_valid() for user in dict_users.values())
    u_noloc_nofnds_cnt = sum(not user.latlon_valid() and not user.friends for user in dict_users.values())

    p_b = sum(user.home_shared for user in dict_users.values()) / u_cnt if u_cnt > 0 else 0

    # Count users who meet the specified conditions for p_u1 and p_u2
    p_u1 = sum(user.latlon_valid() and user.home_shared for user in dict_users.values()) / u_cnt if u_cnt > 0 else 0
    p_u2 = sum(user.latlon_valid() and user.home_shared and bool(user.friends) for user in dict_users.values()) / u_cnt if u_cnt > 0 else 0

    return u_cnt, u_noloc_cnt, u_noloc_nofnds_cnt, p_b, p_u1, p_u2
