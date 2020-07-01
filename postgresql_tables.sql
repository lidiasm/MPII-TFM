--
-- PostgreSQL database: socialnetworksdb.
--
-- Table profiles which stores user personal data related to their social media accounts.
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
    n_medias INTEGER NOT NULL,
    social_media VARCHAR(20) NOT NULL
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profiles OWNER TO lidia;

--
-- The Primary Key is made up of two fields: the username and the date in which
--  the row has been inserted. In this way, multiple data of a same user can
--  be stored in order to keep many records of them.
--
ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profile_pkey PRIMARY KEY (username, date);
    
--
-- Table followers, in which the usernames of the users who are followed by an
--  user are stored. Its Primary Key is an auto-increment id number.
--
CREATE TABLE followers(
    id_follower SERIAL PRIMARY KEY, 
    id_profile VARCHAR(20) NOT NULL, 
    username VARCHAR(20) NOT NULL,
    social_media VARCHAR(20) NOT NULL
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.followers OWNER TO lidia;

--
-- Table followings, in which the usernames of the followers of an user are stored.
--  Its Primary Key is an auto-increment id number.
--
CREATE TABLE followings(
    id_following SERIAL PRIMARY KEY, 
    id_profile VARCHAR(20) NOT NULL, 
    username VARCHAR(20) NOT NULL,
    social_media VARCHAR(20) NOT NULL
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.followings OWNER TO lidia;

--
-- Table posts in which the media items of the users are stored. It contains
--  fields such as the id of the post, the username who is the owner of the 
--  post, the number of likes and comments about it.
--
-- The Primary Key is the id media returned by the API.
--
CREATE TABLE posts(
    id_media VARCHAR(100) PRIMARY KEY, 
    username VARCHAR(20) NOT NULL, 
    like_count INTEGER NOT NULL CHECK (like_count>=0), 
    com_count INTEGER NOT NULL CHECK (com_count>=0),
    social_media VARCHAR(20) NOT NULL
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.posts OWNER TO lidia;

--
-- Table likers in which the users who liked a post of the another user are stored
--  along with the number of posts liked. 
--
CREATE TABLE likers(
    id_liker SERIAL PRIMARY KEY, 
    id_profile VARCHAR(20) NOT NULL, 
    username VARCHAR(20) NOT NULL, 
    n_likes INTEGER NOT NULL CHECK (n_likes>=0),
    social_media VARCHAR(20) NOT NULL
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.likers OWNER TO lidia;

--
-- Table comments in which the post comments are stored. It contains fields
--  such as the text of the comment, the user who wrote it, the post in which
--  has been written (foreign key) and the user who is the owner of the post.
--
CREATE TABLE comments(
    id_comment SERIAL PRIMARY KEY, 
    id_profile VARCHAR(20) NOT NULL, 
    id_media VARCHAR(100) NOT NULL REFERENCES posts(id_media), 
    username VARCHAR(20) NOT NULL, 
    text VARCHAR(500) NOT NULL,
    social_media VARCHAR(20) NOT NULL
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.comments OWNER TO lidia;
