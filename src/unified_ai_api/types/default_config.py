from typing import TypedDict

__all__ = ['DefaultsConfig']

class DefaultsConfig(TypedDict, total=False):
    '''Type definition for defaults configuration file.'''

    _comment: str
    _description: str
    _version: str
    _last_updated: str
    default_provider: str
    default_config_index: int
    default_api_type: str
    timeouts: dict[str, int]
    retry_policy: dict[str, float | int]
    logging: dict[str, str]
