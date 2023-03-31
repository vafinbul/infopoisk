import os
from typing import List

index = dict()
total_count_of_pages = set(i for i in range(1, len(os.listdir('../1/output/'))))
i_expression = input('Введите булево выражение ')
operations = {'|', '!', '&'}


def parse_index():
    with open('./index.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if len(line) == 0:
                continue

            splitted_line = line.split(":")
            index[splitted_line[0]] = set(map(int, splitted_line[1].split()))


def parse_intersection_bul(expression: List):
    for i, part in enumerate(expression):
        if part != '&':
            continue

        left_operand_index = i - 1
        right_operand_index = i + 1

        temp_express = expression
        if len(temp_express[:left_operand_index]) > 0:
            expression = temp_express[:left_operand_index]
        else:
            expression = list()

        if len(temp_express[left_operand_index] & temp_express[right_operand_index]) > 0:
            expression.append(temp_express[left_operand_index] & temp_express[right_operand_index])
        else:
            expression.append(set())

        if len(temp_express[right_operand_index + 1:]) > 0:
            expression += temp_express[right_operand_index + 1:]

        return parse_intersection_bul(expression)

    return expression


def parse_union_bul(expression: List):
    for i, part in enumerate(expression):
        if part != '|':
            continue

        left_operand_index = i - 1
        right_operand_index = i + 1

        temp_express = expression
        if len(temp_express[:left_operand_index]) > 0:
            expression = temp_express[:left_operand_index]
        else:
            expression = list()

        expression.append(temp_express[left_operand_index] | temp_express[right_operand_index])

        if len(temp_express[right_operand_index + 1:]) > 0:
            expression += temp_express[right_operand_index + 1:]

        return parse_union_bul(expression)

    return expression


def main(expression: str):
    parse_index()
    expression_parts = expression.split()

    temp_expression = list()
    for part in expression_parts:
        if part not in operations:
            try:
                if not part.startswith('!'):
                    temp_expression.append(index[part])
                else:
                    try:
                        temp_expression.append(total_count_of_pages - index[part[1:]])
                    except:
                        temp_expression.append(total_count_of_pages)
            except:
                temp_expression.append(set())
                print('Слова', part, 'нет в индексе')
        else:
            temp_expression.append(part)

    temp_expression = parse_intersection_bul(temp_expression)
    temp_expression = parse_union_bul(temp_expression)

    return temp_expression[0]


result = main(i_expression)
if len(result) > 0:
    print(*sorted([int(i) for i in result]))
else:
    print("Ничего не найдено")

# стартовый & мост | секция
# стартовый & !мост | !секция
# стартовый | мост | секция
# стартовый | !мост | !секция