# Copyright 2019 Lorenzo Cabrini
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import setuptools

longdesc = """\
Pigrizia is a library for automation, monitoring and reporting.
"""

setuptools.setup(
        name='pigrizia',
        version='0.0.1',
        author='Lorenzo Cabrini',
        author_email='lorenzo.cabrini@gmail.com',
        description='Pigrizia is a library for automation',
        long_description=longdesc,
        url="https://github.com/lcabrini/pigrizia",
        packages=setuptools.find_packages(),
        install_requires=[
            'paramiko',
            ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Linux"
            ],
        python_requires='>=3.7',
        )
