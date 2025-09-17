# Wagtail News Template

This project template is designed for creating [Wagtail](https://wagtail.org) builds quickly, intended for developers to bootstrap their Wagtail site development using `wagtail start --template=`. The template comes with pre-defined pages, blocks, functionalities, and fixtures to streamline the initial setup process.

## Getting Started

1. **Check that you have an appropriate version of Python 3** You want to make sure that you have a [compatible version](https://docs.wagtail.org/en/stable/releases/upgrading.html#compatible-django-python-versions) installed:

   ```sh
   python --version
   # Or:
   python3 --version
   # **On Windows** (cmd.exe, with the Python Launcher for Windows):
   py --version
   ```

2. **Create a Virtual Environment**: Set up a virtual environment to isolate your project dependencies. These instructions are for GNU/Linux or MacOS, but there are [other operating systems in the Wagtail docs](https://docs.wagtail.org/en/stable/getting_started/tutorial.html#create-and-activate-a-virtual-environment).

   ```bash
   python -m venv myproject/env
   source myproject/env/bin/activate
   ```

3. **Navigate to Project Directory**: Move into the newly created project directory.

   ```bash
   cd myproject
   ```

4. **Install Wagtail**: Install the Wagtail CMS package using pip.

   ```bash
   pip install wagtail
   ```

5. **Initialize Project**: Use the `wagtail start` command to create a new project based on the KNI template.

   ```bash
   wagtail start --template=https://github.com/wagtail/KNI/archive/refs/heads/main.zip myproject .
   ```

6. **Install Project Dependencies**: Install the project's dependencies into a virtual environment.

   ```bash
   pip install -r requirements.txt
   ```

All commands from now on should be run from inside the virtual environment.

### Using Docker (alternative to steps 2–6)

Once you've generated your project with `wagtail start` and moved into the project directory, you can stay close to the production image while keeping development convenient:

1. Build the image: `make build`
2. Load the demo content (migrations, fixtures, collectstatic): `make load-data`
3. Start a development server with Django autoreload: `make dev`
   - Stop with `Ctrl+C`. Override the port with `DEV_HOST_PORT=8010` or add Docker flags via `DEV_RUN_FLAGS=-it`.
4. Start a production-like server (Gunicorn, identical to the Dockerfile's `CMD`): `make start`
   - Use `PROD_HOST_PORT=8010` to change the host binding, or `make start PROD_RUN_FLAGS=-d` to run detached.

Use `make manage CMD="migrate"` for ad hoc management commands and `make shell` for an interactive shell inside the image. Set `ENV_FILE=.env` to load environment variables automatically; additional Docker arguments can be supplied through `DEV_RUN_FLAGS`, `PROD_RUN_FLAGS`, or `MANAGE_RUN_FLAGS`.

8. **Load Dummy Data**: Load in some dummy data to populate the site with some content.

   ```bash
   make load-data  # executes management commands inside the Docker image
   ```

9. **Start the Server**: Start the Django development server.

   ```bash
   make start  # runs the Docker image with its production entrypoint
   ```

10. **Access the Site and Admin**: Once the server is running, you can view the site at `localhost:8000` and access the Wagtail admin interface at `localhost:8000/admin`. Log in with the default credentials provided by :

    - Username: admin
    - Password: password

### Deploying

Once you have your own copy of the template, you can extend and configure it however you like.

To get it deployed, follow the instructions below for your hosting provider of choice.

Don't see your preference here? Contributions are always welcome!

#### fly.io

Before you can deploy to [fly.io](https://fly.io/), you will need an account and the `fly` CLI tool will need to be [installed on your machine](https://fly.io/docs/flyctl/install/).

1. In the root directory of your project (the one with a `fly.toml` file), run `fly launch`
   1. When prompted about copying the existing `fly.toml` file to a new app, choose "Yes".

> [!CAUTION]
> Choosing "No" (the default) here will result in a broken deployment, as the `fly.toml` file requires configuration needed for the project to run correctly.

2. When prompted about continuing the setup in the web UI, or tweak the generated settings, choose "No".
   1. The "Region" will be selected automatically. If you wish to change this, choose "Yes" instead, and modify the region in the browser.
3. Once the launch is successful, you'll need to [generate a secret key](https://realorangeone.github.io/django-secret-key-generator/)
   1. This can be done using `fly secrets set SECRET_KEY=<key>`, or through the web UI.
4. Finally (optional), load in the dummy data, to help get you started
   1. `fly ssh console -u wagtail -C "./manage.py load_initial_data"`

> [!NOTE]
> If you receive "error connecting to SSH server" when running the above command, It likely means the `fly.toml` above wasn't picked up correctly. Unfortunately, you'll need to delete your application and start again, resetting the changes to the `fly.toml` file.
> If the error still persists, check the application logs.

You can now visit your wagtail site at the URL provided by `fly`. We strongly recommend setting strong password for your user.

The database and user-uploaded media are stored in the attached volume. To save costs and improve efficiency, the app will automatically stop when not in use, but will automatically restart when the browser loads.

#### Dokploy

Deploying with [Dokploy](https://dokploy.com/) works directly from the provided `Dockerfile`.

1. **Build and push the image**
   Build the image locally (or in CI) and push it to the container registry Dokploy can access:

   ```bash
   docker build -t registry.example.com/your-org/{{ project_name }}:latest .
   docker push registry.example.com/your-org/{{ project_name }}:latest
   ```

2. **Create the Dokploy application**
   - Choose **Dockerfile / Docker image** as the deployment method.
   - Point Dokploy at the pushed image (or let it build from the repository; the Dockerfile already targets production settings).

3. **Set environment variables**
   At minimum configure:
   - `SECRET_KEY`
   - `DATABASE_URL` (e.g. `postgres://USER:PASSWORD@HOST:5432/DBNAME`)
   - `ALLOWED_HOSTS` (comma separated hostnames supplied by Dokploy)
   - `CSRF_TRUSTED_ORIGINS` (comma separated HTTPS origins, e.g. `https://example.com`)
   Dokploy automatically sets `PORT`; keep it at `8000` or update both `PORT` and the exposed port in the service definition.

4. **Mount persistent storage**
   Add a Dokploy volume that maps to `/app/media` so user uploads survive restarts. Static files are baked into the image during `collectstatic`.

5. **Handle database migrations**
   Configure a release/one-off command in Dokploy to run `python manage.py migrate` on deploys. (The container's default `CMD` still performs migrations defensively, but an explicit release step is recommended.)

6. **Optional demo content**
   Once deployed, run `python manage.py load_initial_data` as a one-off task if you want the bundled sample content.

After the app is healthy you can log in at `/admin` using the credentials you set (change the default password immediately).

#### Divio Cloud

[![Deploy to Divio](https://docs.divio.com/deploy-to-divio.svg)](https://control.divio.com/app/new/?template_url=https://github.com/wagtail/KNI/archive/refs/heads/main.zip)

Easily deploy your application to [Divio Cloud](https://www.divio.com/) using the steps below:

1. **Getting Started**
   Follow the [Getting Started](#getting-started) instructions to set up your project locally.

2. **Push Your Repository**
   Upload your project to GitHub or another Git provider.

3. **Create a New Application**
   Log in to the [Divio Control Panel](https://control.divio.com/) and create a new application and

   - Choose "**I already have a repository**.".
   - Connect your Git provider and proceed by clicking "**Next**.".
   - Give your application a suitable name and select the "**Free Trial**" plan, then click **"Create application."**.

   Your application will be created with two environments: **Test** and **Live**.

4. **Add a Database service**
   From the **Services** view of your application, add a [database](https://docs.divio.com/introduction/aldryn-django/django-05-database/) service.

5. **Deploy Your Application**
   From the "Environments" view, click "**Deploy**" on the **Test** environment. Once the deployment completes, access your site using the "Env URL" link.

6. **Additional Configuration**
   **Migrations and Environment Variables**:

   To automatically run migrations on every deployment, add a "Release command" within the **Settings** section of your application with the value `python manage.py migrate`.
You can add additional commands as needed.

   Use the **Env Variables** section to set variables such as `SECRET_KEY` ([generator](https://realorangeone.github.io/django-secret-key-generator/)) for the test and live environments.

   **Media Storage**: From the **Services** view of your application, add an [object storage](https://docs.divio.com/reference/work-media-storage/) to store user-uploaded files.

## Makefile Commands Reference

This project includes a comprehensive Makefile that simplifies Docker operations and development workflows. All commands run in Docker containers, ensuring consistent environments across different machines.

### Configuration Variables

The Makefile supports several configuration options:

- `DOCKER`: Docker command to use (default: `docker`)
- `PROJECT_NAME`: Auto-derived from directory name (`kni_app`)
- `IMAGE`: Docker image name (`kni_app:latest`)
- `DEV_SETTINGS`: Django settings for development (`KNI.settings.dev`)
- `DEV_HOST_PORT`: Local port for development (default: 8000)
- `PROD_HOST_PORT`: Local port for production (default: 8000)
- `ENV_FILE`: Optional environment file to load

### Build & Development Commands

#### `make build`
**Purpose**: Build the Docker image with all dependencies
```bash
make build
```
**When to use**: First time setup or after changing Dockerfile/requirements

#### `make dev`
**Purpose**: Start development server with live code reloading
```bash
make dev
```
**What it does**:
- Builds image if needed
- Runs server with live code reloading
- Mounts your code directory for instant changes
- Accessible at http://localhost:8000
- Stop with `Ctrl+C`

**Options**:
```bash
# Change port
DEV_HOST_PORT=8010 make dev

# Add Docker flags
DEV_RUN_FLAGS="-it" make dev
```

#### `make start`
**Purpose**: Start production-like server (Gunicorn)
```bash
make start
```
**What it does**:
- Runs optimized production container
- No code mounting (uses image code)
- Uses production settings

**Options**:
```bash
# Change port
PROD_HOST_PORT=8010 make start

# Run detached
make start PROD_RUN_FLAGS="-d"
```

### Database & Content Management

#### `make load-data`
**Purpose**: Complete database setup with sample data
```bash
make load-data
```
**What it does**:
1. Creates cache table
2. Runs all migrations
3. Loads demo content from `fixtures/demo.json`
4. Collects static files

**When to use**: First setup or fresh environment

#### `make migrate`
**Purpose**: Apply database migrations only
```bash
make migrate
```
**When to use**: After model changes

#### `make collectstatic`
**Purpose**: Gather static files for serving
```bash
make collectstatic
```
**When to use**: Before production deployment

#### `make dump-data`
**Purpose**: Create backup of current site content
```bash
make dump-data
```
**What it does**: Exports all data to `fixtures/demo.json`
**When to use**: Before major changes or for backups

#### `make reset-db`
**Purpose**: Completely reset database to fresh state
```bash
make reset-db
```
**What it does**:
1. Deletes `db.sqlite3`
2. Runs `make load-data`

**When to use**: Start over with clean data

### Utility Commands

#### `make manage CMD="<command>"`
**Purpose**: Run any Django management command
```bash
make manage CMD="createsuperuser"
make manage CMD="showmigrations"
make manage CMD="shell"
make manage CMD="collectstatic"
```
**When to use**: One-off Django admin tasks

#### `make shell`
**Purpose**: Open interactive bash shell in container
```bash
make shell
```
**When to use**: Debugging, manual operations, exploring container

### Environment Variables

Load environment variables from a file:
```bash
ENV_FILE=.env make dev
```

### Common Workflows

**First time setup:**
```bash
make build
make load-data
make dev
```

**Daily development:**
```bash
make dev  # Just this!
```

**Create backup:**
```bash
make dump-data
```

**Reset everything:**
```bash
make reset-db
make dev
```

**Create superuser:**
```bash
make manage CMD="createsuperuser"
```

**Check migration status:**
```bash
make manage CMD="showmigrations"
```

**Access Django shell:**
```bash
make manage CMD="shell"
```

### Backup & Restore Workflow

The Makefile provides robust backup and restore functionality:

1. **Create a backup** of your current site:
   ```bash
   make dump-data
   ```

2. **Restore from backup** later:
   ```bash
   make reset-db  # Deletes current DB and loads from fixtures/demo.json
   ```

3. **Load backup into empty database**:
   ```bash
   make load-data  # Use when database doesn't exist
   ```

All backups are stored in `fixtures/demo.json` and include:
- All pages and content
- User accounts and permissions
- Site settings and configuration
- Media file references (actual media files in `fixtures/media/`)

The system excludes temporary data like sessions, search indexes, and cached permissions for clean restores.

## Contributing

To customize this template, you can either make changes directly or backport changes from a generated project (via the `wagtail start` command) by following these steps:

1. Create a new project using the provided instructions in the [Getting Started](#getting-started) section.
2. Make changes within the new project.
3. Once you've completed your changes, you'll need to copy them over to the original project template, making sure to:

   3.1. Replace occurrences of `myproject` with `{{ project_name }}`

   3.2. Rename the project directory from `myproject` to `project_name` (without double curly brackets this time).

   3.3. Wrap template code (`.html` files under the templates directory), with a [verbatim tag](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/#std-templatetag-verbatim) or similar [templatetag](https://docs.djangoproject.com/en/5.0/ref/templates/builtins/#templatetag) to prevent template tags being rendered on `wagtail start` ([see django's rendering warning](https://docs.djangoproject.com/en/5.0/ref/django-admin/#render-warning)).

4. Update compiled static assets using `npm run build:prod`.
5. Update fixtures using `make dump-data`

Make sure to test any changes by reviewing them against a newly created project, by following the [Getting Started](#getting-started) instructions again.

Happy coding with Wagtail! If you encounter any issues or have suggestions for improvement, feel free to contribute or open an issue.
