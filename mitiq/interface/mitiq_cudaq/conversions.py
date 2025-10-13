# Copyright (C) Unitary Foundation
#
# This source code is licensed under the GPL license (v3) found in the
# LICENSE file in the root directory of this source tree.

"""Functions to convert between Mitiq's internal circuit representation and
Cuda-Quantum's circuit representation.
"""

from cirq import Circuit
from cudaq import PyKernel
from qbraid.transpiler.conversions.cirq import cirq_to_qasm2
from qbraid.transpiler.conversions.cudaq import cudaq_to_qasm2
from qbraid.transpiler.conversions.openqasm3 import openqasm3_to_cudaq
from qbraid.transpiler.conversions.qasm2 import qasm2_to_cirq, qasm2_to_qiskit
from qbraid.transpiler.conversions.qasm3 import qasm3_to_openqasm3
from qbraid.transpiler.conversions.qiskit import qiskit_to_qasm3


def from_cudaq(kernel: PyKernel) -> Circuit:
    """Convert a cudaq PyKernel to a cirq Circuit via OpenQASM 3.

    Args:
        kernel (PyKernel): The cudaq PyKernel to convert.

    Returns:
        Circuit: The converted cirq Circuit.
    """
    qasm2_str = cudaq_to_qasm2(kernel)
    return qasm2_to_cirq(qasm2_str)


def to_cudaq(circuit: Circuit) -> PyKernel:
    """Convert a cirq Circuit to a cudaq PyKernel via OpenQASM 3.

    Args:
        circuit (Circuit): The cirq Circuit to convert.

    Returns:
        PyKernel: The converted cudaq PyKernel.
    """
    from qiskit import transpile

    qasm2_str = cirq_to_qasm2(circuit)
    qiskit_qc = qasm2_to_qiskit(qasm2_str)
    # We need to transpile as `openqasm3_to_cudaq` cannot work
    # with arbitrary gates, i.e., ccx, rxx, etc.
    qiskit_qc = transpile(qiskit_qc, basis_gates=["u3", "cx"])
    qasm3_str = qiskit_to_qasm3(qiskit_qc)
    openqasm3_str = qasm3_to_openqasm3(qasm3_str)
    cudaq_qc = openqasm3_to_cudaq(openqasm3_str)

    return cudaq_qc
