dbt-debug:
	uv run --env-file .env dbt debug --project-dir pipeline_spotify_dbt --profiles-dir pipeline_spotify_dbt

dbt-run:
	uv run --env-file .env dbt run --project-dir pipeline_spotify_dbt --profiles-dir pipeline_spotify_dbt

dbt-test:
	uv run --env-file .env dbt test --project-dir pipeline_spotify_dbt --profiles-dir pipeline_spotify_dbt

dbt-docs:
	uv run --env-file .env dbt docs generate --project-dir pipeline_spotify_dbt --profiles-dir pipeline_spotify_dbt
	uv run --env-file .env dbt docs serve --project-dir pipeline_spotify_dbt --profiles-dir pipeline_spotify_dbt