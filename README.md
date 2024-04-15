---
date: 2024-04-15T17:43:45.578023
author: AutoGPT <info@agpt.co>
---

# test

Based on the understood requirements and prior information gathered through the interview and search process, the solution involves developing an image processing application. The core functionality of this application includes accepting an image file from the user, resizing the image to fit within specified dimensions and optionally cropping it to maintain the aspect ratio, and finally returning the resized image file to the user. The preferences for supporting PNG and SVG formats are noted, ensuring versatility and scalability in image handling. Maintaining the aspect ratio during resizing is essential for preserving the image's original visual integrity, as highlighted by the user. Additional features such as adjusting brightness and contrast, applying filters, and performing rotation and flipping have been considered to enhance the visual appeal and suitability of images for various contexts.

The tech stack recommended for this project includes Python as the programming language, known for its robust libraries and frameworks for image processing tasks. The PIL (Python Imaging Library) or its more updated fork, Pillow, will be utilized for the core image manipulation tasks, such as resizing, cropping, and applying additional visual adjustments as per the user's requirements. These libraries offer built-in functions to handle aspect ratio calculations, interpolation methods, and format-specific settings, aligning with the best practices identified during the research phase.

For the backend API, FastAPI is chosen for its performance and ease of building async APIs that can handle file uploads and processing efficiently. PostgreSQL will serve as the database to manage user sessions or stored images if needed, with Prisma as the ORM for seamless integration and database management. FastAPI's ability to work asynchronously fits well with the potentially resource-intensive nature of image processing, ensuring the application remains responsive.

The application will provide endpoints allowing users to upload images, specify desired dimensions (and optionally request cropping), and receive the processed image. This setup aims to offer a user-friendly, efficient, and scalable solution to image resizing and manipulation needs.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'test'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
