from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):
    help = 'remove all expired otp codes from data base'

    def handle(self, *args, **kwargs):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write(self.style.SUCCESS('all expired codes removed from data base.'))

