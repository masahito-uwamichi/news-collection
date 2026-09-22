import os
import yaml
import json
from datetime import datetime

def load_sources():
    with open('feeds/sources.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)['sources']

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')

    articles_file = f"feeds/articles/{year}/{month}/{today}.md"

    if not os.path.exists(articles_file):
        print(f"No articles file found for today: {articles_file}")
        return

    # In a real scenario, we'd want to parse the articles.
    # Since fetch_rss.py writes a simple markdown list, we'll parse that.
    # However, for a more robust pipeline, I should have used JSON for raw articles.
    # Let's implement a simple parser for the current format.

    articles_by_category = {}

    with open(articles_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("- ["):
                # Simple parse: - [Title](Link) | Source | Category | Date
                try:
                    parts = line.split(' | ')
                    meta = parts[1].split(' | ') # Wait, the format is Source | Category | Date
                    # Let's adjust the fetch_rss.py format for easier parsing or just be careful here.
                    # Actually, let's re-read the line.
                    # line: "- [Title](Link) | Source | Category | Date"

                    # Title/Link are in the first part
                    content = parts[0].strip("- ")
                    source = parts[1].strip()
                    category = parts[2].strip()
                    date = parts[3].strip()

                    if category not in articles_by_category:
                        articles_by_category[category] = []

                    articles_by_category[category].append({
                        'title_link': content,
                        'source': source,
                        'date': date
                    })
                except Exception as e:
                    print(f"Error parsing line: {line}. Error: {e}")

    if not articles_by_category:
        print("No articles to generate digest for.")
        return

    digest_path = f"feeds/digests/{today}.md"
    with open(digest_path, 'w', encoding='utf-8') as f:
        f.write(f"---\ndate: {today}\n---\n\n")
        f.write(f"# RSS Digest - {today}\n\n")

        for category, articles in articles_by_category.items():
            f.write(f"## {category}\n\n")
            for art in articles:
                f.write(f"- {art['title_link']}\n")
                f.write(f"  - Source: {art['source']}\n")
                f.write(f"  - Published: {art['date']}\n")
            f.write("\n")

    print(f"Digest generated at {digest_path}")

if __name__ == "__main__":
    main()
