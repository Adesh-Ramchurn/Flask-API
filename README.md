docker build -t flask-smorest-api . -> building the docker image



docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api -> this will create a volume where if we make changes to the code, then the app is rebuilt on docker

