# Dokploy Deployment Guide

## Prerequisites

- Dokploy server running
- GitHub repository with KNIv2
- Domain name (optional but recommended)

## Step-by-Step Deployment

### 1. Create New Application

1. Login to your Dokploy dashboard
2. Click **"Create Application"**
3. Select **"GitHub"** as source
4. Choose your KNIv2 repository

### 2. Configure Application Settings

**Basic Settings:**
- **Application Name**: `kni-cms` (or your preferred name)
- **Build Context**: `kni_app/`
- **Dockerfile Path**: `Dockerfile` (relative to build context)
- **Port**: `8000`

**Advanced Settings:**
- **Health Check Path**: `/admin/login/`
- **Restart Policy**: `unless-stopped`

### 3. Environment Variables

Add these required environment variables:

```bash
SECRET_KEY=your-super-secret-key-here-generate-new-one
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SETTINGS_MODULE=KNI.settings.production
```

**Optional (Recommended for Production):**
```bash
# Database (if using external PostgreSQL)
DATABASE_URL=postgres://user:password@host:5432/database

# AWS S3 Storage (for media files)
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=cdn.yourdomain.com

# Cache Control
CACHE_CONTROL_S_MAXAGE=3600
CACHE_CONTROL_STALE_WHILE_REVALIDATE=86400
```

### 4. Domain Configuration

1. In Dokploy, go to **Domains** tab
2. Add your domain: `yourdomain.com`
3. Enable **SSL/TLS** (Let's Encrypt)
4. Set **www** redirect if needed

### 5. Deploy

1. Click **"Deploy"** button
2. Monitor build logs for any issues
3. Wait for deployment to complete

## Post-Deployment Setup

### Create Superuser

SSH into your Dokploy server and run:
```bash
# Replace 'kni-cms' with your actual container name
docker exec -it kni-cms python manage.py createsuperuser
```

Or use Dokploy's container console:
1. Go to **Containers** tab
2. Click **"Console"** on your running container
3. Run: `python manage.py createsuperuser`

### Load Initial Data (Optional)

If you want the demo content:
```bash
docker exec -it kni-cms python manage.py load_initial_data
```

## Environment-Specific Configuration

### Development/Staging
```bash
DEBUG=False
ALLOWED_HOSTS=staging.yourdomain.com
```

### Production
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
```

## Database Options

### Option 1: SQLite (Default)
- No additional configuration needed
- Suitable for small sites
- Data persists in container volume

### Option 2: PostgreSQL (Recommended)
1. Create PostgreSQL service in Dokploy
2. Set `DATABASE_URL` environment variable
3. Format: `postgres://user:pass@postgres-service:5432/dbname`

### Option 3: External Database
```bash
DATABASE_URL=postgres://user:pass@external-host:5432/dbname
```

## Storage Options

### Option 1: Local Storage (Default)
- Files stored in container
- Use Docker volumes for persistence
- Suitable for development

### Option 2: AWS S3 (Recommended for Production)
Set these environment variables:
```bash
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

## Monitoring & Logs

### View Logs
- Dokploy Dashboard → Your App → **Logs** tab
- Or via CLI: `docker logs kni-cms -f`

### Health Checks
- Endpoint: `https://yourdomain.com/admin/login/`
- Should return HTTP 200

### Performance Monitoring
- Monitor container resources in Dokploy
- Set up alerts for high CPU/memory usage

## Backup & Restore

### Backup Data
```bash
docker exec kni-cms python manage.py dumpdata --output=/app/backup.json
docker cp kni-cms:/app/backup.json ./backup-$(date +%Y%m%d).json
```

### Restore Data
```bash
docker cp backup.json kni-cms:/app/
docker exec kni-cms python manage.py loaddata /app/backup.json
```

## Troubleshooting

### Build Failures
- Check build logs in Dokploy
- Ensure `kni_app/` build context is correct
- Verify Dockerfile path

### Runtime Issues
- Check container logs
- Verify environment variables are set
- Test database connectivity

### Static Files Not Loading
- Ensure `ALLOWED_HOSTS` includes your domain
- Check if AWS S3 credentials are correct
- Verify static files were collected during build

### SSL Certificate Issues
- Wait 2-3 minutes for Let's Encrypt provisioning
- Ensure domain DNS points to your server
- Check Dokploy SSL configuration

## Scaling

### Horizontal Scaling
- Increase replica count in Dokploy
- Use external PostgreSQL database
- Use S3 for media files

### Vertical Scaling
- Increase container CPU/memory limits
- Monitor resource usage
- Optimize database queries

## Security Checklist

- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` set
- ✅ HTTPS enabled via Dokploy
- ✅ `ALLOWED_HOSTS` configured
- ✅ Database credentials secured
- ✅ Regular backups scheduled
- ✅ Container running as non-root user

## Support

- Check logs for error details
- Verify environment variable configuration
- Test with minimal configuration first
- Gradually add features (S3, custom domain, etc.)