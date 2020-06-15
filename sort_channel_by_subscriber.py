'''
As a user I want to know the best Python Youtube Channels (according to the number of subscribers).
The Output should be structured like this:
1. CoreySchafer: 524.000 subscribers (just an example)

Here is a list of potentially best python channels:

Programming with Mosh
freeCodeCamp.org
Corey Schafer
Keith Galli
Telusko
CS Dojo
Clever Programmer
edureka!
Tech With Tim
ProgrammingKnowledge
sentdex

Solution Approach:
put all descriptive channel name + usernames / ids in one list of tuples
run query for each user name / id (check if the string starts with 'UC')
store results in dictionary with username / id as key and viewcount, subscriber count, videocount as a tuple as value
sort the dictionary by subscribers
format it
print it
save it in a csv file
'''

'''
Improvement Ideas:
- use objects
- parallelize api calls to save time
- save retrieved data in a txt file to reduce the number of api calls (e.g. only call the api when the last update is older than 23 hours)
- add borders to the table
- save results to a csv, excel, or google spreadsheet or publish it on a website
- automate the script e.g. let it run once a day to update info on the website
- automate to retrieve the most interesting channels (e.g. number of videos with python in the name)
'''

from googleapiclient.discovery import build
import os
import csv

# channels have either defined a username or id (idk why)
l_channels = [
    ('Corey Schafer', 'schafer5'),
    ('Programming with Mosh', 'programmingwithmosh'),
    ('freeCodeCamp', 'UC8butISFwT-Wl7EV0hUK0BQ'),
    ('Keith Galli', 'UCq6XkhO5SZ66N04IcPbqNcw'),
    ('Telusko', 'javaboynavin'),
    ('CS Dojo', 'UCxX9wt5FWQUAAz4UrysqK9A'),
    ('Clever Programmer', 'UCqrILQNl5Ed9Dz6CGMyvMTQ'),
    ('edureka!', 'edurekaIN'),
    ('Tech With Tim', 'UC4JX40jDee_tINbkjycV4Sg'),
    ('ProgrammingKnowledge', 'ProgrammingKnowledge'),
    ('sentdex', 'sentdex')
]

youtube_api_key = os.environ.get('YOUTUBE_API_KEY')

d_channels = dict()


def get_channel_info(channel):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    # Check if the parameter is an id or username
    if ch[1][0:2] == 'UC':
        request = youtube.channels().list(
            part='statistics',
            id=ch[1]
        )
    else:
        request = youtube.channels().list(
            part='statistics',
            forUsername=ch[1]
        )

    response = request.execute()

    d_channels[ch] = (
        int(response['items'][0]['statistics']['videoCount']),
        int(response['items'][0]['statistics']['subscriberCount']),
        int(response['items'][0]['statistics']['viewCount'])
    )


def print_dictionary(d_channels):
    print("{:<25} {:<7} {:<12} {:<10}".format(
        'channel', ' videos', ' subscribers', ' views'))
    for key, value in d_channels.items():
        videos, subscribers, views = value
        print("{:<25} {:<7} {:<12} {:<10}".format(
            key, videos, subscribers, views))


def print_list(l_channels_sorted_by_subscribers):
    print("{:<25} {:>7} {:>12} {:>10}".format(
        'channel', ' videos', ' subscribers', ' views'))
    for item in l_channels_sorted_by_subscribers:
        print("{:<25} {:>7} {:>12} {:>10}".format(
            item[0][0], item[1][0], item[1][1], item[1][2]))


def write_to_file(l_channels_sorted_by_subscribers):
    with open("youtube-channels-python.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["channel", "videos", "subscribers", "views"])
        for ch in l_channels_sorted_by_subscribers:
            writer.writerow([ch[0][0], ch[1][0], ch[1][1], ch[1][2]])


for ch in l_channels:
    get_channel_info(ch)

# print(d_channels)

l_channels_sorted_by_subscribers = sorted(
    d_channels.items(), key=lambda elem: elem[1][1], reverse=True)

# print(l_channels_sorted_by_subscribers)

print_list(l_channels_sorted_by_subscribers)

write_to_file(l_channels_sorted_by_subscribers)

