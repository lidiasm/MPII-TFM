--
-- PostgreSQL database dump
--
CREATE TABLE public.profile (
    username character varying(20) NOT NULL,
    date character varying(20) NOT NULL,
    name character varying(100),
    userid bigint NOT NULL,
    biography character varying(200),
    gender character varying(20),
    profile_pic character varying(400),
    location character varying(100),
    birthday character varying(30),
    date_joined character varying(20),
    n_followers integer NOT NULL,
    n_followings integer NOT NULL,
    n_medias integer NOT NULL
);

ALTER TABLE public.profile OWNER TO lidia;

--
-- Name: profile profile_pkey; Type: CONSTRAINT; Schema: public;
--
ALTER TABLE ONLY public.profile
    ADD CONSTRAINT profile_pkey PRIMARY KEY (username, date);