#!/usr/bin/env python3

from typing import List
import gi
import cv2
import time
from datetime import datetime
import ctf
from dataclasses import dataclass
from threading import Thread, Lock
import logging
import os
import json
import string
import random

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib

with open('../conf.json', 'r') as f:
    CONFIG = json.load(f)

def putTextContourBW(im, text, org, fontFace, fontScale, color, thickness, lineType):
    for c, t in [((~color) & 0xff, thickness + 1), (color, thickness)]:
        im = cv2.putText(
            im,
            text=text,
            org=org,
            fontFace=fontFace,
            fontScale=fontScale,
            color=c,
            thickness=t,
            lineType=lineType
        )
    
    return im

Gst.init(None)
loop = GLib.MainLoop()

def image2cam(im, cam_name, width, height):
    im = cv2.resize(im, (width, height), \
        interpolation = cv2.INTER_LINEAR)

    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    im = putTextContourBW(
        im,
        text=cam_name,
        org=(10, 20),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.5,
        color=255,
        thickness=1,
        lineType=cv2.LINE_AA
    )

    im = putTextContourBW(
        im,
        text=f'dim:{width}x{height} host:{ctf.HOST}',
        org=(10, height - 10),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.25,
        color=255,
        thickness=1,
        lineType=cv2.LINE_AA
    )

    now = datetime.now()
    im = putTextContourBW(
        im,
        text=now.isoformat(),
        org=(width - 260, 20),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.5,
        color=255,
        thickness=1,
        lineType=cv2.LINE_AA
    )

    im = cv2.rectangle(
        im,
        pt1=(5,5),
        pt2=(width-5,height-5),
        color=255,
    )

    return im

class LiveFeed:
    def __init__(self, path, name, fps=None, width=None, height=None, loop=True):
        self.connecting = True
        self.cap =  cv2.VideoCapture(path) if os.path.isfile(path) else cv2.VideoCapture(path, cv2.CAP_GSTREAMER)
        self._frame = None
        self.frame_lock = Lock()

        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS)) if fps is None else fps
        if self.fps == 0:
            self.fps = 1

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) if width is None else width
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) if height is None else height

        self.name = name

        self.thread = Thread(target=self._loop, daemon=True)

        self.loop = loop
        self.started = False
        self.done = False
    
    def start(self):
        if not self.started:
            self.thread.start()
            self.started = True

            time.sleep(2.0) # grace time

            self.connecting = False

    def frame(self):
        with self.frame_lock:
            if self._frame is not None:
                return self._frame
                
        return None

    def _loop(self):
        while self.cap.isOpened() and not self.done:
            ret, frame = self.cap.read()
            if not ret and self.loop:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()

            if ret:
                with self.frame_lock:
                    self._frame = self._process_frame(frame)
            else:
                self.done = True
                break
            
            time.sleep(1/self.fps)
        
    def _process_frame(self, frame):
        return image2cam(frame, self.name, self.width, self.height)


