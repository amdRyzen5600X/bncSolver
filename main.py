from random import shuffle
from itertools import cycle, islice
from pyrogram import Client, filters
from time import sleep

import CONFIG

app = Client("my_account", api_id=CONFIG.API_ID, api_hash=CONFIG.API_HASH)


def swap_element_string(string: str, i: int, j: int) -> str:
    tempo = list(string)
    tempo[i], tempo[j] = tempo[j], tempo[i]
    return ''.join(tempo)


def remove_character(bulls: int, string: str, i: int, possible_positions: list) -> None:
    string1 = string * 2
    if bulls == 0:
        for x in range(16):
            possible_positions[x] = possible_positions[x].replace(string1[i + x], '')


def generate_random_variant(string: str) -> str:
    list_of_string = []
    shuffled_string = ''
    for i in string:
        list_of_string.append(i)
    shuffle(list_of_string)
    for i in list_of_string:
        shuffled_string = f'{shuffled_string}{i}'
    return shuffled_string


def generate_first_variants(string: str) -> list:
    possible_variants = []
    for x in range(16):
        alphabet = cycle(string)
        temp = ''
        for i in islice(alphabet, x, x + 16):
            temp = f'{temp}{i}'
        possible_variants.append(temp)
    return possible_variants


def calculate_variants(impossible_variants: list, index: int, symbol: str, possible_positions: list) -> str:
    for impossible_variant in impossible_variants:
        symbol1 = impossible_variant[index]
        find = impossible_variant.find(symbol)
        jndex = find
        if not (symbol1 in possible_positions[jndex]):
            return swap_element_string(impossible_variant, index, jndex)


def add_answer(bulls: int, answer: str, answers: dict) -> None:
    answers[bulls].append(answer)


# noinspection PyGlobalUndefined
@app.on_message(filters.bot & filters.chat(-1001720756304))
def get_bulls(_, msg) -> None:
    global Gbulls
    Gbulls = int(msg.text[18])


@app.on_message(filters.command('strt', prefixes='/') & filters.me)
def main(_, msg):
    app.send_message(msg.chat.id, '/bnc hex 16')
    final_answer = ''
    i = 0
    answers = {}
    for x in range(16):
        answers[x] = []
    string = '0123456789abcdef'
    possible_positions = []
    for x in range(16):
        possible_positions.append(string)
    while i < 16:
        variant = generate_first_variants(string)[i]
        app.send_message(msg.chat.id, variant)
        sleep(5)
        bulls = Gbulls
        remove_character(bulls, string, i, possible_positions)
        add_answer(bulls, variant, answers)
        i += 1
    # for x in possible_positions:
    #     print(x)
    for x in range(5):
        random_variant = generate_random_variant(string)
        app.send_message(msg.chat.id, random_variant)
        sleep(5)
        bulls = Gbulls
        remove_character(bulls, random_variant, 0, possible_positions)
        add_answer(bulls, random_variant, answers)
    for index, position in enumerate(possible_positions):
        for symbol in position:
            if symbol == position[len(position) - 1]:
                final_answer = final_answer.join(symbol)
                remove_string = symbol * 16
                remove_character(0, remove_string, 0, possible_positions)
                possible_positions[index] = symbol
                break

            calculated_variant = calculate_variants(answers[0], index, symbol, possible_positions)
            app.send_message(msg.chat.id, calculated_variant)
            sleep(5)
            bulls = Gbulls
            add_answer(bulls, calculated_variant, answers)
            if bulls == 1:
                final_answer = final_answer.join(calculated_variant[index])
                remove_string = calculated_variant[index] * 16
                remove_character(0, remove_string, 0, possible_positions)
                possible_positions[index] = calculated_variant[index]
                break
            remove_character(bulls, calculated_variant, 0, possible_positions)

        for answer in answers[1]:
            if answer[index] == possible_positions[index]:
                remove_character(0, answer, 0, possible_positions)
                possible_positions[index] = answer[index]

        for answer in answers[2]:
            for i in range(index):
                if (answer[i] == possible_positions[i]) and (answer[index] == possible_positions[index]):
                    remove_character(0, answer, 0, possible_positions)
                    possible_positions[i] = answer[i]
                    possible_positions[index] = answer[index]

        for ind, pos in enumerate(possible_positions):
            if len(pos) == 1:
                remove_character(0, pos * 16, 0, possible_positions)
                possible_positions[ind] = pos

        file = open('possible_positions.txt', 'w')
        file.write('')
        file.close()
        file = open('possible_positions.txt', 'a')
        for f in possible_positions:
            file.write(f'{f}\n')
        file.write(final_answer)
        file.close()

    print(''.join(possible_positions))


if __name__ == '__main__':
    app.run()
