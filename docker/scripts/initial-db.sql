--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.5
-- Dumped by pg_dump version 9.3.5
-- Started on 2014-09-11 10:23:21 BST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

DROP DATABASE rehabradio;
--
-- TOC entry 2242 (class 1262 OID 16385)
-- Name: rehabradio; Type: DATABASE; Schema: -; Owner: rehabradio
--

CREATE DATABASE rehabradio WITH TEMPLATE = template0 ENCODING = 'SQL_ASCII' LC_COLLATE = 'C' LC_CTYPE = 'C';


ALTER DATABASE rehabradio OWNER TO rehabradio;

\connect rehabradio

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 2243 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 211 (class 3079 OID 11753)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2245 (class 0 OID 0)
-- Dependencies: 211
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 177 (class 1259 OID 24606)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO rehabradio;

--
-- TOC entry 176 (class 1259 OID 24604)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO rehabradio;

--
-- TOC entry 2246 (class 0 OID 0)
-- Dependencies: 176
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- TOC entry 179 (class 1259 OID 24616)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO rehabradio;

--
-- TOC entry 178 (class 1259 OID 24614)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO rehabradio;

--
-- TOC entry 2247 (class 0 OID 0)
-- Dependencies: 178
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- TOC entry 175 (class 1259 OID 24596)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO rehabradio;

--
-- TOC entry 174 (class 1259 OID 24594)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO rehabradio;

--
-- TOC entry 2248 (class 0 OID 0)
-- Dependencies: 174
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- TOC entry 181 (class 1259 OID 24626)
-- Name: auth_user; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO rehabradio;

--
-- TOC entry 183 (class 1259 OID 24636)
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO rehabradio;

--
-- TOC entry 182 (class 1259 OID 24634)
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO rehabradio;

--
-- TOC entry 2249 (class 0 OID 0)
-- Dependencies: 182
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 180 (class 1259 OID 24624)
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO rehabradio;

--
-- TOC entry 2250 (class 0 OID 0)
-- Dependencies: 180
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 185 (class 1259 OID 24646)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO rehabradio;

--
-- TOC entry 184 (class 1259 OID 24644)
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO rehabradio;

--
-- TOC entry 2251 (class 0 OID 0)
-- Dependencies: 184
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- TOC entry 187 (class 1259 OID 24698)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO rehabradio;

--
-- TOC entry 186 (class 1259 OID 24696)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO rehabradio;

--
-- TOC entry 2252 (class 0 OID 0)
-- Dependencies: 186
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- TOC entry 173 (class 1259 OID 24586)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO rehabradio;

--
-- TOC entry 172 (class 1259 OID 24584)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO rehabradio;

--
-- TOC entry 2253 (class 0 OID 0)
-- Dependencies: 172
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- TOC entry 171 (class 1259 OID 24578)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO rehabradio;

--
-- TOC entry 170 (class 1259 OID 24576)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO rehabradio;

--
-- TOC entry 2254 (class 0 OID 0)
-- Dependencies: 170
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- TOC entry 210 (class 1259 OID 25101)
-- Name: django_session; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO rehabradio;

--
-- TOC entry 189 (class 1259 OID 24722)
-- Name: radio_metadata_album; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_metadata_album (
    id integer NOT NULL,
    source_type character varying(10) NOT NULL,
    source_id character varying(100) NOT NULL,
    name character varying(500) NOT NULL
);


ALTER TABLE public.radio_metadata_album OWNER TO rehabradio;

--
-- TOC entry 188 (class 1259 OID 24720)
-- Name: radio_metadata_album_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_metadata_album_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_metadata_album_id_seq OWNER TO rehabradio;

--
-- TOC entry 2255 (class 0 OID 0)
-- Dependencies: 188
-- Name: radio_metadata_album_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_metadata_album_id_seq OWNED BY radio_metadata_album.id;


--
-- TOC entry 191 (class 1259 OID 24732)
-- Name: radio_metadata_artist; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_metadata_artist (
    id integer NOT NULL,
    source_type character varying(10) NOT NULL,
    source_id character varying(100) NOT NULL,
    name character varying(500) NOT NULL
);


ALTER TABLE public.radio_metadata_artist OWNER TO rehabradio;

--
-- TOC entry 190 (class 1259 OID 24730)
-- Name: radio_metadata_artist_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_metadata_artist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_metadata_artist_id_seq OWNER TO rehabradio;

--
-- TOC entry 2256 (class 0 OID 0)
-- Dependencies: 190
-- Name: radio_metadata_artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_metadata_artist_id_seq OWNED BY radio_metadata_artist.id;


--
-- TOC entry 193 (class 1259 OID 24742)
-- Name: radio_metadata_track; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_metadata_track (
    id integer NOT NULL,
    source_type character varying(10) NOT NULL,
    source_id character varying(100) NOT NULL,
    name character varying(500) NOT NULL,
    duration_ms integer NOT NULL,
    preview_url character varying(200) NOT NULL,
    track_number integer NOT NULL,
    play_count integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    album_id integer,
    owner_id integer NOT NULL,
    image_large character varying(200),
    image_medium character varying(200),
    image_small character varying(200),
    uri character varying(500) NOT NULL
);


ALTER TABLE public.radio_metadata_track OWNER TO rehabradio;

--
-- TOC entry 195 (class 1259 OID 24750)
-- Name: radio_metadata_track_artists; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_metadata_track_artists (
    id integer NOT NULL,
    track_id integer NOT NULL,
    artist_id integer NOT NULL
);


ALTER TABLE public.radio_metadata_track_artists OWNER TO rehabradio;

--
-- TOC entry 194 (class 1259 OID 24748)
-- Name: radio_metadata_track_artists_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_metadata_track_artists_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_metadata_track_artists_id_seq OWNER TO rehabradio;

--
-- TOC entry 2257 (class 0 OID 0)
-- Dependencies: 194
-- Name: radio_metadata_track_artists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_metadata_track_artists_id_seq OWNED BY radio_metadata_track_artists.id;


--
-- TOC entry 192 (class 1259 OID 24740)
-- Name: radio_metadata_track_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_metadata_track_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_metadata_track_id_seq OWNER TO rehabradio;

--
-- TOC entry 2258 (class 0 OID 0)
-- Dependencies: 192
-- Name: radio_metadata_track_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_metadata_track_id_seq OWNED BY radio_metadata_track.id;


