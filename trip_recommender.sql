--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-06-15 13:11:24 EDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16389)
-- Name: Attraction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Attraction" (
    attraction_id integer NOT NULL,
    destination_id integer NOT NULL,
    name text NOT NULL,
    type character varying(50),
    rating double precision,
    description text,
    url text
);


ALTER TABLE public."Attraction" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16404)
-- Name: CostOfLiving; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."CostOfLiving" (
    cost_of_living_id integer NOT NULL,
    destination_id integer NOT NULL,
    daily_avg_usd double precision,
    avg_cost_for_food double precision,
    budget_level character varying(25)
);


ALTER TABLE public."CostOfLiving" OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16575)
-- Name: Country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Country" (
    country_id integer NOT NULL,
    name text NOT NULL,
    iso_code character varying(20) NOT NULL,
    safety_index integer,
    currency character varying(50)
);


ALTER TABLE public."Country" OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16409)
-- Name: Destination; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Destination" (
    destination_id integer NOT NULL,
    country_id integer NOT NULL,
    name text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    description text,
    tags character varying(50)
);


ALTER TABLE public."Destination" OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16399)
-- Name: Lodging; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Lodging" (
    lodging_id integer NOT NULL,
    destination_id integer NOT NULL,
    name text NOT NULL,
    type character varying(50),
    avg_price_per_night double precision NOT NULL,
    rating double precision,
    url text,
    description text
);


ALTER TABLE public."Lodging" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16394)
-- Name: TransportOption; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."TransportOption" (
    transport_id integer NOT NULL,
    destination_id integer NOT NULL,
    origin_city text NOT NULL,
    transport_type character varying(50) NOT NULL,
    avg_duration_hours double precision NOT NULL,
    avg_price_usd double precision NOT NULL,
    carrier_name text,
    notes text
);


ALTER TABLE public."TransportOption" OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16582)
-- Name: VisaRequirement-; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."VisaRequirement-" (
    visa_requirement_id integer NOT NULL,
    destination_country_id integer NOT NULL,
    visa_required_origin_countries text[],
    banned_origin_countries text[]
);


ALTER TABLE public."VisaRequirement-" OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16568)
-- Name: Weather; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Weather" (
    weather_id integer NOT NULL,
    destination_id integer NOT NULL,
    avg_monthly_temp_c double precision[],
    avg_monthly_precip_mm double precision[],
    best_travel_months text[]
);


ALTER TABLE public."Weather" OWNER TO postgres;

--
-- TOC entry 3645 (class 0 OID 16389)
-- Dependencies: 217
-- Data for Name: Attraction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Attraction" (attraction_id, destination_id, name, type, rating, description, url) FROM stdin;
\.


--
-- TOC entry 3648 (class 0 OID 16404)
-- Dependencies: 220
-- Data for Name: CostOfLiving; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."CostOfLiving" (cost_of_living_id, destination_id, daily_avg_usd, avg_cost_for_food, budget_level) FROM stdin;
\.


--
-- TOC entry 3651 (class 0 OID 16575)
-- Dependencies: 223
-- Data for Name: Country; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Country" (country_id, name, iso_code, safety_index, currency) FROM stdin;
\.


--
-- TOC entry 3649 (class 0 OID 16409)
-- Dependencies: 221
-- Data for Name: Destination; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Destination" (destination_id, country_id, name, latitude, longitude, description, tags) FROM stdin;
\.


--
-- TOC entry 3647 (class 0 OID 16399)
-- Dependencies: 219
-- Data for Name: Lodging; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Lodging" (lodging_id, destination_id, name, type, avg_price_per_night, rating, url, description) FROM stdin;
\.


--
-- TOC entry 3646 (class 0 OID 16394)
-- Dependencies: 218
-- Data for Name: TransportOption; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."TransportOption" (transport_id, destination_id, origin_city, transport_type, avg_duration_hours, avg_price_usd, carrier_name, notes) FROM stdin;
\.


--
-- TOC entry 3652 (class 0 OID 16582)
-- Dependencies: 224
-- Data for Name: VisaRequirement-; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."VisaRequirement-" (visa_requirement_id, destination_country_id, visa_required_origin_countries, banned_origin_countries) FROM stdin;
\.


