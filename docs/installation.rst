=========================================
AwesomeBioVault Installation Guide
=========================================

.. contents::
    :local:

Introduction
------------

This guide provides two methods to install and run the AwesomeBioVault project:

1. **Docker Installation**: Utilizes Docker and Docker Compose.
2. **Local Installation**: Installs project dependencies locally using `requirements/dev.txt`.

Prerequisites
-------------

Make sure you have the following software installed on your machine:

- **Docker**: https://docs.docker.com/get-docker/
- **Docker Compose**: https://docs.docker.com/compose/install/
- **Python and pip**: https://www.python.org/downloads/

Clone the Repository
--------------------

Clone the AwesomeBioVault project repository from GitHub:

.. code-block:: bash

    git clone https://github.com/mramitdas/AwesomeBioVault.git
    cd AwesomeBioVault

Create the .env File
--------------------

Create a file named ``.env`` in the project root and add the following variables:

    .. code-block:: bash

        DB_URL=""
        DB_NAME=AwesomeBioVault
        PROFILE_TABLE_NAME=github_profile
        REDIS_SERVER=redis://redis:6379/0

        PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

        GITHUB_TOKEN=""
        REPO_OWNER=mramitdas
        REPO_NAME=AwesomeBioVault
        BRANCH=dev



Docker Installation
--------------------

1. **Build and Run with Docker Compose:**

    .. code-block:: bash

        docker-compose up --build

    This command will build the Docker images and start the containers.

2. **Access the Application:**

    Once the containers are running, access the AwesomeBioVault application in your web browser:

    - Open your browser and navigate to: http://localhost:5000

3. **Stopping the Application:**

    To stop the application and shut down the containers, use the following command:

    .. code-block:: bash

        docker-compose down

Local Installation (without Docker)
-----------------------------------

1. **Install Dependencies:**

    Install project dependencies locally using `requirements/dev.txt`:

    .. code-block:: bash

        pip install -r requirements/dev.txt

2. **Run the Application:**

    Run the AwesomeBioVault application locally:

    .. code-block:: bash

        cd app
        flask run --reload

    The application should be accessible in your browser at http://localhost:5000.

Customization
-------------

If you need to customize the project settings, you can modify the `docker-compose.yml` file for Docker installation or adjust local configuration files.

Conclusion
-----------

Congratulations! You have successfully installed and run the AwesomeBioVault project using Docker or a local setup. If you encounter any issues, refer to the project documentation or seek help from the project community.
