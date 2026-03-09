DROP TABLE IF EXISTS admin_users;
DROP TABLE IF EXISTS portfolio;
DROP TABLE IF EXISTS bookings;

CREATE TABLE admin_users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
);

CREATE TABLE portfolio (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  event_name TEXT,
  description TEXT NOT NULL,
  image_filename TEXT NOT NULL
);

CREATE TABLE bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  shoot_type TEXT NOT NULL,
  video_style TEXT,
  message TEXT NOT NULL
);