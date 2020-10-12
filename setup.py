from setuptools import setup, find_packages
import versioneer

setup(
    name="metagraph-karateclub",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="karateclub plugins for Metagraph",
    author="Anaconda, Inc.",
    packages=find_packages(include=["metagraph_karateclub", "metagraph_karateclub.*"]),
    include_package_data=True,
    install_requires=["metagraph", "karateclub"],
    entry_points={"metagraph.plugins": "plugins=metagraph_karateclub.plugins:find_plugins"},
)
