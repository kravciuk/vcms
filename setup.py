from setuptools import setup
import sys

setup(
    # Basic package information.
    name = 'vcms',
    version = '1.1.0',
    packages = ['vcms'],
    include_package_data = True,
    install_requires = [],
    url = 'https://github.com/kravciuk/vcms',
    keywords = 'vcms',
    description = 'CMS',
    classifiers = [
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)

