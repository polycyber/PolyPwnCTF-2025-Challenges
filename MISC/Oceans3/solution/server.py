#!/usr/bin/env python

import os
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

loop = GLib.MainLoop()
Gst.init(None)

class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        print(url)
        pipeline = f"filesrc location={src_file} ! decodebin ! videorate max-rate=1 ! videoconvert ! video/x-raw,format=I420 ! x264enc bitrate=4096 tune=zerolatency speed-preset=ultrafast threads=3 sliced-threads=true insert-vui=1 key-int-max=30 ! rtph264pay name=pay0 pt=96"
        print ("Element created: " + pipeline)
        return Gst.parse_launch(pipeline)

    def set_roles(self, roles):
        permissons = GstRtspServer.RTSPPermissions()
        for role in roles:
            permissons.add_role(role)
            permissons.add_permission_for_role(role, "media.factory.access", True)
            permissons.add_permission_for_role(role, "media.factory.construct", True)
        print(permissons)
        self.set_permissions(permissons)	

class GstreamerRtspServer():
    def __init__(self):
        self.rtspServer = GstRtspServer.RTSPServer()
        factory = TestRtspMediaFactory()
        factory.set_shared(True)

        auth = GstRtspServer.RTSPAuth()
        token = GstRtspServer.RTSPToken()
        token.set_string('media.factory.role', "user")
        basic = GstRtspServer.RTSPAuth.make_basic("user", "password")
        auth.add_basic(basic, token)
        self.rtspServer.set_auth(auth)

        factory.set_roles(['user'])

        mountPoints = self.rtspServer.get_mount_points()
        mountPoints.add_factory('/vault.rtsp', factory)
    
        self.rtspServer.attach(None)

if __name__ == '__main__':
    src_file = 'vault_static.mp4'
    s = GstreamerRtspServer()
    loop.run()