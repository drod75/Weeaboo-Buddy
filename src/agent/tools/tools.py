"""
LangChain Tools for Jikan API (MyAnimeList unofficial API), and Trace Moe API (Image Scene Tracing)
Provides tools for accessing anime, manga, character, and user information from MyAnimeList, and scene locater tools.
"""

from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from jikanpy import Jikan
import requests
import json

# Initialize Jikan client
jikan = Jikan()
trace_moe = "https://api.trace.moe"


@tool
def jikan_anime(
    id: int, extension: Optional[str] = None, page: Optional[int] = None
) -> Dict[str, Any]:
    """Gets information on an anime by ID.

    Args:
        id: ID of the anime to get information of
        extension: Special information to get (e.g., 'episodes', 'news', 'characters')
        page: Page number of results (for paginated extensions)

    Returns:
        Dictionary containing anime information
    """
    return jikan.anime(id=id, extension=extension, page=page)


@tool
def jikan_anime_episode_by_id(anime_id: int, episode_id: int) -> Dict[str, Any]:
    """Gets specific episode information by anime ID and episode ID.

    Args:
        anime_id: ID of the anime
        episode_id: ID of the episode

    Returns:
        Dictionary containing episode information
    """
    return jikan.anime_episode_by_id(anime_id=anime_id, episode_id=episode_id)


@tool
def jikan_characters(id: int, extension: Optional[str] = None) -> Dict[str, Any]:
    """Gets information on a character by ID.

    Args:
        id: ID of the character
        extension: Special information to get (e.g., 'full', 'anime', 'manga')

    Returns:
        Dictionary containing character information
    """
    return jikan.characters(id=id, extension=extension)


@tool
def jikan_clubs(id: int, extension: Optional[str] = None) -> Dict[str, Any]:
    """Gets information on a club by ID.

    Args:
        id: ID of the club
        extension: Special information to get

    Returns:
        Dictionary containing club information
    """
    return jikan.clubs(id=id, extension=extension)


@tool
def jikan_genres(type: str, filter: Optional[str] = None) -> Dict[str, Any]:
    """Gets anime or manga genres.

    Args:
        type: Type to get genres for ('anime' or 'manga')
        filter: Filter genres by 'genres', 'explicit_genres', 'themes', or 'demographics'

    Returns:
        Dictionary containing genre information
    """
    return jikan.genres(type=type, filter=filter)


@tool
def jikan_manga(
    id: int, extension: Optional[str] = None, page: Optional[int] = None
) -> Dict[str, Any]:
    """Gets information on a manga by ID.

    Args:
        id: ID of the manga
        extension: Special information to get (e.g., 'characters', 'news', 'reviews')
        page: Page number of results (for paginated extensions)

    Returns:
        Dictionary containing manga information
    """
    return jikan.manga(id=id, extension=extension, page=page)


@tool
def jikan_people(id: int, extension: Optional[str] = None) -> Dict[str, Any]:
    """Gets information on a person by ID.

    Args:
        id: ID of the person
        extension: Special information to get (e.g., 'full', 'anime', 'manga', 'voices')

    Returns:
        Dictionary containing person information
    """
    return jikan.people(id=id, extension=extension)


@tool
def jikan_producers(id: int, extension: Optional[str] = None) -> Dict[str, Any]:
    """Gets anime by producer/studio/licensor.

    Args:
        id: Producer ID from MyAnimeList
        extension: Special information to get (e.g., 'full', 'external')

    Returns:
        Dictionary containing producer information
    """
    return jikan.producers(id=id, extension=extension)


@tool
def jikan_random(type: str) -> Dict[str, Any]:
    """Gets a random resource of specified type.

    Args:
        type: Type of resource ('anime', 'manga', 'characters', 'people', 'users')

    Returns:
        Dictionary containing random resource information
    """
    return jikan.random(type=type)


@tool
def jikan_recommendations(type: str, page: Optional[int] = None) -> Dict[str, Any]:
    """Gets recommendations for anime or manga.

    Args:
        type: Type of recommendations ('anime' or 'manga')
        page: Page number of results

    Returns:
        Dictionary containing recommendations
    """
    return jikan.recommendations(type=type, page=page)


@tool
def jikan_reviews(type: str, page: Optional[int] = None) -> Dict[str, Any]:
    """Gets reviews for anime or manga.

    Args:
        type: Type of reviews ('anime' or 'manga')
        page: Page number of results

    Returns:
        Dictionary containing reviews
    """
    return jikan.reviews(type=type, page=page)


