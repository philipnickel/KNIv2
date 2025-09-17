hjjj# KNI v2 - Wagtail CMS

A Docker-ready Wagtail CMS template optimized for GitHub integration and Dokploy deployment.

## Quick Start

```bash
cd kni_app
make build
make load-data
make dev
```

Visit: http://localhost:8000

## Makefile Commands

| Command | Purpose |
|---------|---------|
| `make build` | Build Docker image |
| `make dev` | Start development server |
| `make start` | Start production server |
| `make load-data` | Setup database with demo content |
| `make dump-data` | Backup current site to `fixtures/demo.json` |
| `make reset-db` | Reset database and restore from backup |
| `make manage CMD="..."` | Run Django commands |
| `make shell` | Open container shell |

## Deployment

### GitHub Integration
- Push to repository triggers automatic builds
- Uses `kni_app/Dockerfile` for containerization
- Environment variables managed via GitHub secrets

### Dokploy Deployment
1. Connect GitHub repository
2. Set build context to `kni_app/`
3. Configure environment variables:
   - `SECRET_KEY` - Django secret key
   - `DATABASE_URL` - Database connection (optional, defaults to SQLite)
   - `ALLOWED_HOSTS` - Comma-separated host list

### Environment Variables
```bash
# Required
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Optional
DATABASE_URL=postgres://user:pass@host:port/db
MEDIA_ROOT=/app/media
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

## Storage Options

**Local (Default)**: SQLite + local filesystem
**Cloud**: PostgreSQL + AWS S3 (auto-configured when `AWS_STORAGE_BUCKET_NAME` is set)

## Data Management

**Backup**: `make dump-data` exports to `fixtures/demo.json`
**Restore**: `make reset-db` restores from backup
**Fresh Start**: Delete `db.sqlite3` and run `make load-data`

## Development

Default admin: Check initial data loading output or create with:
```bash
make manage CMD="createsuperuser"
```

Port customization:
```bash
DEV_HOST_PORT=8080 make dev
```