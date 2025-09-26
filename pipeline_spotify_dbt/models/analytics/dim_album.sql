{{ config(materialized='table') }}

select
    album_id,
    album_name,
    album_type,
    release_date,
    total_tracks,
    image_url,
    spotify_url
from {{ ref('stg_album') }}