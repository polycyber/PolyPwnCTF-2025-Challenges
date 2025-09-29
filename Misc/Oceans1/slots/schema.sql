CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    balance REAL NOT NULL
);

CREATE TABLE streams (
    id TEXT PRIMARY KEY,
    endpoint TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NO NULL
);

INSERT INTO streams VALUES
    ('13a1169d-52e1-4b88-ba37-ba6f910a1d25', '/slots.rtsp', 'operator', 'dQw4w9WgXcQ');