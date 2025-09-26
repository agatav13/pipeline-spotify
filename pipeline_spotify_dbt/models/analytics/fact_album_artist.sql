{{ config(materialized='table') }}

select
    aa.album_id,
    al.album_name,
    aa.artist_id,
    ar.artist_name
from {{ ref('stg_album_artist') }} aa
join {{ ref('stg_album') }} al on aa.album_id = al.album_id
join {{ ref('stg_artist') }} ar on aa.artist_id = ar.artist_id 