#Rate limiting
from slowapi import Limiter 
from slowapi.util import get_remote_address


# limiter = Limiter(key_func=get_remote_address,default_limits=['5/minute'])

limiter = Limiter(key_func=get_remote_address, storage_uri='redis://localhost:6379',default_limits=['5/minute'])
