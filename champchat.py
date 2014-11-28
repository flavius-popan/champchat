#!/usr/bin/env python

import pdb
import praw
import time


def main():
    r = praw.Reddit('r/leagueoflegends champchatter bot v0.1 by u/locrawl')

    try:
        with open('champions.txt', 'r') as infile:
            champion_names = set(line.strip().lower() for line in infile)
    except IOError:
        print('error opening file')

    seen = []

    while True:
        all_comments = r.get_comments('leagueoflegends', limit=None)

        for comment in all_comments:
            split_body = comment.body.lower().split()
            if any(name in split_body for name in champion_names) and comment.id not in seen:
                print(get_names(split_body, champion_names))
                print(comment.author)
                print(comment.submission)
                print(comment.permalink)
                print()
                seen.append(comment.id)

        time.sleep(2)


def get_names(split_body, names):
    found = ""
    for name in names:
        if name in split_body:
            found += name + " "

    return found

if __name__ == "__main__":
    main()