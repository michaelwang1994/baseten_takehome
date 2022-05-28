export FLASK_HOST=0.0.0.0
export FLASK_PORT=5000
export REDIS_HOST=127.0.0.1
export REDIS_PORT=6379
export FLASK_APP=main
docker run -p $REDIS_PORT:$REDIS_PORT redis:latest &
flask run --host $FLASK_HOST --port $FLASK_PORT