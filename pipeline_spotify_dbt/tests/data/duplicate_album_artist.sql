select album_id, artist_id, count(*) as duplicates
from {{ ref('fact_album_artist') }}
group by album_id, artist_id
having count(*) > 1