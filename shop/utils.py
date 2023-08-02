from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(phone_number, code):
    '''
    this function send an one time password  by kavenegar service
    '''
    try:
        api = KavenegarAPI('2B3242307037572F525245516459744F634754415753526367514A6767306F54422F61366B58456269786B3D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'enter this code  {code}'
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


class ISAdminUserMixin(UserPassesTestMixin):
    '''
    This class checks if it is a superuser or not. If it is not superuser,
     it does not allow to display and delete the page.
    '''
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
