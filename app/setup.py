from setuptools import setup, find_packages

setup(
    name="snowvillage",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "streamlit.components.v1": [
            "launch_screen = snowvillage.launch_screen"
        ]
    },
)