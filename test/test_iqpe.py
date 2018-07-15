# -*- coding: utf-8 -*-

# Copyright 2018 IBM RESEARCH. All Rights Reserved.
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

import unittest
from parameterized import parameterized
from qiskit_acqua import get_algorithm_instance, get_initial_state_instance, Operator
from qiskit_acqua.utils import decimal_to_binary
import numpy as np
from scipy.linalg import expm
from test.common import QISKitAcquaTestCase


pauli_dict = {
    'paulis': [
        {"coeff": {"imag": 0.0, "real": -1.052373245772859}, "label": "II"},
        {"coeff": {"imag": 0.0, "real": 0.39793742484318045}, "label": "ZI"},
        {"coeff": {"imag": 0.0, "real": -0.39793742484318045}, "label": "IZ"},
        {"coeff": {"imag": 0.0, "real": -0.01128010425623538}, "label": "ZZ"},
        {"coeff": {"imag": 0.0, "real": 0.18093119978423156}, "label": "XX"}
    ]
}
qubitOp_h2_with_2_qubit_reduction = Operator.load_from_dict(pauli_dict)


class TestIQPE(QISKitAcquaTestCase):
    """QPE tests."""

    @parameterized.expand([
        [qubitOp_h2_with_2_qubit_reduction],
    ])
    def test_qpe(self, qubitOp):
        self.algorithm = 'QPE'
        self.log.debug('Testing QPE')

        self.qubitOp = qubitOp

        exact_eigensolver = get_algorithm_instance('ExactEigensolver')
        exact_eigensolver.init_args(self.qubitOp, k=1)
        results = exact_eigensolver.run()

        w = results['eigvals']
        v = results['eigvecs']

        self.qubitOp._check_representation('matrix')
        np.testing.assert_almost_equal(
            self.qubitOp.matrix @ v[0],
            w[0] * v[0]
        )
        np.testing.assert_almost_equal(
            expm(-1.j * self.qubitOp.matrix) @ v[0],
            np.exp(-1.j * w[0]) * v[0]
        )

        self.ref_eigenval = w[0]
        self.ref_eigenvec = v[0]
        self.log.debug('The exact eigenvalue is:       {}'.format(self.ref_eigenval))
        self.log.debug('The corresponding eigenvector: {}'.format(self.ref_eigenvec))

        num_time_slices = 50
        num_iterations = 12

        iqpe = get_algorithm_instance('IQPE')
        iqpe.setup_quantum_backend(backend='local_qasm_simulator', shots=100, skip_transpiler=True)

        state_in = get_initial_state_instance('CUSTOM')
        state_in.init_args(self.qubitOp.num_qubits, state_vector=self.ref_eigenvec)

        iqpe.init_args(
            self.qubitOp, state_in, num_time_slices, num_iterations,
            paulis_grouping='random',
            expansion_mode='suzuki',
            expansion_order=2,
        )

        result = iqpe.run()
        # self.log.debug('operator paulis:\n{}'.format(self.qubitOp.print_operators('paulis')))
        # self.log.debug('qpe circuit:\n\n{}'.format(result['circuit']['complete'].qasm()))

        self.log.debug('top result str label:         {}'.format(result['top_measurement_label']))
        self.log.debug('top result in decimal:        {}'.format(result['top_measurement_decimal']))
        self.log.debug('stretch:                      {}'.format(result['stretch']))
        self.log.debug('translation:                  {}'.format(result['translation']))
        self.log.debug('final eigenvalue from QPE:    {}'.format(result['energy']))
        self.log.debug('reference eigenvalue:         {}'.format(self.ref_eigenval))
        self.log.debug('ref eigenvalue (transformed): {}'.format(
            (self.ref_eigenval + result['translation']) * result['stretch'])
        )
        self.log.debug('reference binary str label:   {}'.format(decimal_to_binary(
            (self.ref_eigenval + result['translation']) * result['stretch'],
            max_num_digits=num_iterations + 3,
            fractional_part_only=True
        )))

        np.testing.assert_approx_equal(self.ref_eigenval, result['energy'], significant=2)


if __name__ == '__main__':
    unittest.main()
