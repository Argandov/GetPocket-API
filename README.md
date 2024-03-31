# Pocket-API-Wrapper-Python

Pocket API Wrapper is a Python script that interacts with Pocket's API to retrieve Pocket posts from the past week, sorted by tags and providing detailed information regarding each post.

## Pocket Setup

Get a Consumer Key from a newly created Pocket App. You can do so by following the instructions [here](https://getpocket.com/developer/docs/authentication).

Use "authorizer.py" to get an authorization code (Authenticate your app).

## .env variables

This program uses environment variables to secure API keys. Before running, ensure that a .env file has been created with the following template:

```
POCKET_APP_NAME=<your-pocket-app-name>
POCKET_CONSUMER_KEY=<your-pocket-consumer-key>
POCKET_ACCESS_TOKEN=<your-pocket-access-token>
```

## Usage

After setting up, run the script by using:

```
python3 pocket_API_wrapper.py
```
Use `--list` or `-l` to list available tags.

Use `--tag` or `-t` followed by a tag to specify a tag.

Example:

```
python3 pocket_API_wrapper.py --tag python
```

## Program Flow

1. The program starts by loading the .env variables and processing the command-line arguments.
2. The `get_last_posts` function is called which interacts with the Pocket API to get the last week’s posts.
3. It then parses the response and filters out the posts based on the tag provided by the user.
4. For each qualifying post, an information summary is printed which includes time added, id, status of the article, word count, language of the article, title, excerpt, and URL.
5. Total word count and count of articles are printed at the end.

## Note

The program's `last_week_timestamp` function does not work anymore since Pocket's API does not respond to relative timestamps and ignores the "since" parameter.

## Contributions

Pull requests and issues are always welcome.
