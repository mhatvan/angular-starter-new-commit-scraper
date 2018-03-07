import urllib2
import subprocess as s
import datetime
from bs4 import BeautifulSoup
from slackclient import SlackClient

now = datetime.datetime.now()

slack_channel = 'insert channel here'
slack_token = 'insert token here'

sc = SlackClient(slack_token)


def main():
    url = urllib2.urlopen(
        "https://github.com/gdi2290/angular-starter/commits/master.atom").read()

    soup = BeautifulSoup(url, "xml")

    updated_arr = []

    for updated_tag in soup.find_all('updated'):
        updated_arr.append(updated_tag.get_text(' ', strip=True))

    updated_arr_sorted = sorted(updated_arr, reverse=False)
    most_recent_update_tag = str(
        updated_arr_sorted[len(updated_arr_sorted) - 1])

    with open("angular-starter.txt") as f:
        data = f.readlines()
        lastline = data[-1]

        fw = open('angular-starter.txt', 'a')

        if lastline == most_recent_update_tag:
            sc.api_call("chat.postMessage",
                        channel=slack_channel,
                        text=now.strftime("%Y-%m-%d %H:%M") + ' | no new angular-starter commit found :disappointed:',
                        username='Angular Starter Scraper Bot',
                        as_user=False)
        elif lastline < most_recent_update_tag:
            sc.api_call("chat.postMessage",
                        channel=slack_channel,
                        text=now.strftime("%Y-%m-%d %H:%M") + ' | new angular-starter commit found! :partyparrot: \n check out the repo at https://github.com/gdi2290/angular-starter/commits',
                        username='Angular Starter Scraper Bot',
                        as_user=False)
            fw.write('\n')
            fw.write('\n')
            fw.write(most_recent_update_tag)

        fw.close()


main()
