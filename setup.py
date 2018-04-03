from setuptools import setup

setup(
    name='lektor-read-full-post',
    version='0.1',
    author='Andrew Shay',
    url='https://andrewshay.me',
    license='MIT',
    py_modules=['lektor_read_full_post'],
    entry_points={
        'lektor.plugins': [
            'read-full-post = lektor_read_full_post:ReadFullPostPlugin',
        ]
    }
)
