"""Fetch users from a public API and export them to Excel."""

import sys

import requests
from openpyxl import Workbook
from openpyxl.styles import Font


USERS_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_FILE = "users.xlsx"


def export_users(users, filename):
    """Write one row per user, with a bold header and readable column widths."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Users"
    sheet.append(["ID", "Name", "Username", "Email", "Phone", "Website", "City", "Company"])

    for user in users:
        sheet.append([
            user.get("id"),
            user.get("name", ""),
            user.get("username", ""),
            user.get("email", ""),
            user.get("phone", ""),
            user.get("website", ""),
            user.get("address", {}).get("city", ""),
            user.get("company", {}).get("name", ""),
        ])

    for cell in sheet[1]:
        cell.font = Font(bold=True)

    for column in sheet.columns:
        width = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column)
        sheet.column_dimensions[column[0].column_letter].width = width + 2

    workbook.save(filename)


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
    try:
        export_users(users, OUTPUT_FILE)
    except OSError as error:
        print(f"Error: Could not write Excel file '{OUTPUT_FILE}': {error}", file=sys.stderr)
        return 1

    print(f"Exported users to {OUTPUT_FILE}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
