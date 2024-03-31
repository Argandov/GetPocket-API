#!/usr/bin/env python3

from datetime import datetime, timedelta
from modules.tagging import tags_list
import os
import requests
import sys
import json
import argparse
from dotenv import load_dotenv, dotenv_values

load_dotenv()
POCKET_APP_NAME = os.environ.get("POCKET_APP_NAME")
consumer_key = os.environ.get("POCKET_CONSUMER_KEY")
access_token = os.environ.get("POCKET_ACCESS_TOKEN")

def last_week_timestamp()-> int:

    """     

        This function does not work anymore since Pocket's API does not respond to relative timestamps 
        (It ignores the "since" parameter)

    """

    # Current time
    now = datetime.now()

    # Time 1 week ago from now
    one_week_ago = now - timedelta(weeks=1)

    # Convert to UNIX timestamp (and round down or convert to integer if necessary)
    one_week_ago_timestamp = int(one_week_ago.timestamp())

    return one_week_ago_timestamp

def format_timestamps(UNIX_TIMESTAMP) -> str:

    """
        Convert UNIX timestamps to readable format
        For use when formatting Pocket API results
    """

    TS = int(UNIX_TIMESTAMP)
    timestamp = datetime.fromtimestamp(TS).strftime('%Y-%m-%d %H:%M:%S')
    
    return timestamp

def get_last_posts(one_week_ago_timestamp, consumer_key, access_token):
    url = "https://getpocket.com/v3/get"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "consumer_key": consumer_key,
        "access_token": access_token,
        "count": "100",
        "detailType": "complete"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response # RETURN RAW TEXT
    else:
        print(f"[X] ERROR!: {response.status_code}")
        sys.exit(1)

def retrieve_articles(res: dict[str], tag) -> int:
    """
        Regresa la lista completa

    """
    wordcount = 0

    for key, value in res.items():
        if isinstance(value, dict) and "tags" in value:

            if tag not in value["tags"]:
                continue
                # If the item is archived:
            elif str(value["status"]) == 1:
                continue
                # If the item is marked as deleted:
            elif str(value["status"]) == 2:
                continue

            wordcount += int(value["word_count"])

                # Time when article was added to Pocket
            time_added = format_timestamps(value["time_added"])

                # Time when article itself has been changed/updated
                # Not very useful: any change (New comments, etc) influence this value
            time_updated = format_timestamps(value["time_updated"])

            article_id_list.append(value["item_id"])

            print("***"*20)
            print(f" - Time Added: {time_added}")
            #print(f" - Time Updated: {time_updated}")
            print(f" - ID: {value["item_id"]}")
                # Not very useful; prone to errors:
            print(f" - Is Article: {\
                    "yes" if int(value["is_article"]) == 1 else \
                    "no"}")
            print(f" - Word Count: {value["word_count"]}")
            print(f" - Language: {value["lang"]}")
            print(f" - Title: {value["resolved_title"]}")
            print(f" - Description (Excerpt): {"N/A" if not value["excerpt"] else value["excerpt"]}")
            print(f" - URL: {value["resolved_url"]}")
            print(f" - Video: {"Includes Video" if int(value["has_video"]) == 1 else ("Is a Video" if int(value["has_video"]) == 2 else "No")}")
            
        else:
            pass

    return wordcount

def argument_parser(tags_list:list[str]) -> list[str]:
    parser = argparse.ArgumentParser(description='Pocket API Help:')
        # Parse arguments
    parser.add_argument('--list', '-l', nargs='?', const=True, default=None, help='List available tags')
    parser.add_argument('--tag', '-t', help='Specify a tag')
            # Argument Parsing
    args = parser.parse_args()
    if args.list:
        for tag in tags_list:
            print(tag)
        sys.exit(0)
    elif args.tag:
        tag = args.tag
    else:
        print("[x] Must specify a Tag. Exiting...")
        sys.exit(1)
    return args, tag



args, tag = argument_parser(tags_list)

relative_time = last_week_timestamp()
raw = get_last_posts(relative_time, consumer_key, access_token)

articles = raw.json()["list"]
    # "list" is the actual value of the nested Dict that Pocket sends where the articles are listed.
#articles = json_obj["list"]

article_id_list = []
wordcount = retrieve_articles(articles, tag)

if len(article_id_list) == 0:
    print("[-] No results")
else:
    print("---"*35)
    print(f"TAG: {tag} | WC: {wordcount} | ARTICLES: {len(article_id_list)}")

""" Useful for later: Archive after reading """
#archive_items(article_id_list)
