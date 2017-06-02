from setuptools import setup, find_packages

setup(
    name="pollux",
    version=open('pollux/version.txt').read().strip(),
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'config_resolver',
        'requests',
    ],
    include_package_data=True,
    author="Michel Albert",
    author_email="michel@albert.lu",
    description="Pollen alert service for Luxembourg",
    license="BSD",
    url="https://github.com/exhuma",
)
