#!/bin/bash

# Backup script for Finanswer model files
# This script creates a backup of the model files outside the git repository

BACKUP_DIR="$HOME/finanswer_backup"
MODEL_DIR="../models/finbert"
DATE=$(date +"%Y%m%d_%H%M%S")

echo "Creating backup of Finanswer model files..."
echo "Backup location: $BACKUP_DIR"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create timestamped backup
BACKUP_PATH="$BACKUP_DIR/finbert_$DATE"
echo "Creating backup at: $BACKUP_PATH"

# Copy model files
cp -r "$MODEL_DIR" "$BACKUP_PATH"

# Verify backup
if [ -f "$BACKUP_PATH/tf_model.h5" ]; then
    echo "✅ Backup created successfully!"
    echo "Backup size: $(du -sh "$BACKUP_PATH" | cut -f1)"
    echo "Files backed up:"
    ls -la "$BACKUP_PATH"
else
    echo "❌ Backup failed!"
    exit 1
fi

# Keep only the 3 most recent backups
echo "Cleaning up old backups (keeping 3 most recent)..."
cd "$BACKUP_DIR"
ls -t finbert_* | tail -n +4 | xargs -r rm -rf

echo "Backup complete! 🎉" 