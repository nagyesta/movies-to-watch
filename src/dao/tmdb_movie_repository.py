from typing import Optional

from src.dao.movie_repository import MovieRepository
from src.dao.tmdb_http_client import TmdbHttpClient


class TmdbMovieRepository(MovieRepository):

    def __init__(self, tmdb_http_client: TmdbHttpClient) -> None:
        self.__client = tmdb_http_client

    def get_details_by_id(self, movie_id: int) -> dict:
        response = self.__client.get(
            path=f"/movie/{movie_id}", params={"language": "en-US"}, additional_headers={})
        return {
            "genres": response["genres"],
            "homepage": response["homepage"],
            "id": response["id"],
            "imdb_id": response["imdb_id"],
            "original_language": response["original_language"],
            "original_title": response["original_title"],
            "overview": response["overview"],
            "poster_path": response["poster_path"],
            "release_date": response["release_date"],
            "runtime": response["runtime"],
            "status": response["status"],
            "tagline": response["tagline"],
            "title": response["title"],
        }

    def get_trailer(self, movie_id: int) -> str:
        response = self.__client.get(
            path=f"/movie/{movie_id}/videos", params={"language": "en-US"}, additional_headers={})

        videos = response['results']
        return _find_best_trailer(videos)

    def get_watch_providers(self, movie_id: int) -> Optional[dict]:
        response = self.__client.get(
            path=f"/movie/{movie_id}/watch/providers", additional_headers={})
        return response['results']


def _find_best_trailer(videos):
    if len(videos) > 0:
        trailer = {}
        for vid in videos:
            if vid['type'] == "Trailer":
                if vid["official"]:
                    trailer = vid
                    break
                elif trailer == {}:
                    trailer = vid
        if trailer == {}:
            trailer = videos[0]
        url = f"https://www.youtube.com/watch?v={trailer['key']}"
    else:
        url = "No trailer data."
    return url
