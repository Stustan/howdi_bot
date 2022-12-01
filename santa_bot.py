import random

n = int(input('Введите количество участников: '))
members_list = []
pairs = {}

for i in range(n):
    members_list.append(input())


def shuffle_members (members_list):
    random.shuffle(members_list)
    return members_list

def set_santa (members_list):
    for i in range(n):
        if i == n-1:
            pairs[members_list[n-1]] = members_list[0]
        else:
            pairs[members_list[i]] = members_list[i+1]
    return pairs

shuffle_members(members_list)
print(set_santa(members_list))