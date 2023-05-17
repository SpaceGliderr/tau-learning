# Opening Report Portal

1. Start Docker container for Report Portal

   ```
   docker compose -p reportportal up -d --force-recreate
   ```

   **NOTE**: Can omit `--force-recreate` flag if you don't want to rebuild the container

2. Check container status

   ```
   docker ps -a
   ```

3. Go to `localhost:8080` and access Report Portal dashboard

# Debugging Log

## ElasticSearch keeps restarting

1. Stop all running containers - `docker stop $(docker ps -aq)`
2. Create /data/elasticsearch directory - `mkdir -p data/elasticsearch`
3. Give permissions to the directory - `chmod 777 data/elasticsearch`
4. Change ownership of the directory - `sudo chown 1000:1000 data/elasticsearch/`
5. Bring up containers - `docker compose -p reportportal up -d`
