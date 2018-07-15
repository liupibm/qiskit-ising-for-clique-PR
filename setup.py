# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import setuptools

long_description="""<a href="https://qiskit.org/acqua" rel=nofollow>QISKit ACQUA</a> is an extensible, 
 modular, open-source library of quantum computing algorithms.
 Researchers can experiment with ACQUA algorithms, on near-term quantum devices and simulators, 
 and can also get involved by contributing new algorithms and algorithm-supporting objects, 
 such as optimizers and variational forms. QISKit ACQUA is used by QISKit ACQUA Chemistry, 
 QISKit ACQUA Artificial Intelligence, and QISKit ACQUA Optimization to experiment with real-world applications to quantum computing."""
    
requirements = [
    "qiskit>=0.5.6",
    "scipy>=0.19,<1.2",
    "numpy>=1.13,<1.15",
    "psutil",
    "jsonschema",
    "scikit-learn",
    "cvxopt",
    "pyobjc-core; sys_platform == 'darwin'",
    "pyobjc-framework-Cocoa; sys_platform == 'darwin'"
]

setuptools.setup(
    name='qiskit-acqua',
    version="0.1.2",  # this should match __init__.__version__
    description='QISKit ACQUA: An extensible library of quantum computing algorithms',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/QISKit/qiskit-acqua',
    author='QISKit ACQUA Development Team',
    author_email='qiskit@us.ibm.com',
    license='Apache-2.0',
    classifiers=(
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering"
    ),
    keywords='qiskit sdk quantum acqua',
    packages=setuptools.find_packages(exclude=['test*']),
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.5",
    entry_points = {
        'console_scripts': [
                'qiskit_acqua_cmd=qiskit_acqua.command_line:main'
        ],
        'gui_scripts': [
                'qiskit_acqua_ui=qiskit_acqua.ui.run.command_line:main',
                'qiskit_acqua_browser=qiskit_acqua.ui.browser.command_line:main'
        ]
    }
)