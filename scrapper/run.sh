python manage.py shell < scrapper/utils.py
python manage.py shell < scrapper/runners/01_video_details.py   &
python manage.py shell < scrapper/runners/02_brand_deals.py     &
python manage.py shell < scrapper/runners/03_new_channels.py    &
python manage.py shell < scrapper/runners/04_validate_deals.py  &
wait

