# grailradar-scrapers
Python-based web scrapers for GrailRadar. Aggregates live auction listings via ScraperAPI and normalises data for ingestion into Typesense.
## Project Structure

- `scrapers/`
  Site-specific scrapers (one file per auctioneer).

- `core/`
  Shared logic for normalisation, validation, date handling, and utilities.

- `config/`
  Runtime configuration (API keys, endpoints). Not committed to git.

- `scripts/`
  Entry points to run scrapers manually or via cron/GitHub Actions.
