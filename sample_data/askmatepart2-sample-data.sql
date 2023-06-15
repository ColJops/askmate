--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text
);


ALTER TABLE public.answer OWNER TO postgres;

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answer_id_seq OWNER TO postgres;

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer
);


ALTER TABLE public.comment OWNER TO postgres;

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_id_seq OWNER TO postgres;

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text
);


ALTER TABLE public.question OWNER TO postgres;

--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_id_seq OWNER TO postgres;

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.question_tag OWNER TO postgres;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


ALTER TABLE public.tag OWNER TO postgres;

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO postgres;

--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: user_answer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_answer (
    answer_id integer,
    user_id integer
);


ALTER TABLE public.user_answer OWNER TO postgres;

--
-- Name: user_comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_comment (
    comment_id integer,
    question_id integer,
    answer_id integer,
    user_id integer
);


ALTER TABLE public.user_comment OWNER TO postgres;

--
-- Name: user_question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_question (
    question_id integer,
    user_id integer
);


ALTER TABLE public.user_question OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying(255) NOT NULL,
    user_pass character varying(255) NOT NULL,
    date_reg character varying(255) NOT NULL,
    user_role character varying(255),
    user_rep character varying(255)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image) FROM stdin;
1	2017-04-28 16:49:00	4	1	You need to use brackets: my_list = []	\N
2	2017-04-25 14:42:00	35	1	Look it up in the Python docs	images/image2.jpg
4	2022-08-13 09:38:00	1	14	f f e er erg45 	\N
7	2022-08-13 18:02:00	1	22	Solution is on internet	refac3.jpg
5	2022-08-13 17:55:00	-2	22	Solution is on internet	refac3.jpg
6	2022-08-13 18:00:00	1	22	Solution is on internet, so keep going bro	\N
8	2022-08-14 15:46:00	0	23	Use google bro :)	images.jpg
9	2022-08-17 12:57:00	0	35	Try to use query in query, bro. 	
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count) FROM stdin;
1	0	\N	Please clarify the question as it is too vague!	2017-05-01 05:49:00	\N
2	\N	1	I think you could use my_list = list() as well.	2017-05-02 16:55:00	\N
4	14	\N	sort, but ok	2022-08-13 09:38:00	0
6	22	\N	google się kłania :)	2022-08-14 15:43:00	1
7	22	\N	fdtg4 f efet4 e5t tegrg	2022-08-14 15:44:00	0
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image) FROM stdin;
0	2017-04-28 08:29:00	29	7	How to make lists in Python?	I am totally new to this, any hints?	\N
1	2017-04-29 09:19:00	25	9	Wordpress loading multiple jQuery Versions	I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();\r\n\r\nI could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.\r\n\r\nBUT in my theme i also using jquery via webpack so the loading order is now following:\r\n\r\njquery\r\nbooklet\r\napp.js (bundled file with webpack, including jquery)	images/image1.png
35	2022-08-17 12:56:00	2	0	Tags still not work	Adding tags to new questins still don't work...	
14	2022-08-13 09:36:00	22	1	Test no 4 min 10 chars	Why it's ok............	\N
21	2022-08-13 15:34:00	12	1	Nowy obrazek, jak zmienić?	  fdg  g g jfx hgdd d dh 	whistling-kite-7340817_960_720.webp
22	2022-08-13 16:04:00	31	2	test obrazka jpg	Sprawdzamy czy dany obrazek działa	mrm4261.jpg
18	2022-08-13 13:46:00	7	0	testing is the best	rhgnb  hfthj kj rh tesrt	\N
24	2022-08-15 11:49:00	0	0	sometthing new	fdfeef fee ewef 	
23	2022-08-14 15:45:00	3	0	New problems need help	g rgryhgrh hg5y tht	programming.jpg
2	2017-05-01 10:41:00	1373	58	Drawing canvas with an image picked with Cordova Camera Plugin	I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS, it throws errors such as cross origin issue, or that I'm trying to use an unknown format.\r\n	\N
25	2022-08-17 01:20:00	4	0	Test using tags	How can I use tags in Ask Mate?	
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
0	1
1	3
2	3
25	2
35	2
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tag (id, name) FROM stdin;
1	python
2	sql
3	css
\.


--
-- Data for Name: user_answer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_answer (answer_id, user_id) FROM stdin;
\.


--
-- Data for Name: user_comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_comment (comment_id, question_id, answer_id, user_id) FROM stdin;
\.


--
-- Data for Name: user_question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_question (question_id, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, user_name, user_pass, date_reg, user_role, user_rep) FROM stdin;
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.answer_id_seq', 9, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comment_id_seq', 7, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_id_seq', 35, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tag_id_seq', 3, true);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- PostgreSQL database dump complete
--

