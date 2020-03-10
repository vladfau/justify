#!/usr/bin/env python3
"""
    jusitfy.py

    Program to justify the given text to some width (left and right)

    Usage: jusitfy.py <width> <'file'|'stdin'> <path to file|text>
    Output: stdin - the resulting text, stderr - all other debug information

    Example: ./jusitfy.py 8 stdin "hi this is me vlad"
    >> ./jusitfy.py 8 stdin "hi! this is me vlad" 2>/dev/null
    hi! this
    is    me
    vlad

    Example: ./jusitfy.py 20 file file 2>/dev/null
    >> ./jusitfy.py 20 file file 2>/dev/null
    This  is  a   sample
    text      but      a
    complicated  problem
    to be solved, so  we
    are adding more text
    to   see   that   it
    actually      works.

    Example: ./jusitfy.py 5 stdin "unconsumable text"
    Init done.
    Width: 5
    From file: False
    From: stdin
    Contents:
    unconsumable text
    There is/are one or more word(s) longer than width. Unable to justify
"""

from typing import List, Tuple, Union, Iterator
import sys
import re
from math import floor
from pathlib import Path


def build_line_list(words: List[Tuple[str, int]], width: int) -> List[Union[List[Tuple[str, int]], int, int]]:
    """
    build_line_list tries to build a list of lines, each containing only the words, which fit within the
    single line for a given width.

    :param words: list of tuples, where each tuple is (string, int) - the word and its length
    :width int: expected width of the paragraph
    :return: the list, each element is a union of selected words (list of tuples (str, int)),
             number of symbols in line, including at least one space between words
             number of words in the line
    """
    line_list = []
    # accumulator for line list candidate
    acc = [[], 0, 0]
    # try to assemble words into lines
    for word, wc in words:
        # first word case (as we must not add spaces for cases if only one word fits the line)
        if acc[1] == 0:
            acc[0].append((word, wc))
            acc[1] += wc
            acc[2] = 1
        # if we can fit the word and at least one preceding space for it, append to buffer
        # append word length to buffer, increase buffer's word count by one
        elif acc[1] + wc + 1 <= width:
            acc[0].append((word, wc))
            acc[1] += wc + 1
            acc[2] += 1
        # otherwise, cleanup the buffer (acc) and store the buffered data in the next line
        else:
            line_list.append(acc)
            acc = [[(word, wc)], wc, 1]

    # not forgetting about the very last line
    line_list.append(acc)
    return line_list

def build_justified_line(line_items: Tuple[str, int], width: int, line_length=-1, word_count=-1) -> str:
    """
    build_justified_line creates a line with expected padding between words. As space factor (optimum number of spaces)
    is calculated as floored-value, this method will try to stick as many space fragments of equal length between
    all the words, leaving the last space fragment all the unallocated spaces symbols (see build_justified_list)

    :param line_items: list of words (tuple (str, int) - word and its length)
    :param width: expected width of the paragraph
    :param line_length: length of all the line_items. if not passed, will be calculated from line_items
    :param word_count: number of words in line_items. if not passed, will be calculated from line_items
    :return: returns the justified to the width string
    """
    if word_count == -1:
        word_count = len(line_items)
    if line_length == -1:
        # all the symbols in all the words + number of spaces between them
        line_length = sum([cc for _,cc in line_items]) + word_count - 1

    resulting_line = ""
    # here is the justification calculation method
    # take all the spaces in the line (wordcount - 1)
    spaces = word_count - 1
    # calculate non-space symbol consumption and deduct it from expected width
    available = width - (line_length - spaces)

    # then we calculate ratio - how many spaces can we fit in the rest of available slots in width
    # note that "available" contains ONLY non-space symbols for the line
    ratio = available/spaces if spaces else 1

    # debug output
    sys.stderr.write('wc = {}, wlen = {}, spaces = {}, available = {}, ratio = {}\n'.format(word_count,
                                                                                            line_length,
                                                                                            spaces,
                                                                                            available, ratio))

    # ratio gives some sort of float number, e.g. 1.3 or 2.6, which basically means
    # that we should put the floored (or the integer part) number of spaces to between all the words except
    # for the last one. The last space will contain (basing on the provided example) as many spaces as it can
    # so, for the given example "This is a sample" string with width=20 gives ratio of 2.3, which means
    # that the string shall be justified as 2,2,3
    space_factor = floor(ratio)

    i = 0
    current_count = 0
    # put each element, except for the last to the resulting line, appending the required number of spaces
    while i < len(line_items) - 1:
        resulting_line += line_items[i][0] + space_factor * ' '
        current_count += line_items[i][1] + space_factor # counting all the symbols already put for the last spaces
        i += 1

    # for the last one, we shall calculate rest of the vacant spaces and just fill them.
    last_spaces = width - current_count - line_items[i][1] if spaces else 0
    resulting_line += (last_spaces * ' ' + line_items[i][0])
    return resulting_line

