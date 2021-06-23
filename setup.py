from setuptools import find_packages, setup

setup(
    name="pollux",
    version="0.1.0",
    description="Pollen alert service for Luxembourg",
    url="https://github.com/exhuma/pollux",
    long_description=open("README.rst").read(),
    author="Michel Albert",
    author_email="michel@albert.lu",
    license="BSD",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "pandas >=1.2.4",
        "bcrypt >=3.2.0, <4.0",
        "beautifulsoup4 >=4.9.2, <5.0",
        "config_resolver >=5.0.2, <6.0",
        "flask >=1.1.2, <2.0",
        "pyjwt >=1.7.1, <2.0",
        "requests >=2.24.0, <3.0",
        "gouge >=1.5.0, <2.0",
        "importlib_metadata >=2.0.0, <3.0; python_version<'3.8'",
    ],
    entry_points={
        "console_scripts": [
            "fetch_pollen_csv = pollux.cli:fetch_csv",
        ]
    },
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pylint",
            "mypy",
            "fabric",
        ]
    },
)
