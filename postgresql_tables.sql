--
-- PostgreSQL database: socialnetworksdb.
--
-- Test table 1.
--
CREATE TABLE public.test1(
    id VARCHAR(50) PRIMARY KEY,
    userid integer NOT NULL,
    username VARCHAR(50) NOT NULL, 
    date VARCHAR(20) NOT NULL, 
    social_media varchar(30) NOT NULL
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.test1 OWNER TO lidia;

--
-- Test table 2.
-- It has a foreign key (FK) to the 'id' field of the 'test1' table. So in order
-- to perform deletes, 'ON DELETE CASCADE' is added to remove the referenced records
-- of the 'test1' table when are referenced by the records of the 'test2' table which
-- are going to be removed.
--
CREATE TABLE public.test2(
    id VARCHAR(50) PRIMARY KEY,
    id_test1 VARCHAR(50) NOT NULL,
    like_count integer NOT NULL,
    text_count integer NOT NULL,
    FOREIGN KEY (id_test1) REFERENCES test1(id) ON DELETE CASCADE
);

-- 
-- Assign an owner to the table in order to operate with it.
--
ALTER TABLE public.test2 OWNER TO lidia;