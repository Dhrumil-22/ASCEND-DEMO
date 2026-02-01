# ASCEND Deployment Guide

## 🚀 Deployment Options

### Option 1: Heroku (Recommended for beginners)

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create ascend-mentorship
   ```

4. **Add PostgreSQL Database**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set FLASK_ENV=production
   ```

6. **Create Procfile**
   ```
   web: gunicorn run:app
   ```

7. **Update requirements.txt**
   Add `gunicorn` and `psycopg2-binary` to requirements.txt

8. **Deploy**
   ```bash
   git push heroku main
   ```

9. **Run Migrations**
   ```bash
   heroku run flask db upgrade
   heroku run python scripts/setup_db.py
   ```

10. **Open App**
    ```bash
    heroku open
    ```

---

### Option 2: Railway.app

1. **Sign up at railway.app**

2. **Create New Project** → Deploy from GitHub

3. **Add PostgreSQL Database**
   - Click "New" → Database → PostgreSQL

4. **Set Environment Variables**
   - `SECRET_KEY`: Your secret key
   - `DATABASE_URL`: (Auto-set by Railway)
   - `FLASK_ENV`: production

5. **Deploy automatically on git push**

---

### Option 3: DigitalOcean App Platform

1. **Create account at digitalocean.com**

2. **Create New App** → Select GitHub repository

3. **Configure Build**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn run:app`

4. **Add Managed Database** (PostgreSQL)

5. **Set Environment Variables** in App Settings

6. **Deploy**

---

### Option 4: AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**
   ```bash
   eb init -p python-3.10 ascend-app
   ```

3. **Create Environment**
   ```bash
   eb create ascend-env
   ```

4. **Set Environment Variables**
   ```bash
   eb setenv SECRET_KEY=your-secret-key
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

---

## 🔧 Production Configuration

### Environment Variables

Create a `.env` file or set these in your hosting platform:

```env
# Required
SECRET_KEY=your-very-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/dbname
FLASK_ENV=production

# Optional
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Migration

```bash
# Initialize migrations (first time only)
flask db init

# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Seed demo data
python scripts/setup_db.py
```

### Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Use PostgreSQL (not SQLite) in production
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookie flags
- [ ] Implement rate limiting
- [ ] Add CSRF protection (already included via Flask-WTF)
- [ ] Sanitize user inputs
- [ ] Regular security updates

---

## 📊 Monitoring & Maintenance

### Application Monitoring

- Use Heroku metrics or your platform's monitoring
- Set up error tracking (Sentry, Rollbar)
- Monitor database performance
- Track user activity and engagement

### Backup Strategy

```bash
# Backup database (Heroku example)
heroku pg:backups:capture
heroku pg:backups:download
```

### Scaling

```bash
# Scale dynos (Heroku)
heroku ps:scale web=2

# Upgrade database
heroku addons:upgrade heroku-postgresql:standard-0
```

---

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Check `DATABASE_URL` is set correctly
- Ensure database is running
- Verify network/firewall settings

**Static Files Not Loading**
- Run `flask assets build` if using Flask-Assets
- Check static file paths in templates
- Verify hosting platform serves static files

**Migration Errors**
- Delete `migrations/` folder and reinitialize
- Check for model conflicts
- Ensure database is accessible

**Import Errors**
- Verify all dependencies in requirements.txt
- Check Python version compatibility
- Rebuild virtual environment

---

## 📞 Support

For deployment issues:
- Check platform documentation
- Review application logs
- Contact platform support
- Open GitHub issue

---

## 🎯 Post-Deployment Checklist

- [ ] Test all user flows (student, mentor, admin)
- [ ] Verify email notifications work
- [ ] Test database backups
- [ ] Set up monitoring and alerts
- [ ] Configure custom domain (optional)
- [ ] Add SSL certificate
- [ ] Test performance under load
- [ ] Document any platform-specific configurations
