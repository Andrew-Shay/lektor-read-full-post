from setuptools import setup

setup(
    name='lektor-read-full-post',
    version='0.3',
    author='Andrew Shay',
    url='https://andrewshay.me',
    long_description="Lektor plugin that allows blog listing posts to be shortened with a link to the full post.",
    license='MIT',
    py_modules=['lektor_read_full_post'],
    entry_points={
        'lektor.plugins': [
            'read-full-post = lektor_read_full_post:ReadFullPostPlugin',
        ]
    }
)
