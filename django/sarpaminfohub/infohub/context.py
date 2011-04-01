# pylint:disable-msg=W0613
def extra_number_settings_context(request):
    from django.conf import settings
    return {
        'sarpam_number_format':settings.SARPAM_NUMBER_FORMAT,
        'sarpam_number_rounding':settings.SARPAM_NUMBER_ROUNDING,
        'sarpam_currency_code':settings.SARPAM_CURRENCY_CODE
    }