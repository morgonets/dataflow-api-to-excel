# DataFlow

DataFlow is a Python CLI tool for API-to-Excel automation. This first milestone
fetches users from JSONPlaceholder and displays the number returned.

## Setup and execution

Use Python 3.9 or newer. From the repository directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python dataflow.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

The script requests `https://jsonplaceholder.typicode.com/users` with a 10-second
timeout, checks the HTTP status, parses the JSON list, and prints its length:

```text
Fetched 10 users.
```

Network, HTTP, invalid JSON, and unexpected response format errors produce a clear
message and exit code 1. Successful execution exits with code 0. Internet access
is required. Excel export is not included in this milestone.
