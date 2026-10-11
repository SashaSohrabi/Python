# pyright: strict
from pprint import pprint
from typing import TypedDict

import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response

URL: str = "https://news.ycombinator.com/newest"


class HNStory(TypedDict):
    title: str
    href: str
    points: int


def get_href(link: Tag) -> str:
    href = link.get("href")
    if not isinstance(href, str):
        raise TypeError("A story link must have a string href.")
    return href


def get_story_points(link: Tag) -> int:
    story_row = link.find_parent("tr")
    if story_row is None:
        return 0

    score_row = story_row.find_next_sibling("tr")
    if score_row is None:
        return 0

    score = score_row.select_one(".score")
    if score is None:
        return 0

    return int(score.get_text(strip=True).split()[0])


def sort_stories_by_points(hn_stories: list[HNStory]) -> list[HNStory]:
    return sorted(hn_stories, key=lambda k: k["points"], reverse=True)


def create_custom_hn(links: ResultSet[Tag], min_points: int) -> list[HNStory]:
    hn_stories: list[HNStory] = [
        HNStory(
            title=link.get_text(strip=True),
            href=get_href(link),
            points=points,
        )
        for link in links
        if (points := get_story_points(link)) >= min_points
    ]
    return sort_stories_by_points(hn_stories)


def main() -> None:
    res: Response = requests.get(URL, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    links: ResultSet[Tag] = soup.select(".titleline > a")
    pprint(create_custom_hn(links, min_points=10))


if __name__ == "__main__":
    main()
