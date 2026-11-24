CREATE DATABASE IF NOT EXISTS dontquotemeDB;
USE dontquotemeDB;

CREATE TABLE clients(
  guild_id INTEGER PRIMARY KEY,
  last_activity FLOAT
);
CREATE TABLE players(
  guild_id INTEGER NOT NULL,
  player_name VARCHAR(255) NOT NULL,
  is_active BOOLEAN,
  
  PRIMARY KEY(guild_id, player_name),
  FOREIGN KEY (guild_id) REFERENCES clients(guild_id) ON DELETE CASCADE
);
CREATE TABLE aliases(
  guild_id INTEGER NOT NULL,
  alias_name VARCHAR(255) NOT NULL,
  player_name VARCHAR(255) NOT NULL,

  PRIMARY KEY(guild_id, alias_name),
  FOREIGN KEY (guild_id) REFERENCES clients(guild_id) ON DELETE CASCADE,
  FOREIGN KEY (player_name) REFERENCES players(player_name) ON DELETE CASCADE
);
CREATE TABLE rulesets(
  guild_id INTEGER NOT NULL,
  ruleset_name VARCHAR(255) NOT NULL,
  is_active BOOLEAN,
  round_limit INTEGER,
  game_type INTEGER,
  allow_aliases BOOLEAN,
  channel_id INTEGER,
  scrape_from FLOAT,
  scrape_to FLOAT,
  
  PRIMARY KEY(guild_id, ruleset_name),
  FOREIGN KEY (guild_id) REFERENCES clients(guild_id) ON DELETE CASCADE
);

-- Convert to separate NoSQL/SQLite DB
-- CREATE TABLE quotes(
--   guild_id INTEGER NOT NULL,
--   message_id INTEGER NOT NULL,
--   PRIMARY KEY(guild_id, message_id),
--   player_name VARCHAR(255) NOT NULL,
--   quote_string TEXT NOT NULL,
--   context_string TEXT NOT NULL
-- );