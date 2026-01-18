from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="screensnap",
    version="1.0.0",
    author="Atlas (Team Brain)",
    author_email="logan@metaphy.dev",
    description="Simple cross-platform screenshot tool for troubleshooting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/ScreenSnap",
    py_modules=["screensnap"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ],
    python_requires='>=3.8',
    install_requires=[
        'pillow>=10.0.0',
    ],
    entry_points={
        'console_scripts': [
            'screensnap=screensnap:main',
        ],
    },
)
