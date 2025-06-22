"""
LangChain Tools for Jikan API (MyAnimeList unofficial API)
Provides tools for accessing anime, manga, character, and user information from MyAnimeList.
"""

from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from jikanpy import Jikan
import requests
import base64

# Initialize Jikan client
jikan = Jikan()
BASE_URL = "https://api.trace.moe"


@tool
def anime(
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
def anime_episode_by_id(anime_id: int, episode_id: int) -> Dict[str, Any]:
    """Gets specific episode information by anime ID and episode ID.

    Args:
        anime_id: ID of the anime
        episode_id: ID of the episode

    Returns:
        Dictionary containing episode information
    """
    return jikan.anime_episode_by_id(anime_id=anime_id, episode_id=episode_id)


@tool
def characters(id: int, extension: Optional[str] = None) -> Dict[str, Any]:
    """Gets information on a character by ID.

    Args:
        id: ID of the character
        extension: Special information to get (e.g., 'full', 'anime', 'manga')

    Returns:
        Dictionary containing character information
    """
    return jikan.characters(id=id, extension=extension)


@tool
def clubs(id: int, extension: Optional[str] = None) -> Dict[str, Any]:
    """Gets information on a club by ID.

    Args:
        id: ID of the club
        extension: Special information to get

    Returns:
        Dictionary containing club information
    """
    return jikan.clubs(id=id, extension=extension)


@tool
def genres(type: str, filter: Optional[str] = None) -> Dict[str, Any]:
    """Gets anime or manga genres.

    Args:
        type: Type to get genres for ('anime' or 'manga')
        filter: Filter genres by 'genres', 'explicit_genres', 'themes', or 'demographics'

    Returns:
        Dictionary containing genre information
    """
    return jikan.genres(type=type, filter=filter)


@tool
def manga(
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
def people(id: int, extension: Optional[str] = None) -> Dict[str, Any]:
    """Gets information on a person by ID.

    Args:
        id: ID of the person
        extension: Special information to get (e.g., 'full', 'anime', 'manga', 'voices')

    Returns:
        Dictionary containing person information
    """
    return jikan.people(id=id, extension=extension)


@tool
def producers(id: int, extension: Optional[str] = None) -> Dict[str, Any]:
    """Gets anime by producer/studio/licensor.

    Args:
        id: Producer ID from MyAnimeList
        extension: Special information to get (e.g., 'full', 'external')

    Returns:
        Dictionary containing producer information
    """
    return jikan.producers(id=id, extension=extension)


@tool
def random(type: str) -> Dict[str, Any]:
    """Gets a random resource of specified type.

    Args:
        type: Type of resource ('anime', 'manga', 'characters', 'people', 'users')

    Returns:
        Dictionary containing random resource information
    """
    return jikan.random(type=type)


@tool
def recommendations(type: str, page: Optional[int] = None) -> Dict[str, Any]:
    """Gets recommendations for anime or manga.

    Args:
        type: Type of recommendations ('anime' or 'manga')
        page: Page number of results

    Returns:
        Dictionary containing recommendations
    """
    return jikan.recommendations(type=type, page=page)


@tool
def reviews(type: str, page: Optional[int] = None) -> Dict[str, Any]:
    """Gets reviews for anime or manga.

    Args:
        type: Type of reviews ('anime' or 'manga')
        page: Page number of results

    Returns:
        Dictionary containing reviews
    """
    return jikan.reviews(type=type, page=page)


@tool
def schedules(
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
def search(
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
def season_history() -> Dict[str, Any]:
    """Gets all years and their respective season names from MyAnimeList.

    Returns:
        Dictionary containing all years and season names
    """
    return jikan.season_history()


@tool
def seasons(
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
def top(
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
def user_by_id(user_id: int) -> Dict[str, Any]:
    """Gets user information by MyAnimeList user ID.

    Args:
        user_id: MyAnimeList user ID

    Returns:
        Dictionary containing user information
    """
    return jikan.user_by_id(user_id=user_id)


@tool
def users(
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
def watch(
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
def search_by_image_url(
    url: str, anilist_info: bool = True, cut_borders: bool = True
) -> Dict[str, Any]:
    """Search for anime scene by image URL.

    Args:
        url: URL of the image to search
        anilist_info: Include AniList info in response (default: True)
        cut_borders: Automatically crop black borders (default: True)

    Returns:
        Dictionary containing search results with anime information
    """
    params = {
        "url": url,
        "anilistInfo": str(anilist_info).lower(),
        "cutBorders": str(cut_borders).lower(),
    }

    response = requests.get(f"{BASE_URL}/search", params=params)
    response.raise_for_status()
    return response.json()


@tool
def search_by_image_file(
    image_path: str, anilist_info: bool = True, cut_borders: bool = True
) -> Dict[str, Any]:
    """Search for anime scene by uploading an image file.

    Args:
        image_path: Path to the image file to search
        anilist_info: Include AniList info in response (default: True)
        cut_borders: Automatically crop black borders (default: True)

    Returns:
        Dictionary containing search results with anime information
    """
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    data = {"image": image_data, "anilistInfo": anilist_info, "cutBorders": cut_borders}

    response = requests.post(f"{BASE_URL}/search", json=data)
    response.raise_for_status()
    return response.json()


def get_all_jikan_tools() -> List:
    """Returns a list of all Jikan API tools.

    Returns:
        List of all available Jikan tools
    """
    return [
        anime,
        anime_episode_by_id,
        characters,
        clubs,
        genres,
        manga,
        people,
        producers,
        random,
        recommendations,
        reviews,
        schedules,
        search,
        season_history,
        seasons,
        top,
        user_by_id,
        users,
        watch,
        search_by_image_url,
        search_by_image_file,
    ]
