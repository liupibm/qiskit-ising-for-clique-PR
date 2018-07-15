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

import logging

from scipy.optimize import minimize

from qiskit_acqua.utils.optimizers import Optimizer

logger = logging.getLogger(__name__)


class COBYLA(Optimizer):
    """Constrained Optimization By Linear Approximation algorithm.

    Uses scipy.optimize.minimize COBYLA
    See https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
    """

    COBYLA_CONFIGURATION = {
        'name': 'COBYLA',
        'description': 'COBYLA Optimizer',
        'input_schema': {
            '$schema': 'http://json-schema.org/schema#',
            'id': 'cobyla_schema',
            'type': 'object',
            'properties': {
                'maxiter': {
                    'type': 'integer',
                    'default': 1000
                },
                'disp': {
                    'type': 'boolean',
                    'default': False
                },
                'rhobeg': {
                    'type': 'number',
                    'default': 1.0
                },
                'tol': {
                    'type': ['number', 'null'],
                    'default': None
                }
            },
            'additionalProperties': False
        },
        'support_level': {
            'gradient': Optimizer.SupportLevel.ignored,
            'bounds': Optimizer.SupportLevel.ignored,
            'initial_point': Optimizer.SupportLevel.required
        },
        'options': ['maxiter', 'disp', 'rhobeg'],
        'optimizer': ['local']
    }

    def __init__(self, configuration=None):
        super().__init__(configuration or self.COBYLA_CONFIGURATION.copy())
        self._tol = None

    def init_args(self, tol=None):
        self._tol = tol

    def optimize(self, num_vars, objective_function, gradient_function=None, variable_bounds=None, initial_point=None):
        super().optimize(num_vars, objective_function, gradient_function, variable_bounds, initial_point)

        res = minimize(objective_function, initial_point, tol=self._tol, method="COBYLA", options=self._options)
        return res.x, res.fun, res.nfev