class FlagLiveFeed(LiveFeed):
    def __init__(self, path, name, flag, fps=2, width=640, height=480):
        self.flag = flag
        super().__init__(path, name, fps, width, height)
    
    def _process_frame(self, frame):
        frame = super()._process_frame(frame)

        now = datetime.now()
        if (now.second - 3) % 10 < 2:
            frame = putTextContourBW(
                frame,
                text=self.flag,
                org=(0, self.height // 2),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=255,
                thickness=1,
                lineType=cv2.LINE_AA
            )
        
        return frame

class OfficeLiveFeed(LiveFeed):
    def __init__(self, path, name):
        super().__init__(path, name)
        self.width *= 2
        self.height *= 2
    
    def _process_frame(self, frame):
        cur_time = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 # msec

        frame = cv2.resize(frame, (self.width, self.height), \
            interpolation = cv2.INTER_LINEAR)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if 17.1 <= cur_time and cur_time <= 20:
            frame = cv2.rectangle(
                frame,
                pt1=(115 * 2,80 * 2),
                pt2=((115+30) * 2,(80+20) * 2),
                color=128,
                thickness=cv2.FILLED
            )

            credentials = [u for u in CONFIG['users'] if u['username'] == 'it'][0]
            text = f'Login Notes:\n{credentials["username"]}\n{credentials["password"]}'
            start_y = 83 * 2
            for line in text.splitlines():
                frame = putTextContourBW(
                    frame,
                    text=line,
                    org=(115 * 2, start_y),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.28,
                    color=255,
                    thickness=1,
                    lineType=cv2.LINE_AA
                )

                start_y += 15
            
        return frame

class SecurityLiveFeed(LiveFeed):
    def __init__(self, path, name):
        super().__init__(path, name, loop=False)
        
        self.host = None
        self.last_frame = None
        self.stream_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
        self.sesspath = os.path.join(CONFIG['session_path'], f'{self.stream_id}.json')
        with open(self.sesspath, 'w') as f:
            f.write('127.0.0.1')

        self.stream_thread = Thread(target=self._stream_update, daemon=True)
        self.stream = None
        self.breached = False
        self.timeout = 150 # 3rd party stream timeout
        self.end_time = None
    
    def _stream_update(self):
        while not self.done:
            with open(self.sesspath, 'r') as f:
                new_host = f.read()

            # only allow one modification to prevent reconnection
            if new_host != self.host and (self.host is None or self.host == '127.0.0.1'):
                print(f'swap! {self.host} -> {new_host}')
                self.host = new_host
                credentials = [u for u in CONFIG['users'] if u['username'] == 'admin'][0]
                self.stream = None
                self.stream = LiveFeed(
                    f'rtsp://{credentials["username"]}:{credentials["password"]}@{self.host}/vault.rtsp',
                    self.stream_id,
                    loop=False
                )

                self.stream.start()
            
            time.sleep(0.2)

    def _check_frame(self, frame):
        if self.breached:
            return

        if self.last_frame is not None:
            try:
                diff = cv2.absdiff(frame, self.last_frame)
                (_, diff) = cv2.threshold(diff, 20, 0, cv2.THRESH_TOZERO)
                cnt = cv2.countNonZero(diff)
                self.breached = cnt > 1500
            except:
                self.breached = True
        self.last_frame = frame

    def _process_frame(self, frame):
        frame = super()._process_frame(frame)
        if not self.stream_thread.is_alive():
            self.stream_thread.start()
        
        if self.end_time is None:
            self.end_time = time.time() + 35

        if self.timeout <= 0:
            self.breached = True

        stream_frame = None
        if self.stream is not None:
            if self.stream.connecting and self.host != '127.0.0.1':
                self.timeout -= 1
            elif self.stream.done:
                self.done = True
            else:
                stream_frame = self.stream.frame()
                self._check_frame(stream_frame)
        else:
            self.timeout -= 1

        frame = putTextContourBW(
            frame,
            text=f'SECURITY ROOM ID: {self.stream_id}',
            org=(10, 40),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=255,
            thickness=1,
            lineType=cv2.LINE_AA
        )

        top_left = (165, 165)
        width = 80
        height = 50
        if stream_frame is None:
            frame = cv2.rectangle(
                frame,
                pt1=top_left,
                pt2=(top_left[0] + width, top_left[1] + height),
                color=128,
                thickness=cv2.FILLED
            )
        else:
            stream_frame = cv2.resize(
                stream_frame,
                (width, height),
                interpolation=cv2.INTER_LINEAR
            )

            frame[top_left[1]:top_left[1] + height, top_left[0]:top_left[0] + width] = stream_frame

        if self.breached:
            frame = putTextContourBW(
                frame,
                text='SECURITY BREACH',
                org=(self.width // 4, self.height // 2 - 5),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.5,
                color=255,
                thickness=3,
                lineType=cv2.LINE_AA
            )
        elif self.end_time < time.time():
            frame = putTextContourBW(
                frame,
                text=CONFIG['flags'][1],
                org=(10, self.height // 2 - 5),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.6,
                color=255,
                thickness=1,
                lineType=cv2.LINE_AA
            )

        return frame

class CameraClient():
    def __init__(self, feed: LiveFeed, rtsp_media):
        self.feed = feed
        self.number_frames = 0
        self.duration = 1 / self.feed.fps * Gst.SECOND  # duration of a frame in nanoseconds
        rtsp_media.set_reusable(True)
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)

    def on_need_data(self, src, length):
        if self.feed.done:
            retval = src.emit('end-of-stream')
        else:
            data = self.feed.frame()
            data = data.tobytes() if data is not None else b''
            buf = Gst.Buffer.new_allocate(None, len(data), None)
            buf.fill(0, data)
            buf.duration = self.duration
            timestamp = self.number_frames * self.duration
            buf.pts = buf.dts = int(timestamp)
            buf.offset = timestamp
            self.number_frames += 1
            retval = src.emit('push-buffer', buf)
        # print('pushed buffer, cam {}, frame {}, duration {} ns, durations {} s'.format(self.feed.name, self.number_frames,
        #                                                                         self.duration,
        #                                                                         self.duration / Gst.SECOND))

        if retval != Gst.FlowReturn.OK:
            print(retval)

class CameraFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, feed_ctor, multicast=False, **properties):
        super(CameraFactory, self).__init__(**properties)
        self.feed_ctor = feed_ctor
        self.multicast = multicast
        if self.multicast:
            self.feed = self.feed_ctor()

        self.clients = []

        temp_feed = self.feed_ctor()
        self.launch_string = 'appsrc name=source do-timestamp=true is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=GRAY8,width={},height={},framerate={}/1 ' \
                             '! videoconvert n-threads=3 ! video/x-raw,format=I420 ' \
                             '! x264enc bitrate=512 tune=zerolatency speed-preset=veryfast threads=3 sliced-threads=true ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96' \
                             .format(temp_feed.width, temp_feed.height, temp_feed.fps)
        
        del temp_feed

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)
    
    def do_configure(self, rtsp_media):
        feed = self.feed if self.multicast else self.feed_ctor()
        feed.start()
        self.clients.append(CameraClient(feed, rtsp_media))
    
    def set_roles(self, roles):
        permissons = GstRtspServer.RTSPPermissions()
        for role in roles:
            permissons.add_role(role)
            permissons.add_permission_for_role(role, "media.factory.access", True)
            permissons.add_permission_for_role(role, "media.factory.construct", True)
        self.set_permissions(permissons)	

