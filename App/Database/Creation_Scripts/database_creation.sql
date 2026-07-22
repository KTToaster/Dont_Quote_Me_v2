CREATE DATABASE IF NOT EXISTS dontquotemeDB;
USE dontquotemeDB;
CREATE TABLE clients(
  guild_id INTEGER PRIMARY KEY,
  game_index INTEGER
);
CREATE TABLE players(
  guild_id INTEGER NOT NULL,
  player_name VARCHAR(255) NOT NULL,
  PRIMARY KEY(guild_id, player_name)
);
CREATE TABLE aliases(
  guild_id INTEGER NOT NULL,
  alias_name VARCHAR(255) NOT NULL,
  PRIMARY KEY(guild_id, alias_name),
  player_name VARCHAR(255) NOT NULL
);
CREATE TABLE rulesets(
  guild_id INTEGER NOT NULL,
  ruleset_name VARCHAR(255) NOT NULL,
  PRIMARY KEY(guild_id, ruleset_name),
  is_active BOOLEAN,
  round_limit INTEGER,
  game_type INTEGER,
  strict_names BOOLEAN,
  channel_id INTEGER
);
CREATE TABLE quotes(
  guild_id INTEGER NOT NULL,
  message_id INTEGER NOT NULL,
  PRIMARY KEY(guild_id, message_id),
  player_name VARCHAR(255) NOT NULL,
  quote_string TEXT NOT NULL,
  context_string TEXT NOT NULL,
  game_index INTEGER
);