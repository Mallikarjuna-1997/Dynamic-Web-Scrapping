# Dynamic-Web-Scrapping Maynooth University Publications Scraper

This Python script scrapes publication data from the Maynooth University website for a specific department and saves the results to a CSV and Excel file.

## Features

- Scrapes publication data from multiple pages of the Maynooth University website
- Extracts publication type, year, and detail for each publication
- Saves the results to a CSV and Excel file
- Handles exceptions and logs errors
- Removes illegal characters for Excel compatibility

## Requirements

- Python 3.x
- Selenium
- pandas
- csv
- os
- re
- time
- logging

## Usage

1. Install the required dependencies:
   ```
   pip install selenium pandas
   ```

2. Download the Microsoft Edge WebDriver from the official website and update the `executable_path` in the `setup_browser()` function.

3. Run the script:
   ```
   python script.py
   ```

4. The script will open the Maynooth University website, scrape the publication data, and save the results to `publications.csv` and `publications.xlsx` in the current directory.

## Logging

The script uses the `logging` module to log information and errors. The log messages are printed to the console with the following format:

```
%(asctime)s - %(levelname)s - %(message)s
```

## Limitations

- The script assumes there are 6 pages of publication data. You may need to modify the loop if there are more or fewer pages.
- The script only scrapes publication data from the "Publications" tab of each person's profile. It does not handle other types of publications or data.

