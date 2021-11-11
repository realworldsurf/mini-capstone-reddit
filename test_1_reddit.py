import requests
import time
from datetime import datetime, timezone

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"}

mock_keywords = {
    "art": ["pixel art", "image processing"],
    "env": ["virtualenv", "pyenv", "poetry"],
    "superlative": ["the best"],
}

muted_users = ["AutoModerator"]


def send_notification(title: str, body: str):
    print("--- Message ---")
    print("Title:", title)
    print(body)
    print("-" * 30)


def fetch_comment_data_periodically(subreddit: str, limit: int = 100):
    with open("read_comment_permalinks.txt", "a") as f:
        pass

    while True:
        with open("read_comment_permalinks.txt", "r") as f:
            read_comments = [l.rstrip() for l in f.read().split("\n")]
        comments = get_comments(subreddit, limit)
        for comment, body in comments:
            matches = scan_comment_for_keywords(body, comment, mock_keywords)
            if not matches:
                continue
            if comment["permalink"] in read_comments:
                continue
            if comment["author"] in muted_users:
                continue

            utc = datetime.utcfromtimestamp(
                comment["created_utc"]).replace(tzinfo=timezone.utc)
            local_time = utc.astimezone(tz=None)
            match_text = ", ".join([m["kind"] for m in matches])
            comment_text = "Author: " + comment["author"]
            comment_text += "\nPermalink: " + comment["permalink"]
            comment_text += "\nCreated: " + \
                local_time.strftime("%d %b, %H:%M:%S")
            comment_text += "\nBody: " + comment["body"]
            send_notification("Match for '%s'" % match_text, comment_text)
            read_comments.append(comment["permalink"])
            with open("read_comment_permalinks.txt", "a") as f:
                f.write(comment["permalink"] + "\n")
        time.sleep(60)


def get_comments(subreddit: str, limit: int = 100):
    res = requests.get("https://www.reddit.com/r/%s/comments.json?limit=%d" %
                    (subreddit, limit), headers=headers)

    comments = res.json()["data"]["children"]
    results = []
    for c in comments:
        comment = c["data"]
        results.append((comment, comment["body"]))
    return results


def scan_comment_for_keywords(comment: str, comment_obj: dict, keywords: dict):
    matches = []
    for k, phrases in keywords.items():
        for p in phrases:
            if p in comment.lower():
                matches.append({"kind": k, "comment": comment_obj})
                break
    return matches


if __name__ == "__main__":
    fetch_comment_data_periodically("python")