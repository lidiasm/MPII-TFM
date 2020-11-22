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
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    mean_followers VARCHAR(20) NOT NULL,
    mean_followings VARCHAR(20) NOT NULL,
    mean_medias VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profilesevolution OWNER TO lidia;

--
-- Table Profiles_ProfilesEvolution which represents the many-to-many relationship
-- between the profile evolution analysis and the profiles themselves. Each profile
-- could participate in several analysis, and one analysis will study many profiles.
--
-- If some of the profiles which has participated in one a analysis is updated/deleted,
-- then the analysis will be updated/removed too.
--
CREATE TABLE public.profiles_profilesevolution(
    id_profile int REFERENCES profiles (id_profile) ON UPDATE CASCADE ON DELETE CASCADE,
    id_profile_evolution int REFERENCES profilesevolution (id_profile_evolution) ON UPDATE CASCADE,
    CONSTRAINT profiles_profilesevolution_pkey PRIMARY KEY (id_profile, id_profile_evolution)
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profiles_profilesevolution OWNER TO lidia;

--
-- Table ProfilesActivity. It will store the results of the analysis which
-- study the activity of the user based on the number of posts they upload.
-- It has a foreign key to the Profiles table in order to check the if the studied 
-- profile exists.
--
CREATE TABLE public.profilesactivity(
    id_profile_activity SERIAL PRIMARY KEY,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    mean_medias VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profilesactivity OWNER TO lidia;

--
-- Table Profiles_ProfilesActivity which represents the many-to-many relationship
-- between the profile activity analysis and the profiles themselves. Each profile
-- could participate in several analysis, and one analysis will study many profiles.
--
-- If some of the profiles which has participated in one a analysis is updated/deleted,
-- then the analysis will be updated/removed too.
--
CREATE TABLE public.profiles_profilesactivity(
    id_profile int REFERENCES profiles (id_profile) ON UPDATE CASCADE ON DELETE CASCADE,
    id_profile_activity int REFERENCES profilesactivity (id_profile_activity) ON UPDATE CASCADE,
    CONSTRAINT profiles_profilesactivity_pkey PRIMARY KEY (id_profile, id_profile_activity)
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.profiles_profilesactivity OWNER TO lidia;

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
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    mean_likes VARCHAR(20) NOT NULL,
    mean_comments VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.mediasevolution OWNER TO lidia;

--
-- Table Medias_MediasEvolution. It contains the relationships between the 
-- performed Medias Evolution analysis and the posts which have participated.
--
CREATE TABLE public.medias_mediasevolution(
    id_media_aut int REFERENCES medias (id_media_aut) ON UPDATE CASCADE ON DELETE CASCADE,
    id_media_evolution int REFERENCES mediasevolution (id_media_evolution) ON UPDATE CASCADE,
    CONSTRAINT medias_mediasevolution_pkey PRIMARY KEY (id_media_aut, id_media_evolution)
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.medias_mediasevolution OWNER TO lidia;

--
-- Table MediasPopularity. It will contain the analysis result from studying the 
-- popularity of the posts based on the number of likes and comments in a specific period of time.
--
CREATE TABLE public.mediaspopularity(
    id_media_popularity SERIAL PRIMARY KEY,
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
-- Table Medias_MediasPopularity. It contains the relationships between the 
-- performed Medias Popularity analysis and the posts which have participated.
--
CREATE TABLE public.medias_mediaspopularity(
    id_media_aut int REFERENCES medias (id_media_aut) ON UPDATE CASCADE ON DELETE CASCADE,
    id_media_popularity int REFERENCES mediaspopularity (id_media_popularity) ON UPDATE CASCADE,
    CONSTRAINT medias_mediaspopularity_pkey PRIMARY KEY (id_media_aut, id_media_popularity)
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.medias_mediaspopularity OWNER TO lidia;

--
-- Table MediaComments. It will contain the comments wrote on the posts of the
-- owner user. 
--
CREATE TABLE public.mediacomments(
    id_text SERIAL PRIMARY KEY,
    id_media_aut INTEGER NOT NULL,
    date DATE NOT NULL,
    text TEXT NOT NULL,
    author VARCHAR(50) NOT NULL,
    type VARCHAR(10),
    FOREIGN KEY (id_media_aut) REFERENCES medias(id_media_aut) ON UPDATE CASCADE ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.mediacomments OWNER TO lidia;

--
-- Table SentimentAnalysis. It will contain the sentiment analysis performed on a
-- post comment with the degree of the positive, neutral and negative sentiment as
-- well as the winner sentiment.
--
CREATE TABLE public.sentimentanalysis(
    id_text INTEGER PRIMARY KEY,
    pos_degree REAL NOT NULL,
    neu_degree REAL NOT NULL,
    neg_degree REAL NOT NULL,
    sentiment VARCHAR(10),
    FOREIGN KEY (id_text) REFERENCES mediacomments(id_text) ON UPDATE CASCADE ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.sentimentanalysis OWNER TO lidia;

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
-- Table TitleSentimentAnalysis. It will contain the sentiment analysis performed on a
-- post title with the degree of the positive, neutral and negative sentiment as
-- well as the winner sentiment.
--
CREATE TABLE public.titlesentimentanalysis(
    id_text INTEGER PRIMARY KEY,
    pos_degree REAL NOT NULL,
    neu_degree REAL NOT NULL,
    neg_degree REAL NOT NULL,
    sentiment VARCHAR(10),
    FOREIGN KEY (id_text) REFERENCES mediatitles(id_text) ON UPDATE CASCADE ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.titlesentimentanalysis OWNER TO lidia;