from setuptools import setup, find_packages

__version__ = "0.0.1"

setup(
    name="procgen-cli",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=["click~=7.1.2", "PyYAML~=5.3.1", "rich~=6.0.0"],
    entry_points={"console_scripts": ["procgen-cli = procgen_cli:cli"]},
    include_package_data=True,
)
