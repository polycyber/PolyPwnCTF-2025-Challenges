FROM alpine:latest

RUN apk add --no-cache \
    python3 \
    py3-pip \
    gstreamer \
    py3-gst \
    py3-gobject3 \
    gstreamer-tools \
    gst-plugins-base \
    gst-plugins-bad \
    gst-plugins-good \
    gst-plugins-ugly \
    py3-opencv \
    py3-gunicorn \
    py3-flask \
    ffmpeg \
    ffmpeg-libs \
    ffmpeg-libswscale

RUN apk add --no-cache gst-rtsp-server --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /

RUN mkdir /sessions && chmod 777 /sessions

COPY . .

RUN chmod +r -R /nvr /rtsp /flag.txt

EXPOSE 80
EXPOSE 554

USER appuser
CMD [ "ash", "/entrypoint.sh" ]