def build_justified_list(line_list: List[Union[List[Tuple[str, int]], int, int]], width: int) -> Iterator[str]:
    """
    Generator to build the list of justified strings, basing on expected width

    :param line_list: the list, each element is a union of selected words (list of tuples (str, int)),
             number of symbols in line, including at least one space between words,
             number of words in the line
    :width int: expected width of the paragraph
    :return: Iterator (yields) to justified line
    """
    for line_items, wlen, wc in line_list:
        yield build_justified_line(line_items, width, wlen, wc)

def justify(paragraph: str, width: int, delimiters=" |\n|\t") -> List[str]:
    """
    Justify given text according to width. The method splits the incoming string by delimiters
    defaulting to space and the newline character, then justifies each line.

    Method checks for empty inputs and incompatible lines (where a single word is longer than width)

    :param paragraph: string of text to justify
    :width int: expected width of the paragraph
    :delimites str: regular expression to re.split() the paragraph by. Defaults to " |\n|\t"
    :returns: list of justified strings
    """
    # splitting into tuples of words and their length, taking only non-zero substrings
    words = [(x, len(x)) for x in re.split(delimiters, paragraph) if len(x)]

    if not len(words):
        sys.stderr.write("No words were found in the input string\n")
        print("\n")
        sys.exit(5)

    # check for illegally long words
    if len([wc for _,wc in words if wc > width]):
        sys.stderr.write("There is/are one or more word(s) longer than width. Unable to justify\n")
        sys.exit(6)

    # first, extract words and fit them into lines using build_line_list, then justify it by width
    # using build_justified_list
    return [x for x in build_justified_list(build_line_list(words, width), width)]

def main():
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: ./jusitfy.py <width> <'file'|'stdin'> <path to file|string>\n")
        sys.exit(1)

    if not sys.argv[1].isnumeric() or int(sys.argv[1]) <= 0:
        sys.stderr.write("<width> must be positive integer\n")
        sys.exit(2)
    width = int(sys.argv[1])

    is_file_input = sys.argv[2] == "file"
    if sys.argv[2] not in ["file", "stdin"]:
        sys.stderr.write("Must pass \"file\" or \"stdin\" as location for the consumed text\n")
        sys.exit(3)

    path = sys.argv[3]
    if is_file_input:
        p = Path(path)
        if not p.exists():
            sys.stderr.write("Path: {} does not exist\n".format(path))
            sys.exit(4)
        input_data = p.read_text()
    else:
        input_data = path

    init_msg = "Init done.\nWidth: {}\nFrom file: {}\nFrom: {}\nContents:\n{}\n"
    sys.stderr.write(init_msg.format(width, is_file_input, path if is_file_input else "stdin", input_data))

    print('\n'.join(justify(input_data, width)))
    # adding basically for the testability
    sys.exit(0)

if __name__ == "__main__":
    main()
