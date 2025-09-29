FROM alpine:latest

RUN apk add --no-cache python3 gstreamer py3-gst py3-gobject3 gstreamer-tools gst-plugins-base gst-plugins-good gst-plugins-ugly py3-opencv
RUN apk add --no-cache gst-rtsp-server --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/

RUN mkdir /app

WORKDIR /app

COPY . .

EXPOSE 554

CMD ["python3", "server.py"]