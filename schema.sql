--
-- PostgreSQL database: socialnetworksdb.
--
-- Table Profiles. It contains downloaded user data from the APIs.
-- The primary key will be the id_profile, which is a combination between the user
-- id and the social media source, along with the date in which the user data
-- were downloaded. In this way, the system will be able to insert many profiles
-- from a specific use but not in the same date.
--
CREATE TABLE public.profiles(
    id_profile SERIAL PRIMARY KEY,
    social_media varchar(30) NOT NULL,
    date DATE NOT NULL, 
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
    n_medias VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profiles OWNER TO lidia;

--
-- Table ProfilesEvolution. It will store the results of the analysis which
-- study the evolution of the number of followers, followings and posts during
-- a specific period of time. 
-- It has a foreign key to the Profiles table in order to check the if the studied 
-- profile exists.
--
CREATE TABLE public.profilesevolution(
    id_profile_evolution SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    n_week VARCHAR(10) NOT NULL,
    mean_followers VARCHAR(20) NOT NULL,
    mean_followings VARCHAR(20) NOT NULL,
    mean_medias VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profilesevolution OWNER TO lidia;

--
-- Table ProfilesActivity. It will store the results of the analysis which
-- study the activity of the user based on the number of posts they upload.
-- It has a foreign key to the Profiles table in order to check the if the studied 
-- profile exists.
--
CREATE TABLE public.profilesactivity(
    id_profile_activity SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    n_week VARCHAR(10) NOT NULL,
    mean_medias VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profilesactivity OWNER TO lidia;

--
-- Table Medias. It will contain the common data about the posts which have been
-- uploaded by an user in a specific social media.
--
CREATE TABLE public.medias(
    id_media_aut SERIAL PRIMARY KEY,
    id_profile INTEGER NOT NULL,
    uploaded_date VARCHAR(15),
    id_media VARCHAR(100),
    like_count VARCHAR(20),
    comment_count VARCHAR(20),
    date DATE,
    type VARCHAR(10),
    FOREIGN KEY (id_profile) REFERENCES profiles(id_profile) ON UPDATE CASCADE ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.medias OWNER TO lidia;

--
-- Table MediasEvolution. It will contain the analysis result from studying the 
-- number of likes and comments in several posts during a specific period of time.
--
CREATE TABLE public.mediasevolution(
    id_media_evolution SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    time VARCHAR(10) NOT NULL,
    mean_likes VARCHAR(20) NOT NULL,
    mean_comments VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.mediasevolution OWNER TO lidia;

--
-- Table MediaComments. It will contain the comments wrote on the posts of the
-- owner user. 
--
CREATE TABLE public.mediacomments(
    id_text SERIAL PRIMARY KEY,
    id_media_aut INTEGER NOT NULL,
    date DATE NOT NULL,
    original_text TEXT NOT NULL,
    preprocessed_text TEXT NOT NULL,
    author VARCHAR(50) NOT NULL,
    type VARCHAR(10) NOT NULL,
    FOREIGN KEY (id_media_aut) REFERENCES medias(id_media_aut) ON UPDATE CASCADE ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.mediacomments OWNER TO lidia;

--
-- Table MediaTitles. It will contain the titles of the posts which could have one,
-- like Instagram posts. This table will be the child of the MediaComments because
-- it's a specialization of this one.
--
CREATE TABLE public.mediatitles(
    CONSTRAINT mediatitles_pkey PRIMARY KEY (id_text)
) INHERITS (mediacomments);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.mediatitles OWNER TO lidia;

--
-- Table MediasPopularity. It will contain the analysis result from studying the 
-- popularity of the posts based on the number of likes and comments in a specific period of time.
--
CREATE TABLE public.mediaspopularity(
    id_media_popularity SERIAL PRIMARY KEY,
    id_media VARCHAR(100) NOT NULL,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    mean_likes VARCHAR(20) NOT NULL,
    mean_comments VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.mediaspopularity OWNER TO lidia;

--
-- Table UserBehaviours. It will save the number of likers and haters in a 
-- specific period of time based on the comment sentiment analysis.
--
CREATE TABLE public.userbehaviours(
    id_user_behaviour SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    time VARCHAR(10) NOT NULL,
    n_likers VARCHAR(20) NOT NULL,
    n_haters VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.userbehaviours OWNER TO lidia;

--
-- Table CommentSentiments. It will store the results of the sentiment analysis
-- for each comment in order to save the identified sentiment as well as its related
-- degree of confidence. 
--
CREATE TABLE public.commentsentiments(
    id_comment_sentiment SERIAL PRIMARY KEY,
    original_text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    degree REAL NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.commentsentiments OWNER TO lidia;

--
-- Table MediaTitles. It will contain the titles of the posts which could have one,
-- like Instagram posts. This table will be the child of the MediaComments because
-- it's a specialization of this one.
--
CREATE TABLE public.mediatitles(
    CONSTRAINT mediatitles_pkey PRIMARY KEY (id_text)
) INHERITS (mediacomments);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.mediatitles OWNER TO lidia;

--
-- Table TextSentiments. It will contain the number of positive, neutral and negative
-- sentiments as well as their related confidence degrees of a set of biographies,
-- titles or comments.
--
CREATE TABLE public.textsentiments(
    id_text_sentiment SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    type VARCHAR(10) NOT NULL,
    n_pos VARCHAR(20) NOT NULL,
    n_neu VARCHAR(20) NOT NULL,
    n_neg VARCHAR(20) NOT NULL,
    pos_degree VARCHAR(20) NOT NULL,
    neu_degree VARCHAR(20) NOT NULL,
    neg_degree VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.textsentiments OWNER TO lidia;