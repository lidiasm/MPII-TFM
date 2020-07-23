--
-- PostgreSQL database: socialnetworksdb.
--
-- Table profiles which stores user personal data related to their social media accounts.
-- The field social_media indicates the social media source which the user profile came from.
-- In this way, we can analyze if the users have different behaviours in different social medias.
--
CREATE TABLE public.profiles (
    username VARCHAR(20) NOT NULL,
    date VARCHAR(20) NOT NULL,
    name VARCHAR(100),
    userid bigint NOT NULL,
    biography VARCHAR(200),
    gender VARCHAR(20),
    profile_pic VARCHAR(400),
    location VARCHAR(100),
    birthday VARCHAR(30),
    date_joined VARCHAR(20),
    n_followers INTEGER NOT NULL,
    n_followings INTEGER NOT NULL,
    n_posts INTEGER NOT NULL,
    social_media VARCHAR(20) NOT NULL
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profiles OWNER TO lidia;

--
-- The Primary Key is made up of two fields: the username and the date in which
--  the data has been inserted. In this way, multiple data of a same user can
--  be stored in order to keep several records of them.
--
ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profile_pkey PRIMARY KEY (username, date);
    
--
-- Table contacts which stores the followers and followings of an user. In order
-- to determinate wether the contact user is follower, following or both there is
-- a field called relationship which could be one of the three previous values (follower, following, both).
--
-- This table also has a foreign key to the profiles table in order to relate the
-- the contacts with the user who follow, is following or bot.
--
CREATE TABLE contacts(
    id_contact SERIAL PRIMARY KEY, 
    username VARCHAR(20) NOT NULL,
    date VARCHAR(20) NOT NULL,
    contact_username VARCHAR(20) NOT NULL, 
    relationship VARCHAR(20) NOT NULL,
    social_media VARCHAR(20) NOT NULL,
    FOREIGN KEY (username, date) REFERENCES profiles(username,date)
);
    
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.contacts OWNER TO lidia;

--
-- Table posts which stores the main fields of each post: its id, the number of
-- likes and the number of comments. 
--
CREATE TABLE posts(
    id_post VARCHAR(100) PRIMARY KEY, 
    username VARCHAR(20) NOT NULL,
    date VARCHAR(20) NOT NULL,
    like_count INTEGER NOT NULL CHECK (like_count>=0), 
    com_count INTEGER NOT NULL CHECK (com_count>=0),
    social_media VARCHAR(20) NOT NULL,
    FOREIGN KEY (username, date) REFERENCES profiles(username,date)
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.posts OWNER TO lidia;

--
-- Table likers in which the users who liked posts are stored as well as the number
-- of posts they liked. 
--
CREATE TABLE likers(
    id_liker VARCHAR(100) PRIMARY KEY, 
    username VARCHAR(20) NOT NULL,
    date VARCHAR(20) NOT NULL,
    liker_username VARCHAR(20) NOT NULL, 
    n_likes INTEGER NOT NULL CHECK (n_likes>=0),
    social_media VARCHAR(20) NOT NULL,
    FOREIGN KEY (username, date) REFERENCES profiles(username,date)
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.likers OWNER TO lidia;
    
    
-- Table comments in which the post comments are stored. It contains fields like
--  * The id of the related post. 
--  * The username who wrote it.
--  * The text of the comment.
--
CREATE TABLE comments(
    id_comment VARCHAR(100) PRIMARY KEY, 
    username VARCHAR(20) NOT NULL,
    date VARCHAR(20) NOT NULL,
    id_post VARCHAR(100) NOT NULL,
    comment_username VARCHAR(20) NOT NULL, 
    text VARCHAR(500) NOT NULL,
    social_media VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_post) REFERENCES posts(id_post),
    FOREIGN KEY (username, date) REFERENCES profiles(username,date)
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.comments OWNER TO lidia;

-- Tables to perform the tests which check the behaviour of the Single Source
-- of Truth which is the class PostgreSQL. Both of them are similar to 'profiles'
-- and 'contacts' tables in order to reproduce the operations which will be done
-- in the real tables.
CREATE TABLE public.test1 (
    username VARCHAR(20) NOT NULL,
    date VARCHAR(20) NOT NULL,
    name VARCHAR(100),
    userid bigint NOT NULL,
    biography VARCHAR(200),
    gender VARCHAR(20),
    profile_pic VARCHAR(400),
    location VARCHAR(100),
    birthday VARCHAR(30),
    date_joined VARCHAR(20),
    n_followers INTEGER NOT NULL,
    n_followings INTEGER NOT NULL,
    n_posts INTEGER NOT NULL,
    social_media VARCHAR(20) NOT NULL
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.test1 OWNER TO lidia;

CREATE TABLE test2(
    id_contact SERIAL PRIMARY KEY, 
    username VARCHAR(20) NOT NULL,
    date VARCHAR(20) NOT NULL,
    contact_username VARCHAR(20) NOT NULL, 
    relationship VARCHAR(20) NOT NULL,
    social_media VARCHAR(20) NOT NULL,
    FOREIGN KEY (username, date) REFERENCES profiles(username,date)
);
    
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.test2 OWNER TO lidia;