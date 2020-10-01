from setuptools import setup, find_packages


with open("README.md") as readme_file:
    readme = readme_file.read()
    # FIXME: Convert to ReST


requirements = "pyyaml pandas humanfriendly tqdm exifread pillow jsonschema".split()

setup(
    name="weedcoco",
    version="0.1.0",
    description="Tools for WeedCOCO agricultural image annotation interchange",
    author="Henry Lydecker, Joel Nothman, Sydney Informatics Hub",
    long_description=readme,
    include_package_data=True,
    packages=find_packages(include=["weedcoco", "weedcoco.*"]),
    license="BSD",
    author_email="henry.lydecker@sydney.edu.au",
    keywords=[""],
    python_requires=">=3.6",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
    ],
)
