import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapingant-client",
    version="0.1.0",
    author="andrii.kovalenko",
    author_email="adrekoval@gmail.com",
    license='Apache-2.0',
    description="Official python client for the ScrapingAnt API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ScrapingAnt/scrapingant-client-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords="scrapingant api scraper scraping",
    python_requires='~=3.5',
    install_requires=['requests>=2,<3'],
    extras_require={
        'dev': [
            'pytest>=6,<7',
            'flake8>=3,<4',
        ]
    }
)
