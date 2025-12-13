# Module 14 Deployment Guide

## Step 1: Set Up Docker Hub (Already Done ✓)

Your Docker Hub repository is: `emkoscielniak/module14_is218`

If you haven't created this repository yet:
1. Go to https://hub.docker.com
2. Click "Create Repository"
3. Name: `module14_is218`
4. Visibility: Public
5. Click "Create"

## Step 2: Configure GitHub Secrets (REQUIRED)

You need to add these secrets to your GitHub repository:

1. Go to: https://github.com/emkoscielniak/module14_is218/settings/secrets/actions

2. Add these secrets:
   - **DOCKERHUB_USERNAME**: `emkoscielniak`
   - **DOCKERHUB_TOKEN**: Get from Docker Hub → Account Settings → Security → New Access Token

### Generate Docker Hub Access Token:
1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Description: `github-actions-module14`
4. Access permissions: Read & Write
5. Click "Generate"
6. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)
7. Add it to GitHub secrets as `DOCKERHUB_TOKEN`

## Step 3: Test Local Docker Build

```bash
# Build the production image
docker build -t emkoscielniak/module14_is218:latest .

# Test it locally
docker run -p 8000:8000 -e DATABASE_URL="postgresql://postgres:postgres@host.docker.internal:5432/fastapi_db" emkoscielniak/module14_is218:latest

# Visit http://localhost:8000
```

## Step 4: Create Docker Hub Repository

**IMPORTANT: Do this BEFORE pushing to GitHub!**

1. Go to https://hub.docker.com/repositories
2. Click "Create Repository"
3. Fill in:
   - **Name**: `module14_is218`
   - **Description**: "FastAPI Module 14 with JWT auth and BREAD operations"
   - **Visibility**: Public (free) or Private (paid)
4. Click "Create"

Your repository will be at: https://hub.docker.com/r/emkoscielniak/module14_is218

## Step 5: Push to GitHub to Trigger Deployment

```bash
# Make s6: Set Up Server (138.197.75.94)

**⚠️ PREREQUISITES:**
- ✅ GitHub Actions workflow completed successfully
- ✅ Docker image visible at https://hub.docker.com/r/emkoscielniak/module14_is218
- ✅ You see the `latest` tag in Docker Hub
git add .
git commit -m "Configure Module 14 deployment with Watchtower"
git push origin main
```

This will trigger the CI/CD pipeline:
1. ✅ Run tests
2. ✅ Security scan
3. ✅ Build Docker image
4. ✅ Push to Docker Hub

Watch the progress at: https://github.com/emkoscielniak/module14_is218/actions

**⏳ WAIT FOR THIS TO COMPLETE (5-10 minutes) BEFORE PROCEEDING TO SERVER SETUP!**

You'll know it's done when:
- ✅ GitHub Actions workflow shows all green checkmarks
- ✅ You can see the image at https://hub.docker.com/r/emkoscielniak/module14_is218/tags
- ✅ You see tags: `latest` and a git SHA tag

## Step 5: Set Up Server (138.197.75.94)

### SSH to Your Server

```bash
ssh root@138.197.75.94
# Or if you have a non-root user:
# ssh your-username@138.197.75.94
```

### Create Application Directory

```bash
mkdir -p ~/module14_is218
cd ~/module14_is218
```

### Create .env File

```bash
nano .env
```

Paste this content (UPDATE THE PASSWORDS!):

```env
# Database Configuration
POSTGRES_DB=fastapi_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=CHANGE_THIS_TO_SECURE_PASSWORD

# Application Configuration (use service name 'db' not 'localhost')
DATABASE_URL=postgresql://postgres:CHANGE_THIS_TO_SECURE_PASSWORD@db:5432/fastapi_db

# JWT Secret Key (generate with command below)
SECRET_KEY=CHANGE_THIS_TO_SECURE_KEY

# Docker Configuration
DOCKER_IMAGE=emkoscielniak/module14_is218
```

**Generate a secure SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and replace `CHANGE_THIS_TO_SECURE_KEY` in .env

### Download Production Docker Compose

```bash
# Download from your repository
wget https://raw.githubusercontent.com/emkoscielniak/module14_is218/main/docker-compose.prod.yml -O docker-compose.yml

# Or create it manually:
nano docker-compose.yml
```

Paste the content from `docker-compose.prod.yml`

### Start the Application

```bash
# Pull the latest images
docker compose pull

# Start all services (web, db, watchtower)
docker compose up -d

# Check that everything is running
docker compose ps

# View logs
docker compose logs -f
```