--
-- TOC entry 203 (class 1259 OID 24973)
-- Name: radio_players_player; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_players_player (
    id integer NOT NULL,
    name character varying(500) NOT NULL,
    location character varying(500) NOT NULL,
    token character varying(500) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    active boolean NOT NULL,
    queue_id integer,
    owner_id integer
);


ALTER TABLE public.radio_players_player OWNER TO rehabradio;

--
-- TOC entry 202 (class 1259 OID 24971)
-- Name: radio_players_player_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_players_player_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_players_player_id_seq OWNER TO rehabradio;

--
-- TOC entry 2259 (class 0 OID 0)
-- Dependencies: 202
-- Name: radio_players_player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_players_player_id_seq OWNED BY radio_players_player.id;


--
-- TOC entry 205 (class 1259 OID 25000)
-- Name: radio_playlists_playlist; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_playlists_playlist (
    id integer NOT NULL,
    name character varying(500) NOT NULL,
    description character varying(500) NOT NULL,
    owner_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    protection character varying(10) NOT NULL
);


ALTER TABLE public.radio_playlists_playlist OWNER TO rehabradio;

--
-- TOC entry 204 (class 1259 OID 24998)
-- Name: radio_playlists_playlist_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_playlists_playlist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_playlists_playlist_id_seq OWNER TO rehabradio;

--
-- TOC entry 2260 (class 0 OID 0)
-- Dependencies: 204
-- Name: radio_playlists_playlist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_playlists_playlist_id_seq OWNED BY radio_playlists_playlist.id;


--
-- TOC entry 207 (class 1259 OID 25010)
-- Name: radio_playlists_playlisttrack; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_playlists_playlisttrack (
    id integer NOT NULL,
    "position" integer NOT NULL,
    owner_id integer NOT NULL,
    playlist_id integer NOT NULL,
    track_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    CONSTRAINT radio_playlists_playlisttrack_position_check CHECK (("position" >= 0))
);


ALTER TABLE public.radio_playlists_playlisttrack OWNER TO rehabradio;

--
-- TOC entry 206 (class 1259 OID 25008)
-- Name: radio_playlists_playlisttrack_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_playlists_playlisttrack_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_playlists_playlisttrack_id_seq OWNER TO rehabradio;

--
-- TOC entry 2261 (class 0 OID 0)
-- Dependencies: 206
-- Name: radio_playlists_playlisttrack_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_playlists_playlisttrack_id_seq OWNED BY radio_playlists_playlisttrack.id;


--
-- TOC entry 197 (class 1259 OID 24873)
-- Name: radio_queue_queue; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_queue_queue (
    id integer NOT NULL,
    name character varying(500) NOT NULL,
    description character varying(500) NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    owner_id integer NOT NULL
);


ALTER TABLE public.radio_queue_queue OWNER TO rehabradio;

--
-- TOC entry 196 (class 1259 OID 24871)
-- Name: radio_queue_queue_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_queue_queue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_queue_queue_id_seq OWNER TO rehabradio;

--
-- TOC entry 2262 (class 0 OID 0)
-- Dependencies: 196
-- Name: radio_queue_queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_queue_queue_id_seq OWNED BY radio_queue_queue.id;


--
-- TOC entry 199 (class 1259 OID 24887)
-- Name: radio_queue_queuetrack; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_queue_queuetrack (
    id integer NOT NULL,
    "position" integer NOT NULL,
    owner_id integer NOT NULL,
    track_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    queue_id integer NOT NULL,
    updated timestamp with time zone NOT NULL,
    state character varying(500),
    time_position integer,
    CONSTRAINT radio_queue_queuetrack_position_check CHECK (("position" >= 0))
);


ALTER TABLE public.radio_queue_queuetrack OWNER TO rehabradio;

--
-- TOC entry 198 (class 1259 OID 24885)
-- Name: radio_queue_queuetrack_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_queue_queuetrack_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_queue_queuetrack_id_seq OWNER TO rehabradio;

--
-- TOC entry 2263 (class 0 OID 0)
-- Dependencies: 198
-- Name: radio_queue_queuetrack_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_queue_queuetrack_id_seq OWNED BY radio_queue_queuetrack.id;


--
-- TOC entry 201 (class 1259 OID 24896)
-- Name: radio_queue_queuetrackhistory; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_queue_queuetrackhistory (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    owner_id integer NOT NULL,
    track_id integer NOT NULL,
    queue_id integer NOT NULL
);


ALTER TABLE public.radio_queue_queuetrackhistory OWNER TO rehabradio;

--
-- TOC entry 200 (class 1259 OID 24894)
-- Name: radio_queue_queuetrackhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_queue_queuetrackhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_queue_queuetrackhistory_id_seq OWNER TO rehabradio;

--
-- TOC entry 2264 (class 0 OID 0)
-- Dependencies: 200
-- Name: radio_queue_queuetrackhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_queue_queuetrackhistory_id_seq OWNED BY radio_queue_queuetrackhistory.id;


--
-- TOC entry 209 (class 1259 OID 25088)
-- Name: radio_users_profile; Type: TABLE; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE TABLE radio_users_profile (
    id integer NOT NULL,
    avatar character varying(200),
    user_id integer NOT NULL
);


ALTER TABLE public.radio_users_profile OWNER TO rehabradio;

--
-- TOC entry 208 (class 1259 OID 25086)
-- Name: radio_users_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: rehabradio
--

CREATE SEQUENCE radio_users_profile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.radio_users_profile_id_seq OWNER TO rehabradio;

--
-- TOC entry 2265 (class 0 OID 0)
-- Dependencies: 208
-- Name: radio_users_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rehabradio
--

ALTER SEQUENCE radio_users_profile_id_seq OWNED BY radio_users_profile.id;


--
-- TOC entry 1948 (class 2604 OID 24609)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- TOC entry 1949 (class 2604 OID 24619)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 1947 (class 2604 OID 24599)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- TOC entry 1950 (class 2604 OID 24629)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 1951 (class 2604 OID 24639)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 1952 (class 2604 OID 24649)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- TOC entry 1953 (class 2604 OID 24701)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- TOC entry 1946 (class 2604 OID 24589)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- TOC entry 1945 (class 2604 OID 24581)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- TOC entry 1955 (class 2604 OID 24725)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_metadata_album ALTER COLUMN id SET DEFAULT nextval('radio_metadata_album_id_seq'::regclass);


