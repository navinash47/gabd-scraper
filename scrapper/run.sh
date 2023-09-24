# Run this atleast 4 times
rm error.txt
python manage.py shell < scrapper/pre_runner.py | tee outputs/output_pre_runner.txt
python manage.py shell < scrapper/runners/01_video_details.py | tee outputs/output_01.txt &
python manage.py shell < scrapper/runners/02_brand_deals.py | tee outputs/output_02.txt &
python manage.py shell < scrapper/runners/03_new_channels.py | tee outputs/output_03.txt &
python manage.py shell < scrapper/runners/04_validate_deals.py | tee outputs/output_04.txt &
wait
python manage.py shell < scrapper/post_runner.py | tee outputs/output_post_runner.txt
cat error.txt
