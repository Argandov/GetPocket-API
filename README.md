# Weaver

![weaver_logo](images/banner.png)

Weaver is a Pocket API Wrapper that interacts with Pocket's API to retrieve Pocket posts from the past week, sorted by tags and providing detailed information regarding each post. Then, summarizes each post and prints a second global summary to stdout.

## Pocket Setup

Get a Consumer Key from a newly created Pocket App. You can do so by following the instructions [here](https://getpocket.com/developer/docs/authentication).

Use "authorizer.py" to get an **authorization** code (Authenticate your app).

## .env variables

This program uses environment variables to secure API keys. Before running, ensure that a .env file has been created with the following template:

```
POCKET_APP_NAME=<your-pocket-app-name>
POCKET_CONSUMER_KEY=<your-pocket-consumer-key>
POCKET_ACCESS_TOKEN=<your-pocket-access-token>
OPENAI_API_KEY=<your-openai-api-key>
```

Optional: If using Poetry, finish setup by running `sh setup.sh` to install the "alias" as `news` in the zshrc/bashrc file.

## Usage

After setting up, run the script by using:

```
python3 pocket_API_wrapper.py -h
```
This will list the available options:
- `--tag` - specify the tag to filter the posts
- `--list` - list all available tags (To be specified in `modules/tagging.py`)
- `--read` - To only display to stdout all the posts that have been saved, and do not process them further
- `--help` - list all available options

Example:

```
python3 app.py -t python -r
```

## Note

The program's `last_week_timestamp` function does not work anymore since Pocket's API does not respond to relative timestamps and ignores the "since" parameter.

## Contributions

Pull requests and issues are always welcome.
