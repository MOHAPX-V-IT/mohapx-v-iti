"""Refresh public GitHub data. No token, private data, or third-party proxy.

Run: python build/update_github.py. A failed refresh leaves the last snapshot intact.
"""
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import urllib.request

USERNAME = "MOHAPX-V-IT"
ROOT = Path(__file__).resolve().parents[1]


def get(url):
    request = urllib.request.Request(url, headers={
        "User-Agent": "MOHAPX-portfolio-public-stats",
        "Accept": "application/vnd.github+json" if "api.github.com" in url else "text/html",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tooltips = {}
        self.target = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "td" and "data-date" in a:
            self.cells[a["id"]] = {"date": a["data-date"], "level": int(a["data-level"])}
        if tag == "tool-tip":
            self.target = a.get("for")

    def handle_data(self, text):
        if self.target:
            self.tooltips[self.target] = self.tooltips.get(self.target, "") + text

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self.target = None

    def days(self):
        result = []
        for key, cell in self.cells.items():
            text = self.tooltips.get(key, "").strip()
            match = re.match(r"([\d,]+) contributions? on", text)
            if text.startswith("No contributions"):
                count = 0
            elif match:
                count = int(match[1].replace(",", ""))
            else:
                raise ValueError(f"Unrecognised GitHub calendar label: {text!r}")
            result.append({**cell, "count": count})
        result.sort(key=lambda day: day["date"])
        if not 350 <= len(result) <= 371:
            raise ValueError("GitHub calendar markup changed; keeping previous snapshot")
        return result


def main():
    profile = json.loads(get(f"https://api.github.com/users/{USERNAME}"))
    repositories = []
    page = 1
    while True:
        batch = json.loads(get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}"))
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    calendar = Calendar()
    calendar.feed(get(f"https://github.com/users/{USERNAME}/contributions"))
    days = calendar.days()
    owned = [repo for repo in repositories if not repo["fork"]]
    snapshot = {
        "username": profile["login"],
        "profileUrl": profile["html_url"],
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "publicRepos": profile["public_repos"],
        "followers": profile["followers"],
        "stars": sum(repo["stargazers_count"] for repo in owned),
        "contributions": sum(day["count"] for day in days),
        "days": days,
        "repositories": [{"name": repo["name"], "url": repo["html_url"],
                          "description": repo["description"], "language": repo["language"],
                          "stars": repo["stargazers_count"]} for repo in owned],
    }
    target = ROOT / "assets" / "github-stats.json"
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)
    print(f"Updated @{USERNAME}: {len(days)} days, {snapshot['contributions']} contributions, {len(repositories)} public repositories")


if __name__ == "__main__":
    main()
