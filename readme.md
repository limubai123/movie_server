# Movie api-server

django framework with sqlite is used to create rest api server for movies.
## Features

- Registration
- Login by JWT
- Add, review, vote, fetch Movie by authenticated user
- User can create fevourite genre list, according to that user will get movie recomendation
- Public movies api where you can sort according to release date, and up and downvote

## Installation

System requires docker and docker-compose

Install the dependencies and devDependencies and start the server.

```sh
sudo docker-compose -f django.yaml build
sudo docker-compose -f django.yaml up -d
```

Test cases are written,  which will run at the time of build command
There is one management command which will fill default genre, it will also run during build process

## Reposatory
```sh
https://github.com/limubai123/movie_server
```

## Postman link
```sh
https://documenter.getpostman.com/view/5497455/UVJckGPQ#55d05e0a-f38d-44aa-a728-851da9c3f495
```

