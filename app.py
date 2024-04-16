#!/usr/bin/env python3

from datetime import datetime, timedelta
from modules.scraper import scrape
from modules.summarizer import summarize
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

def get_last_posts(one_week_ago_timestamp, consumer_key, access_token, results_counter=100):
    url = "https://getpocket.com/v3/get"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "consumer_key": consumer_key,
        "access_token": access_token,
        "count": str(results_counter),
        "detailType": "complete"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response # RETURN RAW TEXT
    else:
        print(f"[X] ERROR!: {response.status_code}")
        sys.exit(1)


def retrieve_articles(res: dict[str], tag: str, results_counter: int):
        # DEFAULT VALUE
    continue_flag = 0
    scraped_articles = []
    """
        Regresa la lista completa

    """

    CONTINUE_MESSAGE = \
            """
    [?] Would you like to summarize this article?
     -  [y]es/ [n]o/ [f]inish and skip this one / Stop Asking and process [A]ll 
    >> """
    wordcount = 0

    # Control flow: User is asked to continue processing articles or not
    counter = 0

    for key, value in res.items():
        if counter == results_counter + 1:
            break
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

                # Print article information If user's previous selection was "y" or "n"
            if continue_flag == 0:

                print(f"****** Article #{str(counter+1)} ******")
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

            if args.process:
                # 0 = Skip current selection
                # 1 = End with current selection, stop processing
                # 2 = Process the rest, don't ask again
                if continue_flag == 1:
                    continue
                elif continue_flag == 0:
                    process_user_selection = input(CONTINUE_MESSAGE)
                    while process_user_selection not in ["y", "n", "f", "a"]:
                        process_user_selection = input(CONTINUE_MESSAGE)
                elif process_user_selection == "a":
                    process_user_selection = "y"
                    continue_flag = 2
                elif continue_flag == 2:
                    process_user_selection == "y"
                if process_user_selection == "y":
                    try:
                        date, raw_article, title, authors = scrape(value["resolved_url"])
                        raw_content = ""
                        raw_content += f"Title: {title}\n"
                        raw_content += f"Authors: {authors}\n"
                        raw_content += f"Date: {date}\n"
                        raw_content += f"Word Count: {value['word_count']}\n"
                        raw_content += f"URL: {value['resolved_url']}\n"
                        raw_content += f"Content: {raw_article}"
                        scraped_articles.append(raw_content)
                    except Exception as e:
                        # Print in color the error:
                        print(f"\033[91m[X] ERROR Scraping this URL: {e}\033[0m")
                elif process_user_selection == "n":
                    continue
                elif process_user_selection == "f":
                    continue_flag = 1
            counter += 1
        else:
            pass

    return wordcount, scraped_articles

def argument_parser(tags_list:list[str]) -> list[str]:
    parser = argparse.ArgumentParser(description='Pocket Wrapper App Help:')
        # Parse arguments
    parser.add_argument('--number', '-n', type=int, default=100, help='Number of articles to retrieve')
    parser.add_argument('--list', '-l', nargs='?', const=True, default=None, help='List available tags')
    parser.add_argument('--process', '-p', nargs='?', const=True, default=None, help='Complete the processing by LLM model (Default: False)')
    parser.add_argument('--tag', '-t', help='Specify a tag')
            # Argument Parsing
    args = parser.parse_args()
    # If no arguments are passed, print help:
    if not args.number:
        results_counter = 100
        print("No limit specified. Defaulting to 100.")
    else:
        results_counter = args.number
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    if args.list:
        for tag in tags_list:
            print(tag)
        sys.exit(0)
    elif args.tag:
        tag = args.tag
    return args, tag, results_counter



args, tag, results_counter = argument_parser(tags_list)

relative_time = last_week_timestamp()
raw = get_last_posts(relative_time, consumer_key, access_token, results_counter)

articles = raw.json()["list"]
    # "list" is the actual value of the nested Dict that Pocket sends where the articles are listed.
#articles = json_obj["list"]

# PHASE 1: Retrieve Articles and Metadata in a list
article_id_list = []
wordcount, scraped_articles = retrieve_articles(articles, tag, results_counter)

if not args.process:
    for article in scraped_articles:
        print(article)
    print(f"WC: {wordcount}")
    print("---"*35)
    print(f"TAG: {tag} | WC: {wordcount} | ARTICLES: {len(article_id_list)} | ARTICLES REQUESTED: {str(results_counter)}")
    sys.exit(0)

if len(article_id_list) == 0:
    print("[-] No results")
    sys.exit(1)

# PHASE 2: Summarize & Get the TL;DR of every article and generate a "list of TLDRs"
TLDR_list = []
for raw_content in scraped_articles:
    # Obtain a list of summarized articles by GPT
    single_summary = summarize(raw_content, "tldr")
    TLDR_list.append(single_summary)

# PHASE 3: Merge the summarized articles into one, and send to GPT to generate the overall digest of information
raw_summaries = ""
for summary in TLDR_list:
    # Merge the summarized articles into one
    raw_summaries += summary + "\n"
    # Generate the final digest
final_digest = summarize(raw_summaries, "merge")

print(final_digest)

""" Useful for later: Archive after reading """
#archive_items(article_id_list)
