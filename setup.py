from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chikyu-sdk',

    version='0.9.0',

    description='GENIEE SFA/CRM SDK',

    long_description=long_description,

    url='https://github.com/chikyuinc/chikyu-sdk-python',

    author='Geniee Inc.',

    author_email='',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Bata',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='http sdk chikyu crm sfa',

    package_dir={'': 'src'},

    # Required
    packages=['chikyu_sdk',
              'chikyu_sdk.config',
              'chikyu_sdk.error',
              'chikyu_sdk.resource',
              'chikyu_sdk.helper'],

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['requests', 'requests-aws4auth', 'boto3'],  # Optional

    extras_require={
    },

    package_data={
    },

    data_files=[],

    entry_points={
        'console_scripts': [],
    },
)