--
-- TOC entry 1956 (class 2604 OID 24735)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_metadata_artist ALTER COLUMN id SET DEFAULT nextval('radio_metadata_artist_id_seq'::regclass);


--
-- TOC entry 1957 (class 2604 OID 24745)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_metadata_track ALTER COLUMN id SET DEFAULT nextval('radio_metadata_track_id_seq'::regclass);


--
-- TOC entry 1958 (class 2604 OID 24753)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_metadata_track_artists ALTER COLUMN id SET DEFAULT nextval('radio_metadata_track_artists_id_seq'::regclass);


--
-- TOC entry 1963 (class 2604 OID 24976)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_players_player ALTER COLUMN id SET DEFAULT nextval('radio_players_player_id_seq'::regclass);


--
-- TOC entry 1964 (class 2604 OID 25003)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_playlists_playlist ALTER COLUMN id SET DEFAULT nextval('radio_playlists_playlist_id_seq'::regclass);


--
-- TOC entry 1965 (class 2604 OID 25013)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_playlists_playlisttrack ALTER COLUMN id SET DEFAULT nextval('radio_playlists_playlisttrack_id_seq'::regclass);


--
-- TOC entry 1959 (class 2604 OID 24876)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queue ALTER COLUMN id SET DEFAULT nextval('radio_queue_queue_id_seq'::regclass);


--
-- TOC entry 1960 (class 2604 OID 24890)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queuetrack ALTER COLUMN id SET DEFAULT nextval('radio_queue_queuetrack_id_seq'::regclass);


--
-- TOC entry 1962 (class 2604 OID 24899)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queuetrackhistory ALTER COLUMN id SET DEFAULT nextval('radio_queue_queuetrackhistory_id_seq'::regclass);


--
-- TOC entry 1967 (class 2604 OID 25091)
-- Name: id; Type: DEFAULT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_users_profile ALTER COLUMN id SET DEFAULT nextval('radio_users_profile_id_seq'::regclass);


--
-- TOC entry 2204 (class 0 OID 24606)
-- Dependencies: 177
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 2266 (class 0 OID 0)
-- Dependencies: 176
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- TOC entry 2206 (class 0 OID 24616)
-- Dependencies: 179
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2267 (class 0 OID 0)
-- Dependencies: 178
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 2202 (class 0 OID 24596)
-- Dependencies: 175
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add album	7	add_album
20	Can change album	7	change_album
21	Can delete album	7	delete_album
22	Can add artist	8	add_artist
23	Can change artist	8	change_artist
24	Can delete artist	8	delete_artist
25	Can add track	9	add_track
26	Can change track	9	change_track
27	Can delete track	9	delete_track
28	Can add player	10	add_player
29	Can change player	10	change_player
30	Can delete player	10	delete_player
31	Can add playlist	11	add_playlist
32	Can change playlist	11	change_playlist
33	Can delete playlist	11	delete_playlist
34	Can add playlist track	12	add_playlisttrack
35	Can change playlist track	12	change_playlisttrack
36	Can delete playlist track	12	delete_playlisttrack
37	Can add queue	13	add_queue
38	Can change queue	13	change_queue
39	Can delete queue	13	delete_queue
40	Can add queue track	14	add_queuetrack
41	Can change queue track	14	change_queuetrack
42	Can delete queue track	14	delete_queuetrack
43	Can add queue track history	15	add_queuetrackhistory
44	Can change queue track history	15	change_queuetrackhistory
45	Can delete queue track history	15	delete_queuetrackhistory
46	Can add profile	16	add_profile
47	Can change profile	16	change_profile
48	Can delete profile	16	delete_profile
\.


--
-- TOC entry 2268 (class 0 OID 0)
-- Dependencies: 174
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('auth_permission_id_seq', 48, true);


--
-- TOC entry 2208 (class 0 OID 24626)
-- Dependencies: 181
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$12000$ZpbgYedd62Pj$sMPYMRQnOr/kcEqmzPK3mdl41OBpo2wRNtigTZrC3+A=	2014-09-11 09:10:58.333357+00	t	admin				t	t	2014-09-11 09:10:27.036345+00
2	pbkdf2_sha256$12000$xA3KCVhjG3oG$LElxCiX6DAu1Vphz9c0HswW6O8MlaY/iQosY16Mqi8E=	2014-09-11 09:13:25.246261+00	f	testuser				f	t	2014-09-11 09:13:25.246315+00
3	4c7461d3-6faa-4db7-ad40-0c61cc42fac9	2014-09-11 09:14:51.523225+00	f	Test Player				t	t	2014-09-11 09:14:51.523317+00
4	88b9c510-493c-42f1-b5d3-9c922d6d3554	2014-09-11 09:15:11.928315+00	f	Test Player 2				t	t	2014-09-11 09:15:11.928383+00
\.


--
-- TOC entry 2210 (class 0 OID 24636)
-- Dependencies: 183
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 2269 (class 0 OID 0)
-- Dependencies: 182
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- TOC entry 2270 (class 0 OID 0)
-- Dependencies: 180
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('auth_user_id_seq', 4, true);


--
-- TOC entry 2212 (class 0 OID 24646)
-- Dependencies: 185
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2271 (class 0 OID 0)
-- Dependencies: 184
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- TOC entry 2214 (class 0 OID 24698)
-- Dependencies: 187
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2014-09-11 09:13:25.343424+00	2	testuser	1		4	1
2	2014-09-11 09:14:51.584045+00	1	Belfast - Test Player	1		10	1
3	2014-09-11 09:15:11.960556+00	2	London - Test Player 2	1		10	1
\.


--
-- TOC entry 2272 (class 0 OID 0)
-- Dependencies: 186
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 3, true);


--
-- TOC entry 2200 (class 0 OID 24586)
-- Dependencies: 173
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	log entry	admin	logentry
2	permission	auth	permission
3	group	auth	group
4	user	auth	user
5	content type	contenttypes	contenttype
6	session	sessions	session
7	album	radio_metadata	album
8	artist	radio_metadata	artist
9	track	radio_metadata	track
10	player	radio_players	player
11	playlist	radio_playlists	playlist
12	playlist track	radio_playlists	playlisttrack
13	queue	radio_queue	queue
14	queue track	radio_queue	queuetrack
15	queue track history	radio_queue	queuetrackhistory
16	profile	radio_users	profile
\.


