# Vercel Deployment Guide

## 🚀 Deploying to Vercel

### Prerequisites
1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Supabase Database**: Create a PostgreSQL database at [supabase.com](https://supabase.com)
3. **GitHub Repository**: Code should be in a GitHub repository

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Set up Environment Variables

In your Vercel project dashboard, add these environment variables:

#### Required Environment Variables:
- `DATABASE_URL` - Your Supabase PostgreSQL connection string
  ```
  postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
  ```
- `FLASK_CONFIG` - Set to `production`
- `SECRET_KEY` - Generate a secure random string
- `OPENAI_API_KEY` - Your OpenAI API key (for AI features)
- `GITHUB_TOKEN` - Your GitHub token (for AI API access)
3. **Vercel Account**: Sign up at https://vercel.com

## Environment Variables

Configure these environment variables in your Vercel dashboard:

### Required Variables:
```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

# AI/LLM Configuration  
GITHUB_TOKEN=github_pat_[YOUR-GITHUB-TOKEN]

# Flask Configuration
FLASK_CONFIG=production
SECRET_KEY=your-production-secret-key-here
```

### How to get DATABASE_URL from Supabase:
1. Go to your Supabase project dashboard
2. Navigate to Settings > Database
3. Copy the Connection String (URI format)
4. Replace `[YOUR-PASSWORD]` with your actual database password

### How to get GITHUB_TOKEN:
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with appropriate permissions
3. Copy the token (starts with `github_pat_`)

## Deployment Steps

1. **Push code to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to https://vercel.com/dashboard
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration from `vercel.json`

3. **Set Environment Variables**:
   - In Vercel dashboard, go to your project
   - Navigate to Settings > Environment Variables
   - Add all the required variables listed above

4. **Deploy**:
   - Vercel will automatically deploy when you push to the main branch
   - First deployment may take 2-3 minutes

## File Structure for Vercel

```
note-taking-app/
├── api/                    # Serverless functions
│   ├── index.py           # Main API entry point
│   ├── notes.py           # Notes API endpoints
│   └── users.py           # Users API endpoints
├── public/                 # Static files served by Vercel
│   └── index.html         # Frontend application
├── src/                    # Source code (shared between local and Vercel)
│   ├── config.py          # Database configuration
│   ├── main.py            # Flask app factory
│   ├── llm.py             # AI/LLM functions
│   ├── models/            # Database models
│   └── routes/            # API routes
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
└── .env                   # Local environment variables (not deployed)
```

## Testing Deployment

After deployment, test these endpoints:

1. **Frontend**: `https://your-app.vercel.app/`
2. **API Health**: `https://your-app.vercel.app/api/notes`
3. **Features**:
   - Create/edit notes
   - Drag and drop reordering
   - Translation functionality
   - Smart note generation

## Troubleshooting

### Common Issues:

1. **Database Connection Error**:
   - Verify DATABASE_URL format
   - Ensure Supabase project is active
   - Check database password

2. **GITHUB_TOKEN Error**:
   - Verify token has correct permissions
   - Token should not be expired
   - Environment variable is set correctly

3. **Import Errors**:
   - Check that all dependencies are in `requirements.txt`
   - Verify Python version compatibility

4. **Static Files Not Loading**:
   - Ensure files are in `public/` directory
   - Check `vercel.json` routing configuration

### Debugging:
- Check Vercel deployment logs in the dashboard
- Use `vercel logs [deployment-url]` for detailed logs
- Test locally with production config: `FLASK_CONFIG=production python src/main.py`

## Local Development vs Production

### Local Development:
- Uses SQLite database by default
- Loads `.env` file for environment variables
- Serves static files through Flask
- Debug mode enabled

### Production (Vercel):
- Uses PostgreSQL (Supabase)
- Environment variables from Vercel dashboard
- Static files served by Vercel CDN
- Debug mode disabled
- Automatic HTTPS and scaling

## Performance Considerations

1. **Database Connection Pooling**: Supabase handles this automatically
2. **Static Asset Caching**: Vercel CDN provides global caching
3. **Serverless Cold Starts**: First request may be slower (~1-2 seconds)
4. **Function Timeout**: Vercel has 10-second timeout for serverless functions

## Security

1. **Environment Variables**: Never commit secrets to version control
2. **HTTPS**: Automatic SSL/TLS certificates from Vercel
3. **CORS**: Properly configured for cross-origin requests
4. **Database**: Supabase provides built-in security features

## Monitoring

1. **Vercel Analytics**: Built-in performance monitoring
2. **Error Tracking**: Check Vercel function logs
3. **Database Monitoring**: Supabase dashboard provides metrics
4. **Uptime**: Vercel provides 99.9% uptime SLA