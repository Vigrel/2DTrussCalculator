from Class.Structure import Structure
import funcoesTermosol as funcoesTermosol
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requiredArgs = parser.add_argument_group("required arguments")
    requiredArgs.add_argument("-i", "--input", required=True)
    args = parser.parse_args()

    structure = Structure(args.input)
    funcoesTermosol.geraSaida(
        "saida.txt",
        structure.support_reactions,
        structure.displacement,
        structure.deformation,
        structure.internal_forces,
        structure.tensile_forces,
    )
