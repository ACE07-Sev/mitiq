# Copyright (C) Unitary Foundation
#
# This source code is licensed under the GPL license (v3) found in the
# LICENSE file in the root directory of this source tree.

"""Functions to convert between Mitiq's internal circuit representation and
OpenQASM's circuit representation.
"""

from cirq import Circuit
from openqasm3.ast import Program
from qbraid.transpiler.conversions.openqasm3 import openqasm3_to_qasm3
from qbraid.transpiler.conversions.qasm3 import qasm3_to_openqasm3


def from_openqasm(circuit: Program) -> Circuit:
    """Convert a OpenQASM program to a cirq Circuit.
    Args:
        circuit (str): The OpenQASM program to convert.
    Returns:
        Circuit: The converted cirq Circuit.
    """
    from mitiq.interface.mitiq_qiskit import from_qasm

    return from_qasm(openqasm3_to_qasm3(circuit))


def to_openqasm(circuit: Circuit) -> Program:
    """Convert a cirq Circuit to OpenQASM program.
    Args:
        circuit (Circuit): The cirq Circuit to convert.
    Returns:
        str: The converted OpenQASM program.
    """
    from mitiq.interface.mitiq_qiskit import to_qasm

    return qasm3_to_openqasm3(to_qasm(circuit))  # type: ignore
