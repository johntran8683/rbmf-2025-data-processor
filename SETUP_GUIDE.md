# Setup Guide for RBMF Data Processor

This guide will help you set up and run the application using gdown (no API credentials required).

## Quick Start

### Step 1: Build and Run
```bash
# Build the Docker image
docker-compose build

# Download files from Google Drive (no credentials needed)
docker-compose run --rm rbmf-processor python -m src.main download

# Process downloaded files
docker-compose run --rm rbmf-processor python -m src.main process

# Run full pipeline (download + process)
docker-compose run --rm rbmf-processor python -m src.main run
```

That's it! The gdown method works without any API setup.

## Environment Configuration (Optional)

If you want to customize the default settings:

### Step 1: Copy Environment File
```bash
cp env.example .env
```

### Step 2: Update Environment Variables
Edit `.env` file with your settings:
```env
GOOGLE_DRIVE_FOLDER_URL=https://drive.google.com/drive/folders/1h2SfH2gCGlRAmV9REkqe-5sacDQ6IghC
LOG_LEVEL=INFO
DATA_DIR=/app/data
LOG_DIR=/app/logs
BATCH_SIZE=10
MAX_RETRIES=3
```

## Verify Setup

### Check Downloaded Files
```bash
ls -la data/
```

### Check Processing Report
```bash
cat data/processing_report.json
```

### Check Logs
```bash
tail -f logs/rbmf_processor.log
```

## Troubleshooting

### Common Issues

1. **"Access denied"**
   - Ensure you have access to the Google Drive folder
   - Check that the folder URL is correct

2. **Docker build fails**
   - Check your internet connection
   - Try: `docker system prune` and rebuild

3. **Download fails**
   - Make sure the Google Drive folder is publicly accessible or you have the correct permissions
   - Check the folder URL format

### Getting Help

- Check the logs in `logs/rbmf_processor.log`
- Make sure you have the correct folder permissions
- Verify the Google Drive folder URL is correct

## Next Steps

Once setup is complete, you can:
1. Modify the folder URL in `.env` to process different folders
2. Customize the data processing logic in `src/rbmf_processor/data_processor.py`
3. Add new file format support
4. Schedule regular downloads using cron or similar tools