You should see:
- ✅ web container running
- ✅ db container running (healthy)
- ✅ watchtower container running

### Test the Application

```bash
# Test locally on the server
curl http://localhost:8000
curl htt7://localhost:8000/docs

# You should get responses!
```

## Step 6: Configure Caddy for HTTPS

### Edit Caddyfile

```bash
sudo nano /etc/caddy/Caddyfile
```

Add this configuration:

```caddyfile
# Module 14 FastAPI Application
project14.emkoscielniak.com {
    reverse_proxy localhost:8000
}

# Optional: www redirect
www.project14.emkoscielniak.com {
    redir https://project14.emkoscielniak.com{uri}
}
```

### Reload Caddy

```bash
sudo systemctl reload caddy
sudo systemctl status caddy
```

### Configure DNS (Namecheap)

1. Go to Namecheap dashboard
2. Select domain: `emkoscielniak.com`
3. Click "Advanced DNS"
4. Add A Record:
   - **Host**: `project14`
   - **Value**: `138.197.75.94`
   - **TTL**: Automatic

Wait 5-10 minutes for DNS propagation.

### Test HTTPS

```bash8
curl https://project14.emkoscielniak.com
curl https://project14.emkoscielniak.com/docs
```

## Step 7: Test Automatic Deployment

### Make a Change Locally

```bash
# On your local machine
cd ~/is218/module14

# Make a visible change
echo "# Deployment test: $(date)" >> README.md
```

### Commit and Push

```bash
git add .
git commit -m "Test automatic deployment"
git push origin main
```

### Watch the Magic Happen

1. **GitHub Actions** (2-5 minutes):
   - Go to https://github.com/emkoscielniak/module14_is218/actions
   - Watch tests run → build → push to Docker Hub

2. **Watchtower** (5 minutes):
   - On server: `docker compose logs -f watchtower`
   - Should see: "Checking for updates..."
   - Should see: "Pulling new image..."
   - Should see: "Stopping old container..."
   - Should see: "Starting new container..."

3. **Verify**:
   ```bash
   # Check your website
   curl https://project14.emkoscielniak.com
   
   # Changes should be live!
   ```

## Monitoring Commands

```bash
# On the server

# View all logs
docker compose logs -f

# View specific service
docker compose logs -f web
docker compose logs -f watchtower

# Check container status
docker compose ps

# Restart a service
docker compose restart web

# Stop everything
docker compose down

# Stop and remove volumes (careful!)
docker compose down -v
```

## Database Backup

```bash
# Create backup
docker compose exec db pg_dump -U postgres fastapi_db > backup-$(date +%Y%m%d-%H%M%S).sql

# Restore from backup
cat backup.sql | docker compose exec -T db psql -U postgres fastapi_db
```

## Troubleshooting

### Watchtower Not Updating

```bash
# Check Watchtower logs
docker compose logs watchtower

# Manually pull and restart
docker compose pull
docker compose up -d
```

### Database Connection Issues

```bash
# Check database is running
docker compose ps db

# Check database logs
docker compose logs db

# Verify DATABASE_URL uses 'db' not 'localhost'
cat .env | grep DATABASE_URL
# Should be: postgresql://postgres:password@db:5432/fastapi_db
```

### Port Already in Use

```bash
# Find what's using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>
```

### View Container Details

```bash
# Inspect container
docker inspect module14_is218-web-1

# Check environment variables
docker compose config
```

## Success Checklist

- ✅ Docker Hub repository created
- ✅ GitHub secrets configured (DOCKERHUB_USERNAME, DOCKERHUB_TOKEN)
- ✅ GitHub Actions workflow running successfully
- ✅ Server set up with .env file
- ✅ Docker Compose running (web, db, watchtower)
- ✅ Caddy configured for HTTPS
- ✅ DNS configured (project14.emkoscielniak.com)
- ✅ Application accessible at https://project14.emkoscielniak.com
- ✅ Automatic deployment working (push → GitHub Actions → Docker Hub → Watchtower → Live)

## URLs

- **Local Development**: http://localhost:8000
- **Production**: https://project14.emkoscielniak.com
- **API Docs**: https://project14.emkoscielniak.com/docs
- **GitHub Repo**: https://github.com/emkoscielniak/module14_is218
- **Docker Hub**: https://hub.docker.com/r/emkoscielniak/module14_is218
- **GitHub Actions**: https://github.com/emkoscielniak/module14_is218/actions

---

**Your Complete CI/CD Pipeline:**
```
Code Change → Git Push → GitHub Actions → Docker Hub → Watchtower → Live Site ✨
```

**Time from push to live: ~10 minutes**