--
-- TOC entry 2273 (class 0 OID 0)
-- Dependencies: 172
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('django_content_type_id_seq', 16, true);


--
-- TOC entry 2198 (class 0 OID 24578)
-- Dependencies: 171
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2014-09-11 09:05:36.292952+00
2	auth	0001_initial	2014-09-11 09:05:37.077714+00
3	admin	0001_initial	2014-09-11 09:05:37.280259+00
4	radio_metadata	0001_initial	2014-09-11 09:05:37.987163+00
5	radio_metadata	0002_auto_20140801_1527	2014-09-11 09:05:38.137851+00
6	radio_metadata	0003_remove_track_vote_count	2014-09-11 09:05:38.213046+00
7	radio_metadata	0004_auto_20140808_1103	2014-09-11 09:05:38.379333+00
8	radio_metadata	0005_auto_20140808_1304	2014-09-11 09:05:38.479667+00
9	radio_metadata	0006_track_uri	2014-09-11 09:05:38.772634+00
10	radio_metadata	0007_auto_20140909_1141	2014-09-11 09:05:38.92158+00
11	radio_queue	0001_initial	2014-09-11 09:05:39.430197+00
12	radio_queue	0002_queuedtrack_alive	2014-09-11 09:05:39.681428+00
13	radio_queue	0003_auto_20140804_1342	2014-09-11 09:05:39.839298+00
14	radio_queue	0004_auto_20140808_1303	2014-09-11 09:05:40.19174+00
15	radio_queue	0005_auto_20140808_1332	2014-09-11 09:05:40.897785+00
16	radio_queue	0006_queuetrackhistory_queue	2014-09-11 09:05:41.242205+00
17	radio_queue	0007_auto_20140811_0814	2014-09-11 09:05:41.956207+00
18	radio_queue	0008_auto_20140811_0915	2014-09-11 09:05:42.315253+00
19	radio_players	0001_initial	2014-09-11 09:05:42.383108+00
20	radio_players	0002_auto_20140813_0846	2014-09-11 09:05:42.74186+00
21	radio_players	0003_auto_20140813_1009	2014-09-11 09:05:43.025405+00
22	radio_players	0004_auto_20140826_0856	2014-09-11 09:05:43.282782+00
23	radio_players	0005_player_owner	2014-09-11 09:05:43.593019+00
24	radio_players	0006_auto_20140827_1651	2014-09-11 09:05:43.891617+00
25	radio_playlists	0001_initial	2014-09-11 09:05:44.298997+00
26	radio_playlists	0002_remove_playlist_protected	2014-09-11 09:05:44.383816+00
27	radio_playlists	0003_auto_20140808_1114	2014-09-11 09:05:45.207979+00
28	radio_playlists	0004_auto_20140811_0915	2014-09-11 09:05:45.342856+00
29	radio_playlists	0005_auto_20140826_0856	2014-09-11 09:05:45.498544+00
30	radio_playlists	0006_playlist_public	2014-09-11 09:05:45.785982+00
31	radio_queue	0009_auto_20140826_0856	2014-09-11 09:05:45.946606+00
32	radio_queue	0010_auto_20140826_1415	2014-09-11 09:05:46.192618+00
33	radio_users	0001_initial	2014-09-11 09:05:46.252941+00
34	radio_users	0002_auto_20140814_1426	2014-09-11 09:05:46.402284+00
35	radio_users	0003_auto_20140814_1520	2014-09-11 09:05:46.559511+00
36	sessions	0001_initial	2014-09-11 09:05:46.68471+00
\.


--
-- TOC entry 2274 (class 0 OID 0)
-- Dependencies: 170
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('django_migrations_id_seq', 36, true);


--
-- TOC entry 2237 (class 0 OID 25101)
-- Dependencies: 210
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- TOC entry 2216 (class 0 OID 24722)
-- Dependencies: 189
-- Data for Name: radio_metadata_album; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_metadata_album (id, source_type, source_id, name) FROM stdin;
1	spotify	7CzrzGbCwqT8Y43tvIUPBX	Days Are Gone (Deluxe Edition)
2	spotify	2gMWwDIxxGIiblnv1pQHyd	Here And Now
3	spotify	4dt9zkhCdk7AwpYDSlyVyW	The Lego® Movie: Original Motion Picture Soundtrack
\.


--
-- TOC entry 2275 (class 0 OID 0)
-- Dependencies: 188
-- Name: radio_metadata_album_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_metadata_album_id_seq', 3, true);


--
-- TOC entry 2218 (class 0 OID 24732)
-- Dependencies: 191
-- Data for Name: radio_metadata_artist; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_metadata_artist (id, source_type, source_id, name) FROM stdin;
1	soundcloud	50707660	MightyGuitarSmith
2	soundcloud	61123	NARSTI
3	soundcloud	2097360	Foo Fighters
4	spotify	4Ui2kfOqGujY81UcPrb5KE	Haim
5	spotify	6deZN1bslXzeGvOLaLMOIF	Nickelback
6	spotify	60TpWrVUOupMgyDaMnp0tM	Joli
\.


--
-- TOC entry 2276 (class 0 OID 0)
-- Dependencies: 190
-- Name: radio_metadata_artist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_metadata_artist_id_seq', 6, true);


