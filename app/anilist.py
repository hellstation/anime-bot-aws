import requests

ANILIST_URL = "https://graphql.anilist.co"

AIRING_QUERY = """
query ($page: Int) {
  Page(page: $page, perPage: 5) {
    media(type: ANIME, status: RELEASING, sort: POPULARITY_DESC) {
      id
      title { romaji }
      nextAiringEpisode { episode airingAt }
    }
  }
}
"""

SEARCH_QUERY = """
query ($search: String) {
  Media(search: $search, type: ANIME) {
    id
    title { romaji english }
    description episodes status season seasonYear genres averageScore
    nextAiringEpisode { episode airingAt }
  }
}
"""

def get_airing_anime():
    response = requests.post(ANILIST_URL, json={"query": AIRING_QUERY, "variables": {"page": 1}}, timeout=10)
    response.raise_for_status()
    return response.json()["data"]["Page"]["media"]

def search_anime(name: str):
    response = requests.post(ANILIST_URL, json={"query": SEARCH_QUERY, "variables": {"search": name}}, timeout=10)
    response.raise_for_status()
    return response.json()["data"]["Media"]
