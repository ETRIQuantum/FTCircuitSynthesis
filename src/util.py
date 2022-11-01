
# -*-coding:utf-8-*-

# This code is part of ftsynthesis
# (fault-tolerant quantum circuit synthesis for fault-tolerant quantum protocols)
#
# Copyright 2022 ETRI
#
# This code is licensed under the BSD-3-Clause.

'''
    module for checkup functions
'''

import pandas
import globalVariable as g


def display_qubit_movements(system_code, lattice_size, **kwargs):
    """
        function to display the qubit move on the 2d array of size "lattice_size"
    """
    # initial mapping
    qubit_mapping = system_code["initial_mapping"]
    inverse_mapping = {v: k for k, v in qubit_mapping.items()}

    layout = [[0 for i in range(lattice_size["width"])]
                 for j in range(lattice_size["height"])]

    for idx, qubit in inverse_mapping.items():
        x_coord = int(idx/lattice_size["width"])
        z_coord = int(idx%lattice_size["width"])

        layout[x_coord][z_coord] = qubit

    print(" =====================================================  ")
    print("Initial Mapping: ")
    print(" -----------------------------------------------------  ")
    print(pandas.DataFrame(layout).to_string())
    print(" =====================================================  ")

    circuit_depth = max(list(system_code["circuit"].keys())) + 1
    # circuit

    for idx in range(circuit_depth):
        instructions = system_code["circuit"][idx]

        flag_swap = False
        print(" =====================================================")
        print(f"instructions at {idx}-th index : {instructions}")
        print(" -----------------------------------------------------")

        for inst in instructions:
            tokens = inst.split(" ")

            if tokens[0] in ["CNOT"]:
                qubits = list(map(int, tokens[1].split(",")))

                print(f"""{tokens[0]} qubits ({qubits[0]}, {qubits[1]})
                       -> ({inverse_mapping[qubits[0]]}, {inverse_mapping[qubits[1]]})""")

                flag_swap = False

            elif tokens[0] in ["SWAP"]:
                qubits = list(map(int, tokens[1].split(",")))

                print(f"""{tokens[0]} qubits ({qubits[0]}, {qubits[1]})
                      -> ({inverse_mapping[qubits[0]]}, {inverse_mapping[qubits[1]]})""")

                inverse_mapping[qubits[0]], inverse_mapping[qubits[1]] =\
                    inverse_mapping[qubits[1]], inverse_mapping[qubits[0]]

                flag_swap = True

            elif tokens[0] in [g.str_barrier_all]:
                print(f" {tokens[0]}")
                flag_swap = False

            else:
                qubit = int(tokens[1])
                print(f" {tokens[0]} ({qubit}) -> {inverse_mapping[qubit]}")
                flag_swap = False

        if flag_swap:
            # form 2d array
            for idx, qubit in inverse_mapping.items():
                x_coord = int(idx/lattice_size["width"])
                z_coord = int(idx%lattice_size["width"])

                layout[x_coord][z_coord] = qubit

        print(pandas.DataFrame(layout).to_string())
        print(" =====================================================")


def display_qubit_mapping(qubit_mapping, layout_size):
    """
        function to display the qubit mapping
    """
    layout = [[0. for i in range(layout_size["width"])]
                 for j in range(layout_size["height"])]

    for key, value in qubit_mapping.items():
        x_coord = int(value/layout_size["width"])
        z_coord = int(value%layout_size["width"])

        layout[x_coord][z_coord] = key

    print()
    print("===============================================")
    print(pandas.DataFrame(layout))
    print("===============================================")


def merge_qubit_layout(mapping1, mapping2, direction, layout_size):
    """
        function to merge both qubit layouts
    """

    extended_qubit_layout = {}

    if direction == "horizon":
        for key, value in mapping1.items():
            x_coord = int(key/layout_size["width"])
            z_coord = int(key%layout_size["width"])

            extended_index = x_coord * 2 * layout_size["width"] + z_coord
            extended_qubit_layout[extended_index] = value

        for key, value in mapping2.items():
            x_coord = int(key/layout_size["width"])
            z_coord = int(key%layout_size["width"])

            extended_index = x_coord * 2 * layout_size["width"] + z_coord + \
                             layout_size["width"]
            extended_qubit_layout[extended_index] = value

    elif direction == "vertical":
        extended_qubit_layout = mapping1
        for key, value in mapping2.items():
            x_coord = int(key/layout_size["width"])
            z_coord = int(key%layout_size["width"])

            index_in_extended_layout = (layout_size["height"] + x_coord) * \
                                       layout_size["width"] + z_coord
            extended_qubit_layout[index_in_extended_layout] = value

    return {v: int(k) for k, v in extended_qubit_layout.items()}
    