#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pdb
import html
import praw
import time
import collections

# List buffer/deque to hold comment ids
processed_deque = collections.deque(maxlen=9000)


def main():
    global processed_deque
    
    r = praw.Reddit('r/leagueoflegends champchatter bot v0.1 by u/locrawl')
    r.config.decode_html_entities = True

    champion_names = []
    space_names = []
    single_names = []

    try:
        with open('champions.txt', 'r') as infile:
            champion_names += set(line.strip() for line in infile)
    except IOError:
        print('error opening file')

    for name in champion_names:
        if ' ' in name:
            space_names.append(name)
        else:
            single_names.append(name)

    # while True:
    all_comments = r.get_comments('leagueoflegends', limit=None)

    for comment in all_comments:
        if comment.id not in processed_deque:
            found_names = find_names(comment, space_names, single_names)
            processed_deque.append(comment.id)
            if found_names:
                print(found_names)
                # print(comment.author)
                # print(str(comment.submission))
                print(comment.permalink)
                print()

        # time.sleep(3)


def find_names(comment, space_names, single_names):
    found_names = []

    # Make comment lowercase to ease matching
    text = html.unescape(comment.body.lower())

    # Find names with spaces before we split on spaces
    for space_name in space_names:
        if space_name in text:
            # Append the first part of the name to rejoin later
            found_names.append(space_name)

    # Next, split text on spaces
    split_text = text.split()

    # Search for the remainder of champion name list

    for word in split_text:
        # Remove all non-letter characters
        word = re.sub("[^a-z\']", "", word)
        # Remove instances of 's
        if word[-2:] == "'s":
            word = word[:-2]
        # Skip one letter words
        if len(word) > 1:
            for single_name in single_names:
                # Check for direct match
                if word == single_name:
                    found_names.append(single_name)
                # Last hope: check for pluralized version of name (ie. mundos)
                elif word[-1] is 's':
                    if word[:-1] == single_name:
                        found_names.append(single_name)

    if found_names:
        return set(found_names)
    else:
        return False

if __name__ == "__main__":
    main()