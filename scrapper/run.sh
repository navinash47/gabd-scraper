#!/bin/bash
# Run this atleast 4 times
# rm error.txt
# num_loops=100

# for ((i=1; i<=$num_loops; i++)); do
#     echo "----------------------LOOP $i----------------------"
#     python manage.py shell < scrapper/pre_runner.py
#     python manage.py shell < scrapper/runners/01_video_details.py &
#     python manage.py shell < scrapper/runners/02_brand_deals.py &
#     python manage.py shell < scrapper/runners/03_new_channels.py &
#     python manage.py shell < scrapper/runners/04_validate_deals.py &
#     wait
#     python manage.py shell < scrapper/post_runner.py | tee outputs/output_post_runner.txt
# done

# echo "----------------------ERRORS----------------------"
# cat error.txt

echo "Uploading the db to supabase..."

source .env
supabase db dump --db-url "$OLD_DB_URL" -f roles.sql --role-only
supabase db dump --db-url "$OLD_DB_URL" -f schema.sql
supabase db dump --db-url "$OLD_DB_URL" -f data.sql --use-copy --data-only
psql \
  --single-transaction \
  --variable ON_ERROR_STOP=1 \
  --file roles.sql \
  --file schema.sql \
  --file data.sql \
  --dbname "$NEW_DB_URL"

echo "Done uploading the db to supabase"
