-- ============================================
-- schema.sql — структура базы данных
-- Создание таблиц. Концептуально отдельно от данных.
-- ============================================

CREATE TABLE IF NOT EXISTS teams (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    city    VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS players (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL,
    position    VARCHAR(100) NOT NULL,
    birth_date  DATE NOT NULL,
    height      INT  NOT NULL,
    team_id     INT  REFERENCES teams(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS news (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    content     TEXT NOT NULL,
    image_path  VARCHAR(255),
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contacts (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL,
    email       VARCHAR(150) NOT NULL,
    message     TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
);
