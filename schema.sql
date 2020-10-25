--
-- PostgreSQL database: socialnetworksdb.
--
-- Table Profiles. It contains downloaded user data from the APIs.
--
CREATE TABLE public.profiles(
    id_profile VARCHAR(50) PRIMARY KEY,
    social_media varchar(30) NOT NULL,
    date VARCHAR(20) NOT NULL, 
    userid VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    biography VARCHAR(200) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    profile_pic VARCHAR(500) NOT NULL,
    location VARCHAR(30) NOT NULL,
    birthday VARCHAR(20) NOT NULL,
    date_joined VARCHAR(20) NOT NULL,
    n_followers VARCHAR(20) NOT NULL,
    n_followings VARCHAR(20) NOT NULL,
    n_posts VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profiles OWNER TO lidia;

--
-- Table Contacts. It contains the relationship between the studied user
-- and their followers and followings.
--
CREATE TABLE public.contacts(
    id_contact SERIAL PRIMARY KEY,
    id_profile VARCHAR(50) NOT NULL,
    social_media varchar(30) NOT NULL,
    date VARCHAR(20) NOT NULL, 
    follower VARCHAR(50) NOT NULL,
    following VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_profile) REFERENCES profiles(id_profile) ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.contacts OWNER TO lidia;

--
-- Table Posts. It contains user data like the post information downloaded
-- from the APIs. 
--
CREATE TABLE public.posts(
    id_post VARCHAR(50) PRIMARY KEY,
    id_profile VARCHAR(50) NOT NULL,
    social_media varchar(30) NOT NULL,
    date VARCHAR(20) NOT NULL, 
    uploaded_date VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_profile) REFERENCES profiles(id_profile) ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.posts OWNER TO lidia;

--
-- Table Users. It contains data from the users who interact with the studied user posts
--
CREATE TABLE public.users(
    id_user VARCHAR(50) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    social_media varchar(30) NOT NULL,
    date VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.users OWNER TO lidia;

--
-- Table CommonInteractions. It contains the interaction data from the posts of 
-- a specific user, like comment count and likes.
--
CREATE TABLE public.commoninteractions(
    id_interaction SERIAL PRIMARY KEY,
    id_post VARCHAR(50) NOT NULL,
    id_user VARCHAR(50) NOT NULL,
    has_liked BOOLEAN NOT NULL,
    comment_count VARCHAR(20) NOT NULL,
    is_common BOOLEAN NOT NULL,
    FOREIGN KEY (id_post) REFERENCES posts(id_post) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.commoninteractions OWNER TO lidia;

--
-- Table TwitterInteractions. This table is the child from the previous table,
-- so it will have its data as well as the specific interactions from Twitter,
-- such as retweets and quotes.
--
CREATE TABLE public.twitterinteractions(
    has_retweeted BOOLEAN NOT NULL,
    has_quoted BOOLEAN NOT NULL
) INHERITS (commoninteractions);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.twitterinteractions OWNER TO lidia;

--
-- Table CommonTexts. It contains the text which all posts from different social
-- media can have: comments. 
--
CREATE TABLE public.commontexts(
    id_text SERIAL PRIMARY KEY,
    id_post VARCHAR(50) NOT NULL,
    id_user VARCHAR(50) NOT NULL,
    social_media varchar(30) NOT NULL,
    date VARCHAR(20) NOT NULL,
    text VARCHAR(300) NOT NULL,
    is_common BOOLEAN NOT NULL,
    FOREIGN KEY (id_post) REFERENCES posts(id_post) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.commontexts OWNER TO lidia;

--
-- Table PostTitles. It contains the titles from the posts who have them, like
-- Instagram. This table will be one of the children of the previous table.
--
CREATE TABLE public.posttitles(
) INHERITS (commontexts);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.posttitles OWNER TO lidia;

--
-- Table PostTexts. It contains the text of the content of a post, in case it
-- has it, like Twitter. This table will be the second child of the table CommonTexts
--
CREATE TABLE public.posttexts(
) INHERITS (commontexts);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.posttexts OWNER TO lidia;