--
-- TOC entry 2220 (class 0 OID 24742)
-- Dependencies: 193
-- Data for Name: radio_metadata_track; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_metadata_track (id, source_type, source_id, name, duration_ms, preview_url, track_number, play_count, created, updated, album_id, owner_id, image_large, image_medium, image_small, uri) FROM stdin;
1	soundcloud	106574135	Avenge Sevenfold Shepard Of Fire	270470	https://api.soundcloud.com/tracks/106574135/stream	0	0	2014-09-11 09:16:37.983133+00	2014-09-11 09:16:37.983182+00	\N	1	\N	\N	\N	soundcloud:song/Avenge Sevenfold Shepard Of Fire.106574135
2	soundcloud	191424	Not As Strong As The Machines	302680	https://api.soundcloud.com/tracks/191424/stream	0	0	2014-09-11 09:16:51.240401+00	2014-09-11 09:16:51.240446+00	\N	1	https://i1.sndcdn.com/artworks-000024344257-2srbjh-t500x500.jpg?e76cf77	https://i1.sndcdn.com/artworks-000024344257-2srbjh-t300x300.jpg?e76cf77	https://i1.sndcdn.com/artworks-000024344257-2srbjh-t67x67.jpg?e76cf77	soundcloud:song/Not As Strong As The Machines.191424
3	soundcloud	117723710	The Pretender	269060	https://api.soundcloud.com/tracks/117723710/stream	0	0	2014-09-11 09:17:15.458813+00	2014-09-11 09:17:15.458865+00	\N	1	https://i1.sndcdn.com/artworks-000061422649-n1ngsr-t500x500.jpg?e76cf77	https://i1.sndcdn.com/artworks-000061422649-n1ngsr-t300x300.jpg?e76cf77	https://i1.sndcdn.com/artworks-000061422649-n1ngsr-t67x67.jpg?e76cf77	soundcloud:song/The Pretender.117723710
4	spotify	7KdF7Zac5eC9jutk9Qret4	The Wire	245800	https://p.scdn.co/mp3-preview/5e1176683ae66ca683ca718d26a097484ec4c3db	3	0	2014-09-11 09:17:29.544785+00	2014-09-11 09:17:29.544858+00	1	1	https://i.scdn.co/image/b83e4011e9b0ae87b0c4913c296f94155a76c159	https://i.scdn.co/image/8fa6077324d497f3cbb83dbc16cf298552863e9e	https://i.scdn.co/image/4164e5082af9f77dcc81329b1894f71d9eba47a2	spotify:track:7KdF7Zac5eC9jutk9Qret4
5	spotify	4bCOAuhvjsxbVBM5MM8oik	When We Stand Together	190786	https://p.scdn.co/mp3-preview/e933a6298574b05bde6d90dee4b5422241777429	3	0	2014-09-11 09:18:04.194821+00	2014-09-11 09:18:04.194871+00	2	1	https://i.scdn.co/image/0be39442eb4d2af9fa6216ca901c8631f7d56a3c	https://i.scdn.co/image/4963e311c6436bcb368ee79645b7d23a4ef585d6	https://i.scdn.co/image/f779ec05fb26d8ce43ae677c40403ac784ef31c2	spotify:track:4bCOAuhvjsxbVBM5MM8oik
6	spotify	3zGaTyI4qNQ3b9IA6hjNpC	Everything is AWESOME!!!	86735	https://p.scdn.co/mp3-preview/581023243070e237d8c273224c215a2e5f9d8d7b	25	0	2014-09-11 09:18:15.807126+00	2014-09-11 09:18:15.807174+00	3	1	https://i.scdn.co/image/a78a0c21745c15f6114602b7c9008d7abb90a8bf	https://i.scdn.co/image/dda5b6587fe090b84c5789c5bcee299fed8a9aaa	https://i.scdn.co/image/1fbdcc7c4464d74bcac3b3b400e4024a056984e9	spotify:track:3zGaTyI4qNQ3b9IA6hjNpC
\.


--
-- TOC entry 2222 (class 0 OID 24750)
-- Dependencies: 195
-- Data for Name: radio_metadata_track_artists; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_metadata_track_artists (id, track_id, artist_id) FROM stdin;
\.


--
-- TOC entry 2277 (class 0 OID 0)
-- Dependencies: 194
-- Name: radio_metadata_track_artists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_metadata_track_artists_id_seq', 1, false);


--
-- TOC entry 2278 (class 0 OID 0)
-- Dependencies: 192
-- Name: radio_metadata_track_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_metadata_track_id_seq', 6, true);


--
-- TOC entry 2230 (class 0 OID 24973)
-- Dependencies: 203
-- Data for Name: radio_players_player; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_players_player (id, name, location, token, created, updated, active, queue_id, owner_id) FROM stdin;
1	Test Player	Belfast	4c7461d3-6faa-4db7-ad40-0c61cc42fac9	2014-09-11 09:14:51.572396+00	2014-09-11 09:14:51.572456+00	t	1	3
2	Test Player 2	London	88b9c510-493c-42f1-b5d3-9c922d6d3554	2014-09-11 09:15:11.948212+00	2014-09-11 09:15:11.948272+00	f	1	4
\.


--
-- TOC entry 2279 (class 0 OID 0)
-- Dependencies: 202
-- Name: radio_players_player_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_players_player_id_seq', 2, true);


--
-- TOC entry 2232 (class 0 OID 25000)
-- Dependencies: 205
-- Data for Name: radio_playlists_playlist; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_playlists_playlist (id, name, description, owner_id, created, updated, protection) FROM stdin;
1	Test Playlist (Public)	Public playlist	1	2014-09-11 09:15:35.761592+00	2014-09-11 09:15:35.761639+00	public
2	Test Playlist (Private)	Private playlist	1	2014-09-11 09:15:48.763125+00	2014-09-11 09:15:48.763174+00	private
\.


--
-- TOC entry 2280 (class 0 OID 0)
-- Dependencies: 204
-- Name: radio_playlists_playlist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_playlists_playlist_id_seq', 2, true);


--
-- TOC entry 2234 (class 0 OID 25010)
-- Dependencies: 207
-- Data for Name: radio_playlists_playlisttrack; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_playlists_playlisttrack (id, "position", owner_id, playlist_id, track_id, created, updated) FROM stdin;
1	1	1	1	1	2014-09-11 09:18:33.028029+00	2014-09-11 09:18:33.028076+00
2	2	1	1	2	2014-09-11 09:18:36.461229+00	2014-09-11 09:18:36.461281+00
3	3	1	1	3	2014-09-11 09:18:39.529364+00	2014-09-11 09:18:39.529417+00
4	4	1	1	4	2014-09-11 09:18:43.245517+00	2014-09-11 09:18:43.245567+00
5	5	1	1	5	2014-09-11 09:18:47.118916+00	2014-09-11 09:18:47.118964+00
6	6	1	1	6	2014-09-11 09:18:50.667064+00	2014-09-11 09:18:50.667117+00
7	1	1	2	3	2014-09-11 09:18:58.784567+00	2014-09-11 09:18:58.784614+00
8	2	1	2	5	2014-09-11 09:19:03.222629+00	2014-09-11 09:19:03.222723+00
9	3	1	2	6	2014-09-11 09:19:08.763363+00	2014-09-11 09:19:08.763412+00
\.


