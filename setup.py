"""
Setup file for the Xinshuo's Python Toolbox package.
"""

from setuptools import find_packages, setup
setup(
    name="ab3dmot",
    version="1.0.0",
    author="Xinshuo Weng",
    author_email="xinshuo.weng@gmail.com",
    description="(IROS 2020, ECCVW 2020) Official Python Implementation for '3D Multi-Object Tracking: A Baseline and New Evaluation Metrics",
    long_description=open("readme.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xinshuoweng/AB3DMOT",
    packages=find_packages(),
    install_requires=[
        'easydict==1.13',
        'filterpy==1.4.5',
        'fire==0.6.0',
        'matplotlib==3.8.2',
        'numba==0.59.0',
        'numpy==1.24.3',
        'opencv_python==4.9.0.80',
        'opencv_python_headless==4.9.0.80',
        'ordereddict==1.1',
        'Pillow==10.3.0',
        'pyquaternion==0.9.9',
        'PyYAML==6.0.1',
        'scipy==1.13.0',
        'setuptools==65.5.0',
        'xinshuo_py_toolbox==1.0.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

