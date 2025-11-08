from typing import Literal, TypeAlias, get_args

__all__ = [
    'ApiSupportedContent',
    'ApiSupported',
    'API_SUPPORTED_CONTENT_TYPES',
    'EndPointUrl',
    'UrlType',
    'ApiEndpoints',
]

ApiSupportedContent: TypeAlias = Literal['huggingface_hub', 'openai', 'requests']

ApiSupported: TypeAlias = list[Literal['huggingface_hub', 'openai', 'requests']]

# Concrete instance derived from the type - single source of truth
API_SUPPORTED_CONTENT_TYPES: ApiSupported = list(get_args(ApiSupportedContent))

EndPointUrl: TypeAlias = str
UrlType: TypeAlias = str

ApiEndpoints: TypeAlias = dict[ApiSupportedContent, EndPointUrl]
