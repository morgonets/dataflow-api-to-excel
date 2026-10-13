"""Fetch users from a public API and display how many were returned."""

import sys

import requests


USERS_URL = "https://jsonplaceholder.typicode.com/users"


def main():
    try:
        response = requests.get(USERS_URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Error: The API request timed out after 10 seconds.", file=sys.stderr)
        return 1
    except requests.exceptions.HTTPError as error:
        print(f"Error: The API returned HTTP {error.response.status_code}.", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as error:
        print(f"Error: Could not fetch users: {error}", file=sys.stderr)
        return 1

    try:
        users = response.json()
    except ValueError:
        print("Error: The API response is not valid JSON.", file=sys.stderr)
        return 1

    if not isinstance(users, list):
        print("Error: Expected a JSON list of users from the API.", file=sys.stderr)
        return 1

    print(f"Fetched {len(users)} users.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
