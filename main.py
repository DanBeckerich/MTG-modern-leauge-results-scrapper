import requests
import re
import csv
import time
from bs4 import BeautifulSoup

# constants
HG = "Hogaak, Arisen Necropolis"
FL = "Faithless Looting"


# this function will hamdle each URL
def digest(url, writer):
    FLcount = 0
    HGcount = 0

    # strip off the new line character. this one gave me some trouble
    response = requests.get(url.rstrip("\n"))

    soup = BeautifulSoup(response.content, 'html5lib')

    # use a bit of regex to extract the date from the URL
    pattern = re.compile("\d\d\d\d-\d\d-(\d\d|\d)")
    date = pattern.search(url)

    print("parsing data from " + date.group())

    # find each deck listing
    decks = soup.find_all("div", attrs={"class": "sorted-by-overview-container sortedContainer"})
    for deck in decks:

        # strip out the list of creatures from each deck listing
        creatures = deck.find_all("div", attrs={"class": "sorted-by-creature clearfix element"})
        for creature in creatures:
            row = creature.find_all("span", attrs={"class": "row"})
            for entry in row:
                # and finally extract the creature name, check if it matches the one we are looking for and increment the counter
                if entry.find("span", attrs={"class": "card-name"}).get_text().lower().strip() == HG.lower().strip():
                    HGcount = HGcount + int(entry.find("span", attrs={"class": "card-count"}).get_text())

        # repeat the process for sourceries.
        sorceries = deck.find_all("div", attrs={"class": "sorted-by-sorcery clearfix element"})
        for sorcery in sorceries:
            row = sorcery.find_all("span", attrs={"class": "row"})
            for entry in row:
                if entry.find("span", attrs={"class": "card-name"}).get_text().lower().strip() == FL.lower().strip():
                    FLcount = FLcount + int(entry.find("span", attrs={"class": "card-count"}).get_text())

    # print the date and count of each card
    print(date.group())
    print(HG + " was used " + str(HGcount) + " times")
    print(FL + " was used " + str(FLcount) + " times")
    # write the data to the datafile
    writer.writerow({"date": date.group(), "Hogaak": HGcount, "Faithless Looting": FLcount})


def main():
    # open the list of url's
    urlList = open(r"URLs.txt", "r")
    with open('cardData.csv', mode='w') as csv_file:
        # set a header
        fnames = ['date', 'Hogaak', 'Faithless Looting']
        writer = csv.DictWriter(csv_file, fieldnames=fnames)
        writer.writeheader()

        # iterate over each URL and digest it.
        for url in urlList.readlines():
            print(url)
            digest(url, writer)
            # be nice to their servers. add a one second delay in between each server request.
            time.sleep(1)

    urlList.close()


if __name__ == "__main__":
    main()