--
-- TOC entry 2281 (class 0 OID 0)
-- Dependencies: 206
-- Name: radio_playlists_playlisttrack_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_playlists_playlisttrack_id_seq', 9, true);


--
-- TOC entry 2224 (class 0 OID 24873)
-- Dependencies: 197
-- Data for Name: radio_queue_queue; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_queue_queue (id, name, description, created, updated, owner_id) FROM stdin;
1	Test Queue	Example queue	2014-09-11 09:14:28.770008+00	2014-09-11 09:14:28.770061+00	1
2	Test Queue (empty)	An empty queue	2014-09-11 09:20:07.616951+00	2014-09-11 09:20:07.617001+00	1
\.


--
-- TOC entry 2282 (class 0 OID 0)
-- Dependencies: 196
-- Name: radio_queue_queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_queue_queue_id_seq', 2, true);


--
-- TOC entry 2226 (class 0 OID 24887)
-- Dependencies: 199
-- Data for Name: radio_queue_queuetrack; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_queue_queuetrack (id, "position", owner_id, track_id, created, queue_id, updated, state, time_position) FROM stdin;
1	1	1	3	2014-09-11 09:19:32.51588+00	1	2014-09-11 09:19:32.51593+00	\N	\N
2	2	1	5	2014-09-11 09:19:32.627549+00	1	2014-09-11 09:19:32.627615+00	\N	\N
3	3	1	6	2014-09-11 09:19:32.708775+00	1	2014-09-11 09:19:32.708825+00	\N	\N
\.


--
-- TOC entry 2283 (class 0 OID 0)
-- Dependencies: 198
-- Name: radio_queue_queuetrack_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_queue_queuetrack_id_seq', 3, true);


--
-- TOC entry 2228 (class 0 OID 24896)
-- Dependencies: 201
-- Data for Name: radio_queue_queuetrackhistory; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_queue_queuetrackhistory (id, created, owner_id, track_id, queue_id) FROM stdin;
1	2014-09-11 09:19:32.536304+00	1	3	1
2	2014-09-11 09:19:32.644687+00	1	5	1
3	2014-09-11 09:19:32.71974+00	1	6	1
\.


--
-- TOC entry 2284 (class 0 OID 0)
-- Dependencies: 200
-- Name: radio_queue_queuetrackhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_queue_queuetrackhistory_id_seq', 3, true);


--
-- TOC entry 2236 (class 0 OID 25088)
-- Dependencies: 209
-- Data for Name: radio_users_profile; Type: TABLE DATA; Schema: public; Owner: rehabradio
--

COPY radio_users_profile (id, avatar, user_id) FROM stdin;
1	\N	1
2	\N	2
3	\N	3
4	\N	4
\.


--
-- TOC entry 2285 (class 0 OID 0)
-- Dependencies: 208
-- Name: radio_users_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rehabradio
--

SELECT pg_catalog.setval('radio_users_profile_id_seq', 4, true);


--
-- TOC entry 1980 (class 2606 OID 24613)
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 1986 (class 2606 OID 24623)
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- TOC entry 1988 (class 2606 OID 24621)
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 1982 (class 2606 OID 24611)
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 1976 (class 2606 OID 24603)
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- TOC entry 1978 (class 2606 OID 24601)
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 1996 (class 2606 OID 24641)
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 1998 (class 2606 OID 24643)
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- TOC entry 1990 (class 2606 OID 24631)
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2002 (class 2606 OID 24651)
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2004 (class 2606 OID 24653)
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- TOC entry 1992 (class 2606 OID 24633)
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 2008 (class 2606 OID 24707)
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 1971 (class 2606 OID 24593)
-- Name: django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- TOC entry 1973 (class 2606 OID 24591)
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 1969 (class 2606 OID 24583)
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 2062 (class 2606 OID 25108)
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 2010 (class 2606 OID 24727)
-- Name: radio_metadata_album_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_metadata_album
    ADD CONSTRAINT radio_metadata_album_pkey PRIMARY KEY (id);


--
-- TOC entry 2012 (class 2606 OID 24729)
-- Name: radio_metadata_album_source_type_2b78c835a32ff94e_uniq; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_metadata_album
    ADD CONSTRAINT radio_metadata_album_source_type_2b78c835a32ff94e_uniq UNIQUE (source_type, source_id);


--
-- TOC entry 2014 (class 2606 OID 24737)
-- Name: radio_metadata_artist_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_metadata_artist
    ADD CONSTRAINT radio_metadata_artist_pkey PRIMARY KEY (id);


--
-- TOC entry 2016 (class 2606 OID 24739)
-- Name: radio_metadata_artist_source_type_2d2e5c661b70c74d_uniq; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_metadata_artist
    ADD CONSTRAINT radio_metadata_artist_source_type_2d2e5c661b70c74d_uniq UNIQUE (source_type, source_id);


--
-- TOC entry 2026 (class 2606 OID 24755)
-- Name: radio_metadata_track_artists_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_metadata_track_artists
    ADD CONSTRAINT radio_metadata_track_artists_pkey PRIMARY KEY (id);


--
-- TOC entry 2028 (class 2606 OID 24757)
-- Name: radio_metadata_track_artists_track_id_artist_id_key; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_metadata_track_artists
    ADD CONSTRAINT radio_metadata_track_artists_track_id_artist_id_key UNIQUE (track_id, artist_id);


--
-- TOC entry 2020 (class 2606 OID 24747)
-- Name: radio_metadata_track_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_metadata_track
    ADD CONSTRAINT radio_metadata_track_pkey PRIMARY KEY (id);


--
-- TOC entry 2022 (class 2606 OID 24759)
-- Name: radio_metadata_track_source_type_73d9b759f2b914a2_uniq; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_metadata_track
    ADD CONSTRAINT radio_metadata_track_source_type_73d9b759f2b914a2_uniq UNIQUE (source_type, source_id);


--
-- TOC entry 2045 (class 2606 OID 24978)
-- Name: radio_players_player_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_players_player
    ADD CONSTRAINT radio_players_player_pkey PRIMARY KEY (id);


