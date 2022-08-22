from jdict import jdict
from caios.service.config_base import get_default_config_base
from caios.abc.mutable_mapping import Mapping, MutableMapping
from caios.abc.mutable_storage import MutableStorage

SECRET_ID = "jira_micro_app_creds_id"
SECRET_NAME = "jira_micro_app_creds_name"


def get_configuration(service_name: str, mode: str) -> tuple[jdict, ...]:
    """
    Return a default configuration for development
    """
    return (
        *get_default_config_base(), 
        jdict(
            resource='GSpread',
            interface='MutableMapping',
            secret='jira_micro_app_google_creds_id',
            scope=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'],
            name='jira_test'
        ),
        jdict(
            resource='SecretsManager',
            interface='Secret',
            name=SECRET_NAME,
            id=SECRET_ID
        )
    )
