# Extract emails from the description
import re
from scrapper.models import Channel

email_regex = r"[\w\.-]+@[\w\.-]+\.\w+"

emails = []
for channel in Channel.objects.filter(status=Channel.FETCHED):
    channel_emails = re.findall(email_regex, channel.description)
    if len(channel_emails) > 0:
        print(channel.title, channel_emails)
        print("--------------------------------")

# python manage.py shell < _custom/tools/emails.py
