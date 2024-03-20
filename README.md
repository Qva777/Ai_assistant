<hr>

<h1>📍How to install: </h1>

> This project is an AI chat assistant developed for the TikTok platform.
> The goal of the project is to provide users with a convenient way to
> obtain a variety of information from their profile, analyze data and
> obtain aggregated data on various aspects of their activity on TikTok.


<!-- DOCKER -->
<details><summary><h2>🐳Connect to Docker Compose:</h2></summary><br/>

<h3>Visit the [API keys](https://platform.openai.com/api-keys) to get your key.</h3>

<h3>Insert this command into cmd/terminal (in .env file set correct values):</h3>

```
cd backend/
echo "Creating .env file..."
cat <<EOL > .env
# Get API KEY https://platform.openai.com/api-keys
OPENAI_API_KEY = "sk-..."

# TOKEN TO MAKE REQUESTS TO DataBase
TOKEN = "eyJhbGciO..."
EOL
cd ..
```

<h3>UP Docker-compose:</h3>

```
docker-compose -f docker/docker-compose.yml up --build
```

<h3>Login to the container console:</h3>

```
docker exec -it django-container bash
```

</details>
<!-- END DOCKER -->

# Endpoints


- **GET** `http://localhost:5173/`: Home page
- **POST** `/query/`: Request to Ai
