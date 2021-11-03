import setuptools

setuptools.setup(
    name="riscos_toolbox",
    version="0.2.0",
    author="Chris Johns",
    author_email="chris@lessthan3.org.uk",
    description="RISC OS Toolbox library",
    long_description="Library to use the RISC OS Toolbox",
    url="https://github.com/c-jo/riscos-toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: RISC OS",
    ],
    python_requires='>=3',
)
