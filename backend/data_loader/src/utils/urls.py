from urllib.parse import urlparse, urlunparse


def replace_netloc(url: str, new_scheme: str, new_domain: str) -> str:
    parsed = urlparse(url)
    new_url = urlunparse((
        new_scheme,
        new_domain,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return new_url


def get_url_parts_from_end(url: str, count: int) -> str:
    """
    Extracts the specified number of path segments from the end of a URL.

    Parameters:
        url (str): The URL string to extract parts from.
        count (int): The number of path segments to return from the end.

    Returns:
        str: A string containing the last `count` path segments joined by '/'.
             If `count` is greater than the total number of segments, returns all segments.

    Examples:
        url = "https://storage.googleapis.com/info-saas-static-eu/1/prod/audio/The_Open_Hand/The_Open_Hand_male_en.mp3"

        get_url_parts_from_end(url, 3)
        # Returns: "audio/The_Open_Hand/The_Open_Hand_male_en.mp3"

        get_url_parts_from_end(url, 5)
        # Returns: "1/prod/audio/The_Open_Hand/The_Open_Hand_male_en.mp3"

        get_url_parts_from_end(url, 10)
        # Returns: "info-saas-static-eu/1/prod/audio/The_Open_Hand/The_Open_Hand_male_en.mp3"
    """
    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split('/') if part]

    if count >= len(path_parts):
        selected_parts = path_parts
    else:
        selected_parts = path_parts[-count:]

    return '/'.join(selected_parts)
