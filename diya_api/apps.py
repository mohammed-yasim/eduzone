from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DiyaApiConfig(AppConfig):
    name = 'diya_api'
    verbose_name = _("Application Program Interface")
