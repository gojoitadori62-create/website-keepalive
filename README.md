# GitHub Actions Web Scraper

This project sets up a web scraper that runs every 5 minutes using GitHub Actions.

## Setup

1. **Fork this repository** to your GitHub account
2. **Clone your forked repository** locally
3. **Customize the scraper**:
   - Modify `scraper.py` to target your desired website
   - Update the selectors in the `scrape_website()` function to extract the data you need

## How It Works

- The scraper runs every 5 minutes using GitHub Actions
- Results are saved in the `results/` directory with timestamps
- The workflow automatically commits and pushes new results to the repository

## Customization

1. **Change the schedule**:
   Edit the cron schedule in `.github/workflows/scraper.yml`
   
2. **Add environment variables**:
   - Create a `.env` file for local development
   - Add secrets in GitHub repository settings (Settings > Secrets and variables > Actions) for production

3. **Modify the scraping logic**:
   - Update the `scrape_website()` function in `scraper.py`
   - Add error handling as needed

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the scraper locally:
   ```bash
   python scraper.py
   ```

## License

MIT