@tool
def jikan_schedules(
    day: Optional[str] = None,
    page: Optional[int] = None,
    parameters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Gets anime schedule information.

    Args:
        day: Day of the week ('monday', 'tuesday', etc.)
        page: Page number of results
        parameters: Additional query parameters

    Returns:
        Dictionary containing scheduled anime
    """
    return jikan.schedules(day=day, page=page, parameters=parameters)


@tool
def jikan_search(
    search_type: str,
    query: str,
    page: Optional[int] = None,
    parameters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Searches MyAnimeList for content.

    Args:
        search_type: Where to search ('anime', 'manga', 'characters', 'people', 'users', 'clubs', 'producers')
        query: Search query string
        page: Page number of results
        parameters: Additional search parameters (filters, sorting, etc.)

    Returns:
        Dictionary containing search results
    """
    return jikan.search(
        search_type=search_type, query=query, page=page, parameters=parameters
    )


@tool
def jikan_season_history() -> Dict[str, Any]:
    """Gets all years and their respective season names from MyAnimeList.

    Returns:
        Dictionary containing all years and season names
    """
    return jikan.season_history()


@tool
def jikan_seasons(
    year: Optional[int] = None,
    season: Optional[str] = None,
    extension: Optional[str] = None,
    page: Optional[int] = None,
    parameters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Gets anime from a specific season or current season.

    Args:
        year: Year to get anime from
        season: Season name ('winter', 'spring', 'summer', 'fall')
        extension: Special information ('now', 'upcoming')
        page: Page number of results
        parameters: Additional query parameters

    Returns:
        Dictionary containing seasonal anime information
    """
    return jikan.seasons(
        year=year, season=season, extension=extension, page=page, parameters=parameters
    )


@tool
def jikan_top(
    type: str, page: Optional[int] = None, parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Gets top items from MyAnimeList.

    Args:
        type: Type of top items ('anime', 'manga', 'people', 'characters', 'reviews')
        page: Page number of results
        parameters: Additional query parameters (filters, subtype, etc.)

    Returns:
        Dictionary containing top items
    """
    return jikan.top(type=type, page=page, parameters=parameters)


@tool
def jikan_user_by_id(user_id: int) -> Dict[str, Any]:
    """Gets user information by MyAnimeList user ID.

    Args:
        user_id: MyAnimeList user ID

    Returns:
        Dictionary containing user information
    """
    return jikan.user_by_id(user_id=user_id)


@tool
def jikan_users(
    username: str,
    extension: Optional[str] = None,
    page: Optional[int] = None,
    parameters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Gets information about a user by username.

    Args:
        username: MyAnimeList username
        extension: Special information ('full', 'statistics', 'favorites', 'userupdates', 'about', 'history', 'friends', 'animelist', 'mangalist', 'reviews', 'recommendations', 'clubs', 'external')
        page: Page number of results (for paginated extensions)
        parameters: Additional query parameters

    Returns:
        Dictionary containing user information
    """
    return jikan.users(
        username=username, extension=extension, page=page, parameters=parameters
    )


@tool
def jikan_watch(
    extension: str, parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Gets information about recent/popular episodes or promotional videos.

    Args:
        extension: Type of watch content ('episodes', 'episodes/popular', 'promos', 'promos/popular')
        parameters: Additional query parameters (limit, etc.)

    Returns:
        Dictionary containing watch information
    """
    return jikan.watch(extension=extension, parameters=parameters)


@tool
def trace_moe_search(
    path: str,
    is_url: bool = False,
    upload_file: bool = False,
    cut_black_borders: bool = True,
    include_anilist_info: bool = True,
) -> str:
    """
    Searches for an anime scene using an image URL or a base64 encoded string.
    This tool is adapted from the user-provided code snippet.

    Args:
        path: Image URL or base64 encoded image string.
        is_url: Set to True if the path is a URL.
        upload_file: This parameter is not used as the image data is handled directly as a base64 string.
        cut_black_borders: Automatically crops black borders from the image.
        include_anilist_info: Includes additional anime information from AniList.

    Returns:
        A JSON string containing the search results or a descriptive error message.
    """
    url = "https://api.trace.moe/search"
    params = {}

    if cut_black_borders:
        params["cutBorders"] = ""
    if include_anilist_info:
        params["anilistInfo"] = ""

    if is_url:
        params["url"] = path
        response = requests.get(url, params=params)
    else:
        f = open(path, "rb")
        response = requests.post(url, files={"image": f}, params=params)

    response.raise_for_status()
    data = response.json()
    result = data.get("result", [])
    return json.dumps(result)


def get_all_tools() -> List:
    """Returns a list of all API tools.

    Returns:
        List of all available tools
    """
    return [
        jikan_anime,
        jikan_anime_episode_by_id,
        jikan_characters,
        jikan_clubs,
        jikan_genres,
        jikan_manga,
        jikan_people,
        jikan_producers,
        jikan_random,
        jikan_recommendations,
        jikan_reviews,
        jikan_schedules,
        jikan_search,
        jikan_season_history,
        jikan_seasons,
        jikan_top,
        jikan_user_by_id,
        jikan_users,
        jikan_watch,
        # trace_moe_search,
    ]