--
-- TOC entry 2048 (class 2606 OID 25007)
-- Name: radio_playlists_playlist_name_3996c384d7358e6a_uniq; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_playlists_playlist
    ADD CONSTRAINT radio_playlists_playlist_name_3996c384d7358e6a_uniq UNIQUE (name, owner_id);


--
-- TOC entry 2050 (class 2606 OID 25005)
-- Name: radio_playlists_playlist_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_playlists_playlist
    ADD CONSTRAINT radio_playlists_playlist_pkey PRIMARY KEY (id);


--
-- TOC entry 2055 (class 2606 OID 25016)
-- Name: radio_playlists_playlisttrack_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_playlists_playlisttrack
    ADD CONSTRAINT radio_playlists_playlisttrack_pkey PRIMARY KEY (id);


--
-- TOC entry 2031 (class 2606 OID 24878)
-- Name: radio_queue_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_queue_queue
    ADD CONSTRAINT radio_queue_queue_pkey PRIMARY KEY (id);


--
-- TOC entry 2036 (class 2606 OID 24893)
-- Name: radio_queue_queuetrack_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_queue_queuetrack
    ADD CONSTRAINT radio_queue_queuetrack_pkey PRIMARY KEY (id);


--
-- TOC entry 2041 (class 2606 OID 24901)
-- Name: radio_queue_queuetrackhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_queue_queuetrackhistory
    ADD CONSTRAINT radio_queue_queuetrackhistory_pkey PRIMARY KEY (id);


--
-- TOC entry 2057 (class 2606 OID 25093)
-- Name: radio_users_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_users_profile
    ADD CONSTRAINT radio_users_profile_pkey PRIMARY KEY (id);


--
-- TOC entry 2059 (class 2606 OID 25095)
-- Name: radio_users_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: rehabradio; Tablespace: 
--

ALTER TABLE ONLY radio_users_profile
    ADD CONSTRAINT radio_users_profile_user_id_key UNIQUE (user_id);


--
-- TOC entry 1983 (class 1259 OID 24660)
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 1984 (class 1259 OID 24666)
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 1974 (class 1259 OID 24654)
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- TOC entry 1993 (class 1259 OID 24678)
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- TOC entry 1994 (class 1259 OID 24672)
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- TOC entry 1999 (class 1259 OID 24690)
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 2000 (class 1259 OID 24684)
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 2005 (class 1259 OID 24708)
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 2006 (class 1259 OID 24714)
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- TOC entry 2060 (class 1259 OID 25109)
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- TOC entry 2017 (class 1259 OID 24766)
-- Name: radio_metadata_track_5e7b1936; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_metadata_track_5e7b1936 ON radio_metadata_track USING btree (owner_id);


--
-- TOC entry 2018 (class 1259 OID 24760)
-- Name: radio_metadata_track_95c3b9df; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_metadata_track_95c3b9df ON radio_metadata_track USING btree (album_id);


--
-- TOC entry 2023 (class 1259 OID 24772)
-- Name: radio_metadata_track_artists_2edb7cf7; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_metadata_track_artists_2edb7cf7 ON radio_metadata_track_artists USING btree (track_id);


--
-- TOC entry 2024 (class 1259 OID 24778)
-- Name: radio_metadata_track_artists_ca949605; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_metadata_track_artists_ca949605 ON radio_metadata_track_artists USING btree (artist_id);


--
-- TOC entry 2042 (class 1259 OID 24992)
-- Name: radio_players_player_5e7b1936; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_players_player_5e7b1936 ON radio_players_player USING btree (owner_id);


--
-- TOC entry 2043 (class 1259 OID 24984)
-- Name: radio_players_player_75249aa1; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_players_player_75249aa1 ON radio_players_player USING btree (queue_id);


--
-- TOC entry 2046 (class 1259 OID 25017)
-- Name: radio_playlists_playlist_5e7b1936; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_playlists_playlist_5e7b1936 ON radio_playlists_playlist USING btree (owner_id);


--
-- TOC entry 2051 (class 1259 OID 25035)
-- Name: radio_playlists_playlisttrack_2edb7cf7; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_playlists_playlisttrack_2edb7cf7 ON radio_playlists_playlisttrack USING btree (track_id);


--
-- TOC entry 2052 (class 1259 OID 25029)
-- Name: radio_playlists_playlisttrack_5d3a6442; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_playlists_playlisttrack_5d3a6442 ON radio_playlists_playlisttrack USING btree (playlist_id);


--
-- TOC entry 2053 (class 1259 OID 25023)
-- Name: radio_playlists_playlisttrack_5e7b1936; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_playlists_playlisttrack_5e7b1936 ON radio_playlists_playlisttrack USING btree (owner_id);


--
-- TOC entry 2029 (class 1259 OID 24879)
-- Name: radio_queue_queue_5e7b1936; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_queue_queue_5e7b1936 ON radio_queue_queue USING btree (owner_id);


--
-- TOC entry 2032 (class 1259 OID 24908)
-- Name: radio_queue_queuetrack_2edb7cf7; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_queue_queuetrack_2edb7cf7 ON radio_queue_queuetrack USING btree (track_id);


--
-- TOC entry 2033 (class 1259 OID 24902)
-- Name: radio_queue_queuetrack_5e7b1936; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_queue_queuetrack_5e7b1936 ON radio_queue_queuetrack USING btree (owner_id);


--
-- TOC entry 2034 (class 1259 OID 24960)
-- Name: radio_queue_queuetrack_75249aa1; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_queue_queuetrack_75249aa1 ON radio_queue_queuetrack USING btree (queue_id);


--
-- TOC entry 2037 (class 1259 OID 24920)
-- Name: radio_queue_queuetrackhistory_2edb7cf7; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_queue_queuetrackhistory_2edb7cf7 ON radio_queue_queuetrackhistory USING btree (track_id);


--
-- TOC entry 2038 (class 1259 OID 24914)
-- Name: radio_queue_queuetrackhistory_5e7b1936; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_queue_queuetrackhistory_5e7b1936 ON radio_queue_queuetrackhistory USING btree (owner_id);


--
-- TOC entry 2039 (class 1259 OID 24933)
-- Name: radio_queue_queuetrackhistory_75249aa1; Type: INDEX; Schema: public; Owner: rehabradio; Tablespace: 
--

