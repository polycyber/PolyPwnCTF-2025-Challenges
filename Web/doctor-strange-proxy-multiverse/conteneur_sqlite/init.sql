CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS universes (id SERIAL PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS secrets_of_the_universe (id SERIAL PRIMARY KEY, secret TEXT NOT NULL);
INSERT INTO users (username, password) VALUES ('admin', 'godoftheuniverse');
INSERT INTO universes (name) VALUES
    ('Zyphora Nexus'), ('Kalon Expanse'), ('Virellis Cluster'),
    ('Solvian Dominion'), ('Xerathis Continuum'), ('Aetheris Convergence'),
    ('Zepharion Reach'), ('Uthraxis Zone'),
    ('Quantos Rift'), ('Nebulon Verge'), ('Celestia Prime'),
    ('Andromeda Veil'), ('Orion''s Span'), ('Cygnus Reach'),
    ('Draco''s Maw'), ('Lyra''s Song'), ('Pegasus Nebula'),
    ('Centauri Frontier'), ('Sirius Sector'), ('Vega Gradient'),
    ('Altair Divide'), ('Polaris Domain'), ('Cassiopeia Crown'),
    ('Gemini Traverse'), ('Leo''s Labyrinth'), ('Aquila''s Ascent'),
    ('Scorpius Depths'), ('Sagittarius Spiral'), ('Taurus Threshold'),
    ('Aries Anomaly'), ('Pisces Paradox'), ('Capricorn Crest'),
    ('Virgo''s Vortex'), ('Libra''s Lineage'), ('Cancer''s Cradle'),
    ('Ophiuchus Orbit'), ('Cetus Chasm');
INSERT INTO secrets_of_the_universe (secret) VALUES ('polycyber{polyverse_8d113abd}');