@dataclass
class CameraInfo:
    factory: CameraFactory
    endpoint: str
    viewers: List[str]

class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)

        auth = GstRtspServer.RTSPAuth()
        
        for user in CONFIG['users']:
            token = GstRtspServer.RTSPToken()
            token.set_string("media.factory.role", user['username'])
            basic = GstRtspServer.RTSPAuth.make_basic(user['username'], user['password'])
            auth.add_basic(basic, token)
		    
        self.set_auth(auth)

        self.factories = []
        for camera in CONFIG['cameras']:
            fullname = '%s\nCAM%02d' % (camera['name'], camera['id'])
            multicast = True
            if camera['name'] == 'SLOTS':
                feed = lambda source=camera['source'], fullname=fullname: FlagLiveFeed(source, fullname, CONFIG['flags'][0])
            elif camera['name'] == 'OFFICE':
                feed = lambda source=camera['source'], fullname=fullname: OfficeLiveFeed(source, fullname)
            elif camera['name'] == 'SECURITY':
                multicast = False
                feed = lambda source=camera['source'], fullname=fullname: SecurityLiveFeed(source, fullname)
            else:
                multicast = False
                feed = lambda source=camera['source'], fullname=fullname: LiveFeed(source, fullname, loop=False)

            factory = CameraFactory(feed, multicast)

            factory.set_shared(True)
            factory.set_roles(camera['viewers'])
            self.get_mount_points().add_factory(camera['endpoint'], factory)
            self.factories.append(factory)

        self.set_service(str('554'))
        self.attach(None)

    def start(self):
        loop.run()

if __name__ == '__main__':
    server = GstServer()
    server.start()