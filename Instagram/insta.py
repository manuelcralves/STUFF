import instaloader 
from instaloader import Profile 
from getpass import getpass
from tqdm import tqdm
from prettytable import PrettyTable

L = instaloader.Instaloader()

username = input("Enter your Instagram username: ")
password = getpass("Enter your Instagram password: ")

L.login(username, password)

profile = Profile.from_username(L.context, username)

print("\nWelcome ", username)
print("\nFetching followers...")

followers = set()
for follower in tqdm(profile.get_followers(), desc="Followers"):
    followers.add(follower.username)

print("Number of followers:", len(followers))

print("\nFetching followees...")

followees = set()
for followee in tqdm(profile.get_followees(), desc="Followees"):
    followees.add(followee.username)

print("Number of followees:", len(followees))

not_following_back = followees - followers

table = PrettyTable()
table.field_names = ["Users who don't follow you back"]

for user in not_following_back:
    table.add_row([user])

print("\nNumber of users who don't follow you back:", len(not_following_back))
print(table)