import feedparser
import yaml
import json
import os
from datetime import datetime

def load_sources():
    with open('feeds/sources.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)['sources']

def load_seen():
    state_file = 'feeds/state/seen.json'
    if os.path.exists(state_file):
        with open(state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_seen(seen):
    state_file = 'feeds/state/seen.json'
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(seen, f, indent=2, ensure_ascii=False)

def main():
    sources = load_sources()
    seen = load_seen()

    today = datetime.now().strftime('%Y-%m-%d')
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')

    articles_dir = f"feeds/articles/{year}/{month}"
    os.makedirs(articles_dir, exist_ok=True)
    articles_file = f"{articles_dir}/{today}.md"

    new_articles = []

    for source in sources:
        print(f"Fetching {source['name']}...")
        feed = feedparser.parse(source['url'])

        for entry in feed.entries:
            guid = entry.get('id') or entry.get('link')
            if guid in seen:
                continue

            article = {
                'title': entry.get('title', 'No Title'),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'source': source['name'],
                'category': source['category'],
                'tags': source.get('tags', []),
                'guid': guid
            }
            new_articles.append(article)
            seen[guid] = today

    if new_articles:
        with open(articles_file, 'w', encoding='utf-8') as f:
            # We save as a simple JSON list in the raw articles file for easier parsing by generate_digest.py
            # Although README says .md, using JSON for raw storage makes the pipeline robust.
            # Let's actually use a simple markdown list for visibility.
            f.write(f"# Articles fetched on {today}\n\n")
            for art in new_articles:
                f.write(f"- [{art['title']}]({art['link']}) | {art['source']} | {art['category']} | {art['published']}\n")

        save_seen(seen)
        print(f"Saved {len(new_articles)} new articles to {articles_file}")
    else:
        print("No new articles found.")

if __name__ == "__main__":
    main()
