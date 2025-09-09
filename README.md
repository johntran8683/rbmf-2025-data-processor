# RBMF Data Processor

A Python application for downloading and processing data from Google Drive folders, specifically designed for RBMF (Result-Based Management Framework) data processing.

## Features

- **Google Drive Integration**: Download files from Google Drive folders using gdown (no API key required)
- **Data Processing**: Process Excel, CSV, and JSON files with detailed analysis
- **Docker Support**: Run the application in a containerized environment
- **Comprehensive Logging**: Detailed logging with file rotation
- **CLI Interface**: Easy-to-use command-line interface
- **Error Handling**: Robust error handling and retry mechanisms

## Prerequisites

1. **Docker**: Docker and Docker Compose installed on your system
2. **Access to Google Drive folder**: You need access to the Google Drive folder you want to download

## Setup

### 1. Environment Configuration (Optional)

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Update the `.env` file with your configuration:
   ```env
   GOOGLE_DRIVE_FOLDER_URL=https://drive.google.com/drive/folders/1h2SfH2gCGlRAmV9REkqe-5sacDQ6IghC
   LOG_LEVEL=INFO
   ```

### 2. Build and Run with Docker

```bash
# Build the Docker image
docker-compose build

# Run the application
docker-compose up

# Or run specific commands
docker-compose run --rm rbmf-processor python -m src.main download
docker-compose run --rm rbmf-processor python -m src.main process
docker-compose run --rm rbmf-processor python -m src.main run
```

## Usage

### Command Line Interface

The application provides several commands:

#### Download Files
```bash
python -m src.main download --folder-url https://drive.google.com/drive/folders/1h2SfH2gCGlRAmV9REkqe-5sacDQ6IghC --output-dir ./data
```

#### Process Downloaded Files
```bash
python -m src.main process --data-dir ./data --output-file ./processing_report.json
```

#### Run Full Pipeline
```bash
python -m src.main run --folder-url https://drive.google.com/drive/folders/1h2SfH2gCGlRAmV9REkqe-5sacDQ6IghC --output-dir ./data
```

### Docker Commands

```bash
# Download files
docker-compose run --rm rbmf-processor python -m src.main download

# Process files
docker-compose run --rm rbmf-processor python -m src.main process

# Run full pipeline
docker-compose run --rm rbmf-processor python -m src.main run
```

## Project Structure

```
rbmf-2025-data-processor/
├── src/
│   ├── rbmf_processor/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── drive_client.py    # Google Drive API client
│   │   └── data_processor.py  # Data processing utilities
│   └── main.py                # Main application entry point
├── tests/                     # Test files
├── docs/                      # Documentation
├── data/                      # Downloaded data (created at runtime)
├── logs/                      # Application logs (created at runtime)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── env.example               # Environment variables example
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Configuration

The application uses environment variables for configuration. See `env.example` for all available options:

- `GOOGLE_DRIVE_FOLDER_ID`: The ID of the Google Drive folder to download
- `GOOGLE_CREDENTIALS_FILE`: Path to the Google API credentials JSON file
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `DATA_DIR`: Directory for downloaded data
- `BATCH_SIZE`: Number of files to process in parallel
- `MAX_RETRIES`: Maximum number of retry attempts for failed operations

## Data Processing

The application can process the following file types:

- **Excel files** (.xlsx, .xls): Analyzes all sheets, columns, data types, and null values
- **CSV files** (.csv): Analyzes structure, data types, and null values
- **JSON files** (.json): Analyzes structure and content

## Output

The application generates:

1. **Downloaded files**: All files from the Google Drive folder
2. **Download summary**: JSON file with download statistics
3. **Processing report**: Detailed analysis of all processed files
4. **Logs**: Comprehensive application logs

## Troubleshooting

### Common Issues

1. **Authentication Error**: Make sure `credentials.json` is in the project root and contains valid credentials
2. **Permission Denied**: Ensure the service account has access to the Google Drive folder
3. **File Not Found**: Check that the folder ID is correct and accessible

### Logs

Check the logs in the `logs/` directory for detailed error information:
```bash
tail -f logs/rbmf_processor.log
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Code Style

The project follows Python best practices:
- Type hints
- Docstrings
- Error handling
- Logging
- Configuration management

## License

This project is licensed under the MIT License.
