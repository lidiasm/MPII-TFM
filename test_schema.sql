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
