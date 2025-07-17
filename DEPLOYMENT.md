# Deployment Guide

This guide covers how to deploy Finanswer for public use.

## Backend Deployment

### Option 1: Heroku (Recommended for Free Tier)

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-finanswer-app
   ```

3. **Add Buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome
   ```

4. **Create Procfile**
   ```bash
   echo "web: gunicorn backend.server:app" > Procfile
   ```

5. **Update requirements.txt**
   ```bash
   echo "gunicorn==20.1.0" >> backend/requirements.txt
   ```

6. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Option 2: Railway

1. **Connect Repository**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub repository
   - Select the repository

2. **Configure Environment**
   - Set environment variables if needed
   - Railway will auto-detect Python

3. **Deploy**
   - Railway will automatically deploy on push

### Option 3: DigitalOcean App Platform

1. **Create App**
   - Go to DigitalOcean App Platform
   - Connect your GitHub repository
   - Select Python as the environment

2. **Configure**
   - Set build command: `pip install -r backend/requirements.txt`
   - Set run command: `gunicorn backend.server:app`

3. **Deploy**
   - DigitalOcean will handle the deployment

## Chrome Extension Deployment

### Publishing to Chrome Web Store

1. **Prepare Extension**
   ```bash
   # Create a production build
   cd extension
   # Ensure all files are ready
   ```

2. **Create ZIP File**
   ```bash
   zip -r finanswer-extension.zip . -x "*.DS_Store" "*.git*"
   ```

3. **Upload to Chrome Web Store**
   - Go to [Chrome Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Click "Add new item"
   - Upload the ZIP file
   - Fill in store listing details:
     - Description
     - Screenshots
     - Privacy policy
     - Terms of service

4. **Submit for Review**
   - Pay one-time developer registration fee ($5)
   - Submit for review (can take 1-3 days)

### Alternative: GitHub Releases

1. **Create Release**
   - Go to GitHub repository
   - Click "Releases" → "Create a new release"
   - Tag version (e.g., v1.0.0)
   - Upload extension ZIP file

2. **Update README**
   - Add installation instructions for manual download

## Environment Variables

### Production Settings

Create a `.env` file for production:

```env
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=https://your-domain.com
MODEL_PATH=/app/models/finbert
```

### Security Considerations

1. **HTTPS Only**
   - Ensure all connections use HTTPS
   - Update extension manifest for HTTPS URLs

2. **API Rate Limiting**
   - Implement rate limiting for API endpoints
   - Consider using Flask-Limiter

3. **CORS Configuration**
   - Restrict CORS to specific domains
   - Update extension host permissions

## Monitoring and Analytics

### Backend Monitoring

1. **Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

2. **Health Checks**
   - Implement `/health` endpoint
   - Set up uptime monitoring

3. **Performance Monitoring**
   - Use services like New Relic or DataDog
   - Monitor response times and errors

### Extension Analytics

1. **Usage Tracking**
   - Track extension usage (with user consent)
   - Monitor error rates

2. **Feedback Collection**
   - Store feedback data securely
   - Analyze for model improvements

## Scaling Considerations

### Backend Scaling

1. **Load Balancing**
   - Use multiple server instances
   - Implement load balancer

2. **Caching**
   - Cache model predictions
   - Use Redis for session storage

3. **Database**
   - Consider adding database for user data
   - Implement proper data backup

### Extension Updates

1. **Auto-Update**
   - Chrome Web Store handles updates
   - For manual distribution, implement update checks

2. **Version Management**
   - Use semantic versioning
   - Maintain changelog

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check CORS configuration
   - Verify extension permissions

2. **Model Loading**
   - Ensure model files are included
   - Check file paths

3. **Memory Issues**
   - Monitor memory usage
   - Consider model optimization

### Support

- Create GitHub issues for bugs
- Use discussions for questions
- Maintain documentation 