Welcome to KNIv2's documentation!
=====================================

KNIv2 is a production-ready Django/Wagtail CMS with optimized development workflow and Dokploy deployment strategy.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quick-start
   workflow
   architecture
   deployment
   PRODUCTION_DEPLOYMENT

Features
========

* **Django Best Practices**: Nginx + Gunicorn + PostgreSQL
* **Dokploy Optimized**: CI builds, Dokploy deploys
* **Staging-Based Workflow**: Clear release boundaries
* **Local Development**: SQLite for fast iteration
* **Production Parity**: PostgreSQL testing before deployment
* **Health Monitoring**: Health checks and rollbacks
* **Persistent Storage**: Proper volume management

Quick Start
===========

.. code-block:: bash

   # Clone repository
   git clone <repository-url>
   cd KNIv2

   # Install dependencies
   pip install -r requirements.txt
   npm install

   # Build static assets
   npm run build

   # Start development server
   make dev

   # Visit: http://localhost:8000

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
