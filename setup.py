import os

from setuptools import setup, find_packages


import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="chargily-epay-django",  # Required
    version="0.0.1",  # Required
    description="Chargily ePay Gateway (Django Library)",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/Chargily/chargily-epay-django",  # Optional
    author="Tarek berkane",  # Optional
    author_email="tarekg320@example.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    include_package_data = True,
    keywords="e-pay, chargily, edahabia, cib, django",  # Optional
    package_dir={"": "src"},  # Optional
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.7",
    install_requires=["chargily-epay"],  # Optional
    project_urls={  # Optional
        "Bug Reports": "https://github.com/Chargily/chargily-epay-django/issues",
        "Funding": "https://donate.pypi.org",
        "Say Thanks!": "https://github.com/Chargily",
        "Source": "https://github.com/Chargily/chargily-epay-django/",
    },
)
