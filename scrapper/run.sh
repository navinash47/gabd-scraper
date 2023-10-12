#!/bin/bash
# Run this atleast 4 times
rm error.txt
num_loops=100

for ((i=1; i<=$num_loops; i++)); do
    echo "----------------------LOOP $i----------------------"
    python manage.py shell < scrapper/pre_runner.py
    python manage.py shell < scrapper/runners/01_video_details.py &
    python manage.py shell < scrapper/runners/02_brand_deals.py &
    python manage.py shell < scrapper/runners/03_new_channels.py &
    python manage.py shell < scrapper/runners/04_validate_deals.py &
    wait
    python manage.py shell < scrapper/post_runner.py | tee outputs/output_post_runner.txt
done

echo "----------------------ERRORS----------------------"
cat error.txt

echo "Uploading the db to supabase..."
source .env
pg_dump $OLD_DB_URL > database_dump.dump
psql $NEW_DB_URL < database_dump.dump

echo "Done uploading the db to supabase"
