from setuptools import setup, find_packages

setup(
    name="panic-trap",
    version="1.0.0",
    author="Emre Kırdım",
    description="A Behavioral Biometric Intrusion Detection System based on Keystroke Dynamics.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/deimooos/Panic-Trap",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Security",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pynput>=1.7.6",
        "numpy>=1.26.4",
        "customtkinter>=5.2.2",
        "requests>=2.31.0",
        "pygetwindow>=0.0.9",
        "pyperclip>=1.8.2"
    ],
    entry_points={
        "console_scripts": [
            "panic-trap=main:main",
        ],
    },
)