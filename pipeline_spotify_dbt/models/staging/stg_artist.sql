with source as (

    select * 
    from {{ source('public', 'artist') }}

),

renamed as (

    select
        artist_id,
        artist_name,
        spotify_url,
        extracted_at,
        processed_at
    from source

)

select * from renamed