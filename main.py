
from qiskit import Aer, transpile
from qiskit import QuantumCircuit
from qiskit.providers.ibmq import IBMQ, least_busy
from qiskit.providers.ibmq.job import job_monitor
from qiskit.quantum_info import Operator

from qiskit.visualization import plot_histogram, array_to_latex

from utils.bit_value.bit_value import BitValue
from utils.db import DB

db_array = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]
find_value = BitValue([0, 1])

class Grover:
    def __init__(self):
        self.db = DB()
        self.db_raw_len = len(db_array[0])
        for raw in db_array:
            assert len(raw) == self.db_raw_len
            self.db.append(BitValue(raw))
        self.grover_circuit = QuantumCircuit(self.db_raw_len)
        self.initialize_circuit()

    def initialize_circuit(self):
        """
        Инициализирует кубиты

        :return:
        """
        for q in range(self.db_raw_len):
            self.grover_circuit.h(q)

    def diffuser(self):
        qc = QuantumCircuit(self.db_raw_len)

        # Apply transformation |s> -> |00..0> (H-gates)
        for qubit in range(self.db_raw_len):
            qc.h(qubit)
            qc.x(qubit)

        # Do multi-controlled-Z gate
        qc.h(self.db_raw_len-1)
        qc.mct(list(range(self.db_raw_len - 1)), self.db_raw_len-1)  # multi-controlled-toffoli
        qc.h(self.db_raw_len-1)

        # Apply transformation |11..1> -> |00..0>
        for qubit in range(self.db_raw_len):
            qc.x(qubit)
            qc.h(qubit)

        return qc

    def run(self):
        """
        Запуск квантового алгоритма

        :return:
        """

        self.grover_circuit.unitary(self.db.quantum_oracle(find_value), [0, 1], label='oracle')

        self.grover_circuit.append(Operator(self.diffuser()), [0, 1])

    def simulate(self):
        """
        Запускает симуляцию алгоритма

        :return:
        """
        sv_sim = Aer.get_backend('statevector_simulator')
        result = sv_sim.run(self.grover_circuit).result()
        statevec = result.get_statevector()
        array_to_latex(statevec, prefix="|\\psi\\rangle =")
        self.grover_circuit.measure_all()

        qasm_sim = Aer.get_backend('qasm_simulator')
        result = qasm_sim.run(self.grover_circuit).result()
        counts = result.get_counts()
        hist = plot_histogram(counts)
        hist.show()

    def real_run(self):
        """
        Теоретически, запускает код на реальном квантовом компьютере,
        но у меня нет доступа и не проверить

        :return:
        """
        provider = IBMQ.load_account()
        provider = IBMQ.get_provider("ibm-q")
        device = least_busy(
            provider.backends(
                filters=lambda x:
                x.configuration().n_qubits >= 3 and
                not x.configuration().simulator and
                x.status().operational == True
            )
        )
        transpiled_grover_circuit = transpile(self.grover_circuit, device, optimization_level=3)
        job = device.run(transpiled_grover_circuit)
        job_monitor(job, interval=2)
        results = job.result()
        answer = results.get_counts(self.grover_circuit)
        hist = plot_histogram(answer)
        hist.show()


g = Grover()
g.run()
g.simulate()
