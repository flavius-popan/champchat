#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import praw
import time
import collections

# List buffer/deque to hold comment ids
processed_deque = collections.deque(maxlen=9000)


def main():
    global processed_deque
    r = praw.Reddit('comment flow gauge v0.1 by u/locrawl - measures comments each 3 sec')
    last_time = 0
    while len(processed_deque) < 9000:
        old_count = len(processed_deque)
        all_comments = r.get_comments('leagueoflegends', limit=100)

        for comment in all_comments:
            if comment.id not in processed_deque:
                processed_deque.append(comment.id)

        new_count = len(processed_deque)
        if old_count != new_count:
            print(len(processed_deque), new_count - old_count, (time.time() - last_time))
            last_time = time.time()

        time.sleep(3)

if __name__ == "__main__":
    main()