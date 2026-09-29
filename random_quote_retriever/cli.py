import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any

import requests
from platformdirs import user_cache_dir, user_data_dir, user_log_dir

APP_NAME = "random-quote-retriever"
API_URL = "https://zenquotes.io/api/random"

# Saved quotes are user data, the "last quote" is disposable cache, logs go in the log dir.
SAVED_QUOTES_FILE = Path(user_data_dir(APP_NAME)) / "quotes.json"
LAST_QUOTE_FILE = Path(user_cache_dir(APP_NAME)) / "last_quote.json"
LOG_FILE = Path(user_log_dir(APP_NAME)) / "logs.log"


def initialize_logging() -> None:
    """Initialize Logging"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=LOG_FILE,
        filemode="a",
    )


def initialize_argument_parser() -> argparse.Namespace:
    """Initialize the Argument Parser"""
    parser = argparse.ArgumentParser(description="finds a random quote")
    parser.add_argument("--save", action="store_true", help="save the quote to file")
    parser.add_argument("--view-saved", action="store_true", help="display saved quotes")
    return parser.parse_args()


def check_file_existence(file_path: Path) -> bool:
    """Check whether a file exists and if it is not empty"""
    return file_path.exists() and file_path.stat().st_size > 0


def load_from_json(file_path: Path) -> Any:
    """Load data from JSON file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_to_json(file_path: Path, data: Any) -> None:
    """Write data to JSON file (via a temp file so a crash can't corrupt it)"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = file_path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    os.replace(tmp_path, file_path)


def main() -> None:
    try:
        initialize_logging()
        args = initialize_argument_parser()
        save = args.save
        view = args.view_saved

        if not save and not view:
            response = requests.get(API_URL, timeout=10)
            if response.status_code == 200:
                logging.info(f"Data Retrieved Successfully {response.status_code}")
                data = response.json()
                raw_quote = data[0]["q"]
                author = data[0]["a"]
                print(f'"{raw_quote}"\n-{author}')

                write_to_json(LAST_QUOTE_FILE, {"author": author, "quote": raw_quote})
            else:
                logging.error(f"Data Not Retrieved {response.status_code}")
                print("Data Not Retrieved")
        if save:
            if check_file_existence(LAST_QUOTE_FILE):
                last_quote = load_from_json(LAST_QUOTE_FILE)
                if check_file_existence(SAVED_QUOTES_FILE):
                    data = load_from_json(SAVED_QUOTES_FILE)
                else:
                    data = []
                data.append(last_quote)
                write_to_json(SAVED_QUOTES_FILE, data)

                logging.info("Quote saved successfully")
                print("Quote Saved")
            else:
                logging.error("Error while saving: last quote was not found")
                print("Could not save quote as no quote was found.")
        if view:
            if check_file_existence(SAVED_QUOTES_FILE):
                for each in load_from_json(SAVED_QUOTES_FILE):
                    print(f'"{each["quote"]}" -{each["author"]}')
            else:
                print("No saved quotes yet.")
    except Exception as e:
        logging.error(f"Error Occurred: {e}")
        print("An error occurred while retrieving, please try again later.")


if __name__ == "__main__":
    main()
