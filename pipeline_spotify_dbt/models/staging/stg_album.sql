with source as (
    select * from {{ source('public', 'album') }}
),
renamed as (
    select
        album_id,
        album_name,
        album_type,
        release_date,
        release_year,
        release_date_precision,
        total_tracks,
        image_url,
        spotify_url,

        extracted_at,
        extraction_type,
        processed_at,
        data_type
    from source
)

select * from renamed