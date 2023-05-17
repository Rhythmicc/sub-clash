from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = "0.0.14"

setup(
    name="sub-clash",
    version=VERSION,
    description="A Clash subscribe convert tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="sub-clash clash subscribe convert",
    author="RhythmLian",
    url="https://github.com/Rhythmicc/sub-clash",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["Qpro"],
    entry_points={
        "console_scripts": [
            "sub-clash = sub_clash.main:main",
        ]
    },
)
