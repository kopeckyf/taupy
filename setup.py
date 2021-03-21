import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taupy",
    version="0.0.1",
    author="Felix Kopecky",
    description="A Python package to study the theory of dialectical structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kopeckyf/taupy",
    project_urls={
        "Bug Tracker": "https://github.com/kopeckyf/taupy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3 License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "taupy"},
    packages=setuptools.find_packages(where="taupy"),
    python_requires=">=3.9",
)
