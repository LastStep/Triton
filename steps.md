
# Main Docker setup
docker compose up --build
- holds the layout for multi docker setup

# Docker setup with node

Node v22.14.0 (LTS) - Windows - Docker - npm
https://nodejs.org/en/download
docker pull node:22-alpine
- downloads the image

docker build -t image-name .
- first we cd into the directory with docker file, then build the image
- then we run the docker container
docker run -it -p 3000:3000 --rm -v e/Triton/frontend:/app node:22-alpine sh
- links the frontend folder in the Triton project with the app folder in dockerfile
- [node:22-alpine sh] this is the image name

npm run dev
- to run the app
- this is added in CMD of dockerfile, to execute when the container starts

Hot reload issues
- removed turbopack from package.json > scripts > dev


# WSL linux distro (for windows)
wsl --install -d Ubuntu-22.04
- download the distro
sudo apt update && sudo apt upgrade


# Python datasource
Install pipx
- pip install pipx
- https://pipx.pypa.io/stable/installation/
- python -m pipx ensurepath # Add pipx to PATH

Install poetry
- pipx install poetry 
- gives poetry its own isolated environment
- pipx inject poetry poetry-plugin-shell
- shell is needed for venv creation