CREATE INDEX radio_queue_queuetrackhistory_75249aa1 ON radio_queue_queuetrackhistory USING btree (queue_id);


--
-- TOC entry 2063 (class 2606 OID 24655)
-- Name: auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2064 (class 2606 OID 24661)
-- Name: auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2065 (class 2606 OID 24667)
-- Name: auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2069 (class 2606 OID 24691)
-- Name: auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2067 (class 2606 OID 24679)
-- Name: auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2066 (class 2606 OID 24673)
-- Name: auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2068 (class 2606 OID 24685)
-- Name: auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2070 (class 2606 OID 24709)
-- Name: djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2071 (class 2606 OID 24715)
-- Name: django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2087 (class 2606 OID 25030)
-- Name: rad_playlist_id_293960e4a7610afa_fk_radio_playlists_playlist_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_playlists_playlisttrack
    ADD CONSTRAINT rad_playlist_id_293960e4a7610afa_fk_radio_playlists_playlist_id FOREIGN KEY (playlist_id) REFERENCES radio_playlists_playlist(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2075 (class 2606 OID 24797)
-- Name: radio_me_artist_id_1c7fa56da04145b9_fk_radio_metadata_artist_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_metadata_track_artists
    ADD CONSTRAINT radio_me_artist_id_1c7fa56da04145b9_fk_radio_metadata_artist_id FOREIGN KEY (artist_id) REFERENCES radio_metadata_artist(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2072 (class 2606 OID 24761)
-- Name: radio_metad_album_id_e787f2cbfce76ed_fk_radio_metadata_album_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_metadata_track
    ADD CONSTRAINT radio_metad_album_id_e787f2cbfce76ed_fk_radio_metadata_album_id FOREIGN KEY (album_id) REFERENCES radio_metadata_album(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2074 (class 2606 OID 24773)
-- Name: radio_metad_track_id_9427a190c200ea0_fk_radio_metadata_track_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_metadata_track_artists
    ADD CONSTRAINT radio_metad_track_id_9427a190c200ea0_fk_radio_metadata_track_id FOREIGN KEY (track_id) REFERENCES radio_metadata_track(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2073 (class 2606 OID 24784)
-- Name: radio_metadata_track_owner_id_4d1c2cd98ba47dd5_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_metadata_track
    ADD CONSTRAINT radio_metadata_track_owner_id_4d1c2cd98ba47dd5_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2088 (class 2606 OID 25036)
-- Name: radio_play_track_id_375780d036d0b49c_fk_radio_metadata_track_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_playlists_playlisttrack
    ADD CONSTRAINT radio_play_track_id_375780d036d0b49c_fk_radio_metadata_track_id FOREIGN KEY (track_id) REFERENCES radio_metadata_track(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2084 (class 2606 OID 24993)
-- Name: radio_players_player_owner_id_6fb709a4adbe47b8_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_players_player
    ADD CONSTRAINT radio_players_player_owner_id_6fb709a4adbe47b8_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2083 (class 2606 OID 24985)
-- Name: radio_players_queue_id_4458c2538e252a40_fk_radio_queue_queue_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_players_player
    ADD CONSTRAINT radio_players_queue_id_4458c2538e252a40_fk_radio_queue_queue_id FOREIGN KEY (queue_id) REFERENCES radio_queue_queue(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2086 (class 2606 OID 25024)
-- Name: radio_playlists_playl_owner_id_1410b62c3d9ab434_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_playlists_playlisttrack
    ADD CONSTRAINT radio_playlists_playl_owner_id_1410b62c3d9ab434_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2085 (class 2606 OID 25018)
-- Name: radio_playlists_playl_owner_id_59675cfb9398e044_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_playlists_playlist
    ADD CONSTRAINT radio_playlists_playl_owner_id_59675cfb9398e044_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2077 (class 2606 OID 24909)
-- Name: radio_queu_track_id_212c3b13d9aec83a_fk_radio_metadata_track_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queuetrack
    ADD CONSTRAINT radio_queu_track_id_212c3b13d9aec83a_fk_radio_metadata_track_id FOREIGN KEY (track_id) REFERENCES radio_metadata_track(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2078 (class 2606 OID 24961)
-- Name: radio_queue_q_queue_id_41f3cc4846f1c9de_fk_radio_queue_queue_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queuetrack
    ADD CONSTRAINT radio_queue_q_queue_id_41f3cc4846f1c9de_fk_radio_queue_queue_id FOREIGN KEY (queue_id) REFERENCES radio_queue_queue(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2082 (class 2606 OID 24934)
-- Name: radio_queue_q_queue_id_69779aebd073c161_fk_radio_queue_queue_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queuetrackhistory
    ADD CONSTRAINT radio_queue_q_queue_id_69779aebd073c161_fk_radio_queue_queue_id FOREIGN KEY (queue_id) REFERENCES radio_queue_queue(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2076 (class 2606 OID 24880)
-- Name: radio_queue_queue_owner_id_6e80fd6eb376bf0a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queue
    ADD CONSTRAINT radio_queue_queue_owner_id_6e80fd6eb376bf0a_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2079 (class 2606 OID 24966)
-- Name: radio_queue_queuetrac_owner_id_20a9382f9301736a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queuetrack
    ADD CONSTRAINT radio_queue_queuetrac_owner_id_20a9382f9301736a_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2080 (class 2606 OID 24915)
-- Name: radio_queue_queuetrac_owner_id_4359582ba94651d9_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queuetrackhistory
    ADD CONSTRAINT radio_queue_queuetrac_owner_id_4359582ba94651d9_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2081 (class 2606 OID 24921)
-- Name: radio_queue_track_id_d0597694ddfdf09_fk_radio_metadata_track_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_queue_queuetrackhistory
    ADD CONSTRAINT radio_queue_track_id_d0597694ddfdf09_fk_radio_metadata_track_id FOREIGN KEY (track_id) REFERENCES radio_metadata_track(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2089 (class 2606 OID 25096)
-- Name: radio_users_profile_user_id_3c36936e2e6f82a6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: rehabradio
--

ALTER TABLE ONLY radio_users_profile
    ADD CONSTRAINT radio_users_profile_user_id_3c36936e2e6f82a6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2244 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2014-09-11 10:23:21 BST

--
-- PostgreSQL database dump complete
--

