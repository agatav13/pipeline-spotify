{% test valid_release_date(model, column_name) %}

select *
from {{ model }}
where {{ column_name }} < '1900-01-01'::date
   or {{ column_name }} > (current_date + interval '1 year')

{% endtest %}