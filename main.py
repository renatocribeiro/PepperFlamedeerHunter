import time
from random import randint
from WebsiteThread import *
from Agents import *
from users import *
import argparse

AGENTS = [my_agent]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only-dump',  action='store_true')
    parser.add_argument('--debug',  action='store_true')
    args = parser.parse_args()
    while True:
        try:
            threads = []
            for agent in AGENTS:
                for user in USERS[agent.short]:
                    threads.append(WebsiteThread(agent, user, args.only_dump, debug = args.debug))
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
            if args.only_dump:
                break
            time.sleep(60*5) #don't abuse ;)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
