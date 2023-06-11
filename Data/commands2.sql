-- SQLite

-- DROP TABLE userdata;

-- CREATE TABLE userdata (
-- userid INTEGER PRIMARY KEY AUTOINCREMENT,
-- username varchar(20) UNIQUE NOT NULL, 
-- name varchar(20) NOT NULL,
-- email varchar(30) NOT NULL,
-- password varchar(256) NOT NULL,
-- token varchar(256) NOT NULL);

-- DROP TABLE admindata;

-- CREATE TABLE admindata (
-- adminid INTEGER PRIMARY KEY AUTOINCREMENT,
-- adminname varchar(20) UNIQUE NOT NULL, 
-- name varchar(20) NOT NULL,
-- email varchar(30) NOT NULL,
-- password varchar(256) NOT NULL,
-- token varchar(256) NOT NULL);

-- DROP TABLE showdata;

-- CREATE TABLE showdata(showid INTEGER PRIMARY KEY AUTOINCREMENT,
-- name varchar(40) NOT NULL,
-- image_url varchar(50),
-- rating SHORT NOT NULL,
-- no_of_ratings SHORT DEFAULT 0,
-- description varchar(150) NOT NULL,
-- tags varchar(200),
-- release TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);

-- DROP TABLE venuedata;

-- CREATE TABLE venuedata(venueid INTEGER PRIMARY KEY AUTOINCREMENT,
-- name varchar(30) NOT NULL, 
-- city_town varchar(20) NOT NULL, 
-- location_desc varchar(50) NOT NULL, 
-- coordinates varchar(30) NOT NULL, 
-- rating SHORT NOT NULL,
-- no_of_rating SHORT NOT NULL DEFAULT 0);

-- DROP TABLE scheduledata;

-- CREATE TABLE scheduledata(scheduleid INTEGER PRIMARY KEY AUTOINCREMENT,
-- venue_id INTEGER NOT NULL,
-- show_id INTEGER NOT NULL,
-- language varchar(20) NOT NULL,
-- total_seats SHORT NOT NULL,
-- booked_seats SHORT NOT NULL DEFAULT 0,
-- start_time TIMESTAMP NOT NULL,
-- end_time TIMESTAMP NOT NULL,
-- price SHORT NOT NULL,
-- FOREIGN KEY(venue_id) REFERENCES venuedata(venueid),
-- FOREIGN KEY(show_id) REFERENCES showdata(showid)
-- );

-- DROP TABLE bookingdata;

-- CREATE TABLE bookingdata(bookingid INTEGER PRIMARY KEY AUTOINCREMENT,
-- userid INTEGER NOT NULL,
-- no_of_seats SHORT NOT NULL,
-- schedule_id INTEGER NOT NULL,
-- FOREIGN KEY(userid) REFERENCES userdata(userid),
-- FOREIGN KEY(schedule_id) REFERENCES scheduledata(scheduleid)
-- );

-- DROP TABLE filters;

-- CREATE TABLE filters(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     tagname varchar(30) NOT NULL,
--     tagtype varchar(30) NOT NULL
-- );

-- add column show_rating and 
-- venue_rating to booking data table

-- ALTER TABLE bookingdata ADD COLUMN show_rating SHORT;
-- ALTER TABLE bookingdata ADD COLUMN venue_rating SHORT;