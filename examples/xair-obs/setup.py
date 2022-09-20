from setuptools import setup

setup(
    name="xair-obs",
    description="Syncs Xair states to OBS scenes",
    install_requires=["obsws-python", "xair-api"],
)
