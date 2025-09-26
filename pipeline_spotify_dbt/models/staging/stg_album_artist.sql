with source as (

    select * 
    from {{ source('public', 'album_artist') }}

),

renamed as (

    select
        album_id,
        artist_id
    from source

)

select * from renamed