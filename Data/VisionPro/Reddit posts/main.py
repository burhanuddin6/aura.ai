import re
import praw
import json

# 🔑 Replace with your Reddit API Credentials
reddit = praw.Reddit(
    client_id="E6oizyNmoxoQbq8MPh8G8A",
    client_secret="OkFbw0L0lB5LCwiD6CRO7aFJX1K0jQ",
    user_agent="my-reddit-scraper/1.0"
)

def get_post_id(url):
    """Extracts the post ID from a full Reddit URL."""
    match = re.search(r"comments/([a-zA-Z0-9]+)/", url)
    return match.group(1) if match else None

def get_reddit_data(post_links):
    all_posts = []
    
    for url in post_links:
        post_id = get_post_id(url)
        if not post_id:
            print(f"❌ Invalid URL: {url}")
            continue
        
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)  # Load all comments

        post_data = {
            "link": url,
            "title": submission.title,
            "selftext": submission.selftext,
            "comments": [{"author": c.author.name if c.author else "Deleted", "text": c.body} for c in submission.comments]
        }
        all_posts.append(post_data)
    
    return all_posts

# Reddit Post Links
post_links = [
    "https://www.reddit.com/r/VisionPro/comments/1b5j7u6/i_made_an_app_that_lets_you_see_the_matrix/",
    "https://www.reddit.com/r/VisionPro/comments/1ai37t7/working_in_the_vision_pro/",
    "https://www.reddit.com/r/VisionPro/comments/1b25jmr/had_an_app_idea_this_weekend_its_a_virtual_window/",
    "https://www.reddit.com/r/VisionPro/comments/1ahhdnj/vision_pros_spatial_understanding_is_insane/"
]

# Fetch data and save as JSON
reddit_data = get_reddit_data(post_links)

with open("reddit_comments.json", "w", encoding="utf-8") as f:
    json.dump(reddit_data, f, indent=4, ensure_ascii=False)

print("✅ Data saved to 'reddit_comments.json'")
