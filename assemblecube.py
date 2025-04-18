def get_face(face):
    # Get the face side of the cube from the given face color
    face_side = {
        "Y": "U",
        "G": "F",
        "R": "L",
        "W": "D",
        "O": "R",
        "B": "B"
    }.get(face, None)
    return face_side

def update_face_mapping(face_dict, face_char, face_string):
    """
    Aggiorna il dizionario associando la stringa alla chiave corrispondente al carattere.

    Args:
        face_dict (dict): Dizionario con chiavi tra 'U', 'F', 'L', 'D', 'R', 'B'.
        face_char (str): Un carattere tra 'U', 'F', 'L', 'D', 'R', 'B'.
        face_string (str): La stringa da associare alla chiave.

    Returns:
        dict: Il dizionario aggiornato.
    """
    if face_char in face_dict:
        face_dict[face_char] = face_string
    else:
        raise ValueError(f"Il carattere '{face_char}' non è una chiave valida. Usa solo 'U', 'F', 'L', 'D', 'R', 'B'.")
    
    return face_dict

def assemble_solver_string(cube_config):
    """
    Assembla una stringa di risoluzione del cubo a partire da un dizionario di configurazione.

    Args:
        cube_config (dict): Dizionario con le facce del cubo e i loro colori.

    Returns:
        str: Stringa di risoluzione del cubo.
    """

    solver_string = ""
    for face in ['U', 'R', 'F', 'D', 'L', 'B']:
        if cube_config[face] is not None:
            current_face = cube_config[face]
            for i in range(9):
                current_face[i] = get_face(current_face[i])
            # Converti la lista in una stringa prima di concatenarla
            solver_string += ''.join(current_face)
    
    return solver_string

def assemble_animcube_string(cube_config):
    visual_indices = [
        # U
        6, 7, 8, 3, 4, 5, 0, 1, 2,
        # D
        9, 12, 15, 10, 13, 16, 11, 14, 17,
        # F
        18, 21, 24, 19, 22, 25, 20, 23, 26,
        # B
        27, 30, 33, 28, 31, 34, 29, 32, 35,
        # L
        38, 37, 36, 41, 40, 39, 44, 43, 42,
        # R
        45, 48, 51, 46, 49, 52, 47, 50, 53
    ]
    
    animcube_string_list = [''] * 54  # 6 facce * 9 sticker ciascuna
    i = 0
    for face in ['U', 'D', 'F', 'B', 'L', 'R']:
        if cube_config[face] is not None:
            current_face = cube_config[face]
            for j in range(9):
                animcube_string_list[visual_indices[i]] = current_face[j]
                i += 1

    return ''.join(animcube_string_list)