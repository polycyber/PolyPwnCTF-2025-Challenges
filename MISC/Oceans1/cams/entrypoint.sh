(cd /nvr && gunicorn -w 4 -b 0.0.0.0:80 app:app) &
P1=$!
(cd /rtsp && python server.py) &
P2=$!
wait $P1 $P2