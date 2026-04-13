# Golden Rules — DuckDB

## Règle critique

`CREATE TABLE AS SELECT` ne préserve PAS les PRIMARY KEY/FK. Toujours utiliser le DDL original + `INSERT INTO ... SELECT` pour les migrations de tables.
