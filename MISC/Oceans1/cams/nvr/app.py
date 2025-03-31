from typing import List
from flask import (
    Flask,
    make_response,
    render_template,
    request,
    jsonify,
    g,
    redirect,
    url_for,
    session,
)
import tempfile
import os
import base64
import re
import http
import subprocess
import json

http.server.BaseHTTPRequestHandler.version_string = lambda _: "LionWatch 3.3.0rc2"

app = Flask(__name__)

app.secret_key = b"SecretSecretIveGotASecret"

with open("../conf.json", "r") as f:
    CONFIG = json.load(f)

PAT_IP = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d{1,5})?$")
PAT_SECID = re.compile(r"^[a-z]{7}$")

####


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))

    error_msg = None

    if request.method == "POST":
        error_msg = (
            "SPECIFIED USERNAME/PASSWORD COMBINATION INVALID -- INCIDENT REPORTED"
        )
        username = request.form.get("username")
        password = request.form.get("password")

        for user in CONFIG["users"]:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                return redirect(url_for("home"))

    return render_template("login.html", error_msg=error_msg)


@app.route("/cams", methods=["GET", "POST"])
def cams():
    if "user" not in session:
        return redirect(url_for("home"))

    if "id" in request.args:
        id = request.args["id"]
        for c in CONFIG["cameras"]:
            if str(c["id"]) != id:
                continue

            output = tempfile.mktemp(".jpg")

            user = [u for u in CONFIG["users"] if "admin" == u["username"]][0]

            size_flags = "" if c["name"] == "VAULT" else "-s 300x200"

            cmd = f'ffmpeg -y -nostats -loglevel 0 -rtsp_transport tcp -i "rtsp://{user["username"]}:{user["password"]}@127.0.0.1{c["endpoint"]}" {size_flags} -vf "fps=1,select=gte(t\\,2)" -f image2 -frames:v 1 {output} > /dev/null'
            os.system(cmd)

            try:
                with open(output, "rb") as f:
                    img = f.read()

                os.remove(output)

                resp = make_response(img)
                resp.headers.set("Content-Type", "image/jpeg")
                return resp
            except:
                return "Error"

        return "Invalid ID"

    error_msg = None

    available_cameras = [
        c for c in CONFIG["cameras"] if session["user"] in c["viewers"]
    ]

    return render_template("cams.html", error_msg=error_msg, cameras=available_cameras)


@app.route("/config", methods=["GET", "POST"])
def config():
    if session.get("user") not in ["it", "admin"]:
        return redirect(url_for("home"))

    net_message = ""
    preview_message = ""
    if request.method == "POST":
        if (
            request.form.get("ipAddress") is not None
            and request.form.get("securityStream") is not None
        ):
            try:
                assert bool(PAT_IP.match(request.form["ipAddress"]))
                assert not request.form["ipAddress"].startswith("127.") # block localhost
                assert bool(PAT_SECID.match(request.form["securityStream"]))

                path = os.path.join(
                    CONFIG["session_path"], f'{request.form["securityStream"]}.json'
                )

                assert os.path.isfile(path)

                with open(path, "w") as f:
                    f.write(request.form["ipAddress"])

                net_message = f'<p style="color: green">Changed IP to {request.form["ipAddress"]} successfully!</p>'
            except:
                net_message = '<p style="color: red">Invalid IP or security ID</p>'

        if request.form.get("previewIp") is not None:
            if session.get("user") != "admin":
                preview_message = (
                    '<script>alert("Must be admin to perform this action")</script>'
                )
            else:
                preview_ip = request.form["previewIp"]

                output = tempfile.mktemp(".jpg")
                cmd = f"ffmpeg -y -nostats -loglevel 0 -rtsp_transport tcp -i rtsp://{preview_ip} -s 300x200 -f image2 -frames:v 1 {output}"

                try:
                    subprocess.check_call(
                        cmd.split(),
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    with open(output, "rb") as f:
                        img = base64.b64encode(f.read()).decode()
                        preview_message = f'<img src="data:image/jpg;base64,{img}" />'
                except:
                    preview_message = (
                        f'<p style="color: red">Error running command {cmd}</p>'
                    )

                try:
                    os.remove(output)
                except:
                    pass

    return render_template(
        "config.html", net_message=net_message, preview_message=preview_message
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)
