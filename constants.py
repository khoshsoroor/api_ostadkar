import os

SRID = 4326
DEFAULT_LOCALE = 'fa-IR'
DEFAULT_TIMEZONE = 'Asia/Tehran'
DEFAULT_CHARSET = 'utf-8'
ODATA_COUNT = 'odata.count'
ODATA_VALUE = 'value'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'

MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 10


class PostGreSQL:
    EPOCH = 'epoch'
    AtTimeZone = 'AT TIME ZONE'


class ConfigKeys:
    LogLevel = "LOG_LEVEL"
    NTPServer = "TIME_SERVER"
    DefaultPageSize = "DEFAULT_PAGE_SIZE"
    MaxPageSize = "MAX_PAGE_SIZE"
    DefaultLocale = "DEFAULT_LOCALE"
    DefaultCharset = "DEFAULT_CHARSET"
    BaseUri = "BASE_URI"


class EmptyMessages:
    EmptyPackageType = "EmptyPackage"
    EmptyWaybill = "EmptyWaybill"


class RegExPatterns:
    Email = '^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$'
    CellNumber = '(0|\+98)?([ ]|,|-|[()]){0,2}9[0-9]([ ]|,|-|[()]){0,2}(?:[0-9]([ ]|,|-|[()]){0,2}){8}'
    Locale = '[a-z]{2}-[A-Z]{2}'


class HeaderKeys:
    ContentType = 'Content-Type'
    Accept = 'Accept'
    AcceptLanguage = 'Accept-Language'
    ContentLanguage = 'Content-Language'
    Serialization = 'X-Serialization'


class MimeTypes:
    JSON = 'application/json'
    MessagePack = 'application/msgpack'
    CBOR = 'application/cbor'
    URLEncoded = 'application/x-www-form-urlencoded'


class SerializerFlags:
    IncludeNulls = 'IncludeNulls'
    ReplaceNullsWithEmpty = 'ReplaceNullsWithEmpty'
