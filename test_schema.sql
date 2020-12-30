-- 
-- Table TestParent. This table will be used to test the methods of the class
-- PostgreDB.
--
CREATE TABLE public.testparent(
    id VARCHAR(50) PRIMARY KEY,
    is_parent BOOLEAN NOT NULL,
    name VARCHAR(20) NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testparent OWNER TO lidia;

--
-- Table TestChild. This table will be used to test the methods of the class
-- PostgreDB. Besides that, it will be the child of the previous table to test
-- the relationship.
--
CREATE TABLE public.testchild(
    CONSTRAINT testchild_pkey PRIMARY KEY (id)
) INHERITS (testparent);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testchild OWNER TO lidia;

--
-- Table TestFK. This table will be used to test the methods of the class 
-- PostgreDB. In this case, the table will have a foreign key to the TestParent 
-- table in order to test that property.
--
CREATE TABLE public.testfk(
    id_test_fk SERIAL PRIMARY KEY,
    id VARCHAR(50) NOT NULL,
    field_one VARCHAR(20) NOT NULL,
    FOREIGN KEY (id) REFERENCES testparent(id) ON DELETE CASCADE
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testfk OWNER TO lidia;

--
-- Table Profiles. It contains downloaded user data from the APIs.
-- The primary key will be the id_profile, which is a combination between the user
-- id and the social media source, along with the date in which the user data
-- were downloaded. In this way, the system will be able to insert many profiles
-- from a specific use but not in the same date.
--
CREATE TABLE public.testprofiles(
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
ALTER TABLE public.testprofiles OWNER TO lidia;

--
-- Table ProfilesEvolution. It will store the results of the analysis which
-- study the evolution of the number of followers, followings and posts during
-- a specific period of time. 
-- It has a foreign key to the Profiles table in order to check the if the studied 
-- profile exists.
--
CREATE TABLE public.testprofilesevolution(
    id_profile_evolution SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    time VARCHAR(10) NOT NULL,
    mean_followers INTEGER NOT NULL,
    mean_followings INTEGER NOT NULL,
    mean_medias INTEGER NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testprofilesevolution OWNER TO lidia;

--
-- Table ProfilesActivity. It will store the results of the analysis which
-- study the activity of the user based on the number of posts they upload.
-- It has a foreign key to the Profiles table in order to check the if the studied 
-- profile exists.
--
CREATE TABLE public.testprofilesactivity(
    id_profile_activity SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    time VARCHAR(10) NOT NULL,
    mean_medias INTEGER NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testprofilesactivity OWNER TO lidia;

--
-- Table Medias. It will contain the common data about the posts which have been
-- uploaded by an user in a specific social media.
--
CREATE TABLE public.testmedias(
    id_media_aut SERIAL PRIMARY KEY,
    id_profile INTEGER NOT NULL,
    uploaded_date VARCHAR(15),
    id_media VARCHAR(100),
    like_count VARCHAR(20),
    comment_count VARCHAR(20),
    date DATE,
    type VARCHAR(10),
    FOREIGN KEY (id_profile) REFERENCES testprofiles(id_profile) ON UPDATE CASCADE ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testmedias OWNER TO lidia;

--
-- Table MediasEvolution. It will contain the analysis result from studying the 
-- number of likes and comments in several posts during a specific period of time.
--
CREATE TABLE public.testmediasevolution(
    id_media_evolution SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    time VARCHAR(10) NOT NULL,
    mean_likes INTEGER NOT NULL,
    mean_comments INTEGER NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testmediasevolution OWNER TO lidia;

--
-- Table MediaComments. It will contain the comments wrote on the posts of the
-- owner user. 
--
CREATE TABLE public.testmediacomments(
    id_text SERIAL PRIMARY KEY,
    id_media_aut INTEGER NOT NULL,
    date DATE NOT NULL,
    original_text TEXT NOT NULL,
    preprocessed_text TEXT NOT NULL,
    author VARCHAR(50) NOT NULL,
    type VARCHAR(10),
    FOREIGN KEY (id_media_aut) REFERENCES testmedias(id_media_aut) ON UPDATE CASCADE ON DELETE CASCADE
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testmediacomments OWNER TO lidia;

--
-- Table MediaTitles. It will contain the titles of the posts which could have one,
-- like Instagram posts. This table will be the child of the MediaComments because
-- it's a specialization of this one.
--
CREATE TABLE public.testmediatitles(
    CONSTRAINT testmediatitles_pkey PRIMARY KEY (id_text)
) INHERITS (testmediacomments);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testmediatitles OWNER TO lidia;

--
-- Table MediasPopularity. It will contain the analysis result from studying the 
-- popularity of the posts based on the number of likes and comments in a specific period of time.
--
CREATE TABLE public.testmediaspopularity(
    id_media_popularity SERIAL PRIMARY KEY,
    id_media VARCHAR(100) NOT NULL,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    mean_likes INTEGER NOT NULL,
    mean_comments INTEGER NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testmediaspopularity OWNER TO lidia;

--
-- Table TextSentiments. It will contain the number of positive, neutral and negative
-- sentiments as well as their related confidence degrees of a set of biographies,
-- titles or comments.
--
CREATE TABLE public.testtextsentiments(
    id_text_sentiment SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    type VARCHAR(10) NOT NULL,
    n_pos INTEGER NOT NULL,
    n_neu INTEGER NOT NULL,
    n_neg INTEGER NOT NULL,
    pos_degree REAL NOT NULL,
    neu_degree REAL NOT NULL,
    neg_degree REAL NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testtextsentiments OWNER TO lidia;

--
-- Table CommentSentiments. It will store the results of the sentiment analysis
-- for each comment in order to save the identified sentiment as well as its related
-- degree of confidence. 
--
CREATE TABLE public.testcommentsentiments(
    id_comment_sentiment SERIAL PRIMARY KEY,
    original_text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    degree REAL NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testcommentsentiments OWNER TO lidia;

--
-- Table UserBehaviours. It will save the number of likers and haters in a 
-- specific period of time based on the comment sentiment analysis.
--
CREATE TABLE public.testuserbehaviours(
    id_user_behaviour SERIAL PRIMARY KEY,
    id_user VARCHAR(50) NOT NULL,
    date_ini DATE NOT NULL,
    date_fin DATE NOT NULL,
    time VARCHAR(10) NOT NULL,
    n_likers INTEGER NOT NULL,
    n_haters INTEGER NOT NULL
);
-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.testuserbehaviours OWNER TO lidia;