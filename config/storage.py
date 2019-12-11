""" Storage Settings """

import os

"""
|--------------------------------------------------------------------------
| Storage Driver
|--------------------------------------------------------------------------
|
| The default driver you will like to use for storing uploads. You may add
| additional drivers as you need or pip install additional drivers.
|
| Supported: 'disk', 's3'
|
"""

DRIVER = os.getenv('STORAGE_DRIVER', 'disk')

"""
|--------------------------------------------------------------------------
| Storage Drivers
|--------------------------------------------------------------------------
|
| Different drivers you can use for storing file uploads.
|
"""

DRIVERS = {
    'disk': {
        'location': 'storage/uploads'
    },
    's3': {
        'client': os.getenv('S3_CLIENT', 'AxJz...'),
        'secret': os.getenv('S3_SECRET', 'HkZj...'),
        'bucket': os.getenv('S3_BUCKET', 's3bucket'),
    }
}


"""
|--------------------------------------------------------------------------
| Static Files
|--------------------------------------------------------------------------
|
| Put anywhere you keep your static assets in a key, value dictionary here
| The key will be the folder you put your assets in relative to the root
| and the value will be the alias you wish to have in your templates.
| You may have multiple aliases of the same name
|
| Example will be the static assets folder at /storage/static
| and an alias of <img src="/static/image.png">
|
"""

STATICFILES = {
    # folder          # template alias
    'storage/static': 'static/',
    'storage/compiled': 'static/',
    'storage/uploads': 'static/',
}