--
-- TOC entry 3650 (class 0 OID 16568)
-- Dependencies: 222
-- Data for Name: Weather; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Weather" (weather_id, destination_id, avg_monthly_temp_c, avg_monthly_precip_mm, best_travel_months) FROM stdin;
\.


--
-- TOC entry 3478 (class 2606 OID 16393)
-- Name: Attraction Attractions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Attraction"
    ADD CONSTRAINT "Attractions_pkey" PRIMARY KEY (attraction_id);


--
-- TOC entry 3484 (class 2606 OID 16408)
-- Name: CostOfLiving CostOfLiving_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CostOfLiving"
    ADD CONSTRAINT "CostOfLiving_pkey" PRIMARY KEY (cost_of_living_id);


--
-- TOC entry 3490 (class 2606 OID 16581)
-- Name: Country Country_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Country"
    ADD CONSTRAINT "Country_pkey" PRIMARY KEY (country_id);


--
-- TOC entry 3486 (class 2606 OID 16413)
-- Name: Destination Destination_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Destination"
    ADD CONSTRAINT "Destination_pkey" PRIMARY KEY (destination_id);


--
-- TOC entry 3482 (class 2606 OID 16403)
-- Name: Lodging Lodging_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Lodging"
    ADD CONSTRAINT "Lodging_pkey" PRIMARY KEY (lodging_id);


--
-- TOC entry 3480 (class 2606 OID 16398)
-- Name: TransportOption TransportOption_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."TransportOption"
    ADD CONSTRAINT "TransportOption_pkey" PRIMARY KEY (transport_id);


--
-- TOC entry 3492 (class 2606 OID 16588)
-- Name: VisaRequirement- VisaRequirement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."VisaRequirement-"
    ADD CONSTRAINT "VisaRequirement_pkey" PRIMARY KEY (visa_requirement_id);


--
-- TOC entry 3488 (class 2606 OID 16574)
-- Name: Weather Weather_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Weather"
    ADD CONSTRAINT "Weather_pkey" PRIMARY KEY (weather_id);


--
-- TOC entry 3497 (class 2606 OID 16599)
-- Name: Destination country_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Destination"
    ADD CONSTRAINT country_id FOREIGN KEY (country_id) REFERENCES public."Country"(country_id) NOT VALID;


--
-- TOC entry 3499 (class 2606 OID 16619)
-- Name: VisaRequirement- destination_country_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."VisaRequirement-"
    ADD CONSTRAINT destination_country_id FOREIGN KEY (destination_country_id) REFERENCES public."Country"(country_id) NOT VALID;


--
-- TOC entry 3493 (class 2606 OID 16589)
-- Name: Attraction destination_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Attraction"
    ADD CONSTRAINT destination_id FOREIGN KEY (destination_id) REFERENCES public."Destination"(destination_id) NOT VALID;


--
-- TOC entry 3496 (class 2606 OID 16594)
-- Name: CostOfLiving destination_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CostOfLiving"
    ADD CONSTRAINT destination_id FOREIGN KEY (destination_id) REFERENCES public."Destination"(destination_id) NOT VALID;


--
-- TOC entry 3495 (class 2606 OID 16604)
-- Name: Lodging destination_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Lodging"
    ADD CONSTRAINT destination_id FOREIGN KEY (destination_id) REFERENCES public."Destination"(destination_id) NOT VALID;


--
-- TOC entry 3494 (class 2606 OID 16609)
-- Name: TransportOption destination_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."TransportOption"
    ADD CONSTRAINT destination_id FOREIGN KEY (destination_id) REFERENCES public."Destination"(destination_id) NOT VALID;


--
-- TOC entry 3498 (class 2606 OID 16614)
-- Name: Weather destination_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Weather"
    ADD CONSTRAINT destination_id FOREIGN KEY (destination_id) REFERENCES public."Destination"(destination_id) NOT VALID;


-- Completed on 2025-06-15 13:11:24 EDT

--
-- PostgreSQL database dump complete
--

