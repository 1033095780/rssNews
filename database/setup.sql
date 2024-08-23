CREATE TABLE IF NOT EXISTS rss_url (
    url VARCHAR PRIMARY KEY NOT NULL UNIQUE,
    desc VARCHAR(40) NOT NULL,
    status VARCHAR NOT NULL CHECK(status IN ("True","False")) DEFAULT "True",
    last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS rss_news (
    url VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    detail_url VARCHAR NOT NULL,
    published VARCHAR NOT NULL,
    last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS notice_keywords (
    keyword VARCHAR(20) PRIMARY KEY,
    last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS notice_history (
    keyword VARCHAR(20) NOT NULL,
    title VARCHAR NOT NULL,
    detail_url VARCHAR NOT NULL,
    last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(18) PRIMARY KEY,
    password VARCHAR NOT NULL,
    last_update TIMESTAMP NOT NULL
);