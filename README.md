# DataFlow

DataFlow is a Python CLI tool for API-to-Excel automation. It fetches users from
JSONPlaceholder, displays the number returned, and exports them using openpyxl.

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
timeout, checks the HTTP status, parses the JSON list, and saves `users.xlsx` in
the current directory:

```text
Fetched 10 users.
Exported users to users.xlsx.
```

The workbook contains ID, Name, Username, Email, Phone, Website, City, and Company.
City comes from `address.city`; Company comes from `company.name`. Headers are
bold and column widths fit the contents. Running the script again overwrites
`users.xlsx`. The generated file is ignored by Git.

Network, HTTP, invalid JSON, unexpected response format, and file-writing errors
produce a clear message and exit code 1. If writing fails, check that the directory
is writable and close the workbook if it is open in Excel. Successful execution
exits with code 0. Internet access is required for the API request.

## Tests

With the environment activated, run:

```sh
python -m unittest -v
```

The tests use mocked API data and a temporary workbook, so they do not need
internet access or overwrite `users.xlsx`.
