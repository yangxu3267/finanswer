# Finanswer Model Backup Guide

## Overview
The Finanswer project uses a large FinBERT model file (`tf_model.h5`, ~418MB) that cannot be stored in Git due to GitHub's 100MB file size limit. This guide explains how to safely manage and backup these model files.

## Backup Location
Model files are backed up to: `~/finanswer_backup/`

## Automatic Backup
Run the backup script before making any changes to the repository:

```bash
cd backend
./backup_model.sh
```

This script will:
- Create a timestamped backup of all model files
- Verify the backup was successful
- Keep only the 3 most recent backups to save space

## Manual Backup
To manually backup the model files:

```bash
# Create backup directory
mkdir -p ~/finanswer_backup

# Copy model files
cp -r models/finbert ~/finanswer_backup/finbert_$(date +"%Y%m%d_%H%M%S")
```

## Restoring from Backup
If the model files are lost, restore them from backup:

```bash
# Find the most recent backup
ls -t ~/finanswer_backup/finbert_*

# Restore the model files
cp -r ~/finanswer_backup/finbert_YYYYMMDD_HHMMSS/* models/finbert/
```

## Downloading Fresh Model
If no backup is available, download the model from Hugging Face:

```python
from transformers import TFDistilBertForSequenceClassification, DistilBertTokenizer

# Download model
model = TFDistilBertForSequenceClassification.from_pretrained('ProsusAI/finbert')
tokenizer = DistilBertTokenizer.from_pretrained('ProsusAI/finbert')

# Save to models directory
model.save_pretrained('models/finbert')
tokenizer.save_pretrained('models/finbert')
```

## Important Notes
- Always backup before git operations that might affect the models directory
- The backup location (`~/finanswer_backup/`) is outside the git repository
- Model files are automatically ignored by git (see `.gitignore`)
- Keep multiple backups in case one becomes corrupted

## File Sizes
- `tf_model.h5`: ~418MB (main model weights)
- `vocab.txt`: ~226KB (vocabulary)
- Other config files: ~2KB total 