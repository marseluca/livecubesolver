import re


content = 'var config = "bgcolor=ffffff"; config+="&movetext=1"; '

# Convert moves from solver format to AnimCubeJS format
def convert_moves(input_string):
    # Rimuove i suffissi tipo (1f), (10f), ecc.
    cleaned = re.sub(r'\(\d+f\)', '', input_string)

    # Suddivide la stringa in singole mosse (assumiamo separate da spazi)
    moves = cleaned.strip().split()

    # Converte le mosse R3 -> R', ecc.
    converted_moves = []
    for move in moves:
        if len(move) == 2 and move[1] == '3':
            converted_moves.append(move[0] + "'")
        elif len(move) == 2 and move[1] == '2':
            converted_moves.append(move[0] + '2')
        elif len(move) == 2 and move[1] == '1':
            converted_moves.append(move[0])  # R1 -> R
        else:
            converted_moves.append(move)  # lascia tutto il resto com'è

    return ' '.join(converted_moves)


def update_animcube_config(config_content,solution_content):

    config_content = 'config+="&facelets=' + config_content + '"; config+="&move=' + solution_content + '";'
    with open("config.js", "w") as file:
        file.write(content+config_content)