{{ config(materialized='table') }}

select 
    artist_id,
    artist_name,
    spotify_url
from {{ ref('stg_artist') }}