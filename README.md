# CLI Random Quote Retriever
## By mhaxanali
## PyPI Project Link
https://pypi.org/project/random-quote-retriever/
## What it does?
- Uses `zenquotes.io/api` to retrieve a random quote. Can optionally save the quote.
- API handling using `requests` and argument parsing using `argparse`
## Setting up
- Download the project:
    ```bash
    python3 -m pip install random-quote-retriever
    ```
## Where quotes are stored
Saved quotes go to your user data folder (e.g. `~/.local/share/random-quote-retriever/quotes.json`
on Linux, `%LOCALAPPDATA%\random-quote-retriever\...` on Windows).

Quotes provided by [ZenQuotes.io](https://zenquotes.io).
## Usage
### Retrieving Quotes
Run the script using (retrieve a random quote):
```bash
quote
```
### Saving Quotes
Run the script with --save:
```
quote --save
```
The last quote that was retrieved will be saved in the quotes file
### Viewing Saved Quotes
Run the script with --view-saved:
```
quote --view-saved
```
All of the quotes that have been saved will be displayed.
