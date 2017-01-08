#!/usr/bin/env python
# coding=utf-8

# clean raw output from pdftotext
#
# Copyright (C) 2017, Alberto Pettarin (www.albertopettarin.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Clean the raw output of pdftotext over the NVdB PDF and
output the full contents of the NVdB dictionary, or just the (unique) words.
"""

import io
import os
import re
import sys

__author__ = "Alberto Pettarin"
__email__ = "alberto@albertopettarin.it"
__copyright__ = "Copyright 2017, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "GNU AGPL 3"
__status__ = "Production"
__version__ = "1.0.0"


GRAMMAR = [
    u"agg.",
    u"agg.compar.inv.",
    u"agg.dimostr.",
    u"agg.escl.",
    u"agg.indef.",
    u"agg.indef.inv.",
    u"agg.interr.",
    u"agg.inv.",
    u"agg.num.pl.",
    u"agg.poss. di terza pers.pl.",
    u"agg.rel.",
    u"art.indet.m.sing.",
    u"avv.",
    u"cong.",
    u"inter.",
    u"lat.",
    u"loc. di comando.",
    u"prep.",
    u"pron. dimostr.m.",
    u"pron. poss. di prima pers.sing.",
    u"pron.dimostr.",
    u"pron.dimostr.m.",
    u"pron.escl.",
    u"pron.indef.",
    u"pron.indef.inv.",
    u"pron.indef.m.",
    u"pron.interr.",
    u"pron.pers. di terza pers.f.pl.",
    u"pron.pers. di terza pers.f.sing.",
    u"pron.poss. di terza pers.sing.",
    u"pron.pers. di terza pers.m.sing.",
    u"pron.poss. di prima pers.pl.",
    u"pron.poss. di prima pers.sing.",
    u"pron.poss. di seconda pers.pl.",
    u"pron.poss. di seconda pers.sing.",
    u"pron.poss. di terza pers.pl.",
    u"pron.poss. di terza pers.sing.",
    u"pron.rel.",
    u"pron.rel.indef.",
    u"s.f. e m.",
    u"s.f. pl.",
    u"s.f.",
    u"s.f.inv.",
    u"s.f.pl.",
    u"s.m. e f.",
    u"s.m. e f.inv.",
    u"s.m.",
    u"s.m.inv.",
    u"s.m.pl.",
    u"simb.",
    u"v.intr.",
    u"v.tr.",
]


def usage():
    """ Print usage. """
    print(u"")
    print(u"$ python %s raw.txt clean.txt [-s|--split|--split-justify|-w|--words-only]" % sys.argv[0])
    print(u"")


def repl(match):
    """ Replace a match with the first group captured. """
    return match.group(1)


def swap(lines, letters):
    """
    Swap the line containing the given letter
    (as letter headings) with the one preceeding it.
    For example, the raw text has:

        hamburger s.m.inv., ...
        H

    but it should have been:

        H
        hamburger s.m.inv., ...

    """
    for letter in letters:
        idx = lines.index(letter)
        tmp = lines[idx]
        lines[idx] = lines[idx - 1]
        lines[idx - 1] = tmp
    return lines


def main():
    """ Entry point """

    # input and output file paths are required
    if len(sys.argv) < 3:
        usage()
        sys.exit(2)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    # options
    words_only = (u"-w" in sys.argv) or (u"--words-only" in sys.argv)
    split = (u"-s" in sys.argv) or (u"--split" in sys.argv) or (u"--split-justify" in sys.argv)
    split_justify = u"--split-justify" in sys.argv

    # read input file
    with io.open(input_file_path, "r", encoding="utf-8") as input_file:
        raw = input_file.read()

    # remove spurious character
    clean = raw.replace(u"", u"\n")

    # split into lines
    lines = clean.split(u"\n")

    # skip first 8
    lines = lines[8:]

    # skip empty lines
    lines = [l.strip() for l in lines]
    lines = [l for l in lines if len(l) > 0]

    # skip lines with header
    lines = [l for l in lines if not l.startswith(u"23 novembre 2016")]

    # skip lines containing only the page number
    lines = [l for l in lines if re.match(r"^[0-9]+$", l) is None]

    # swap lines with the following letters
    lines = swap(lines, [u"H", u"J", u"W", u"Y"])

    # replace lines containing only one letter with , to help joining later
    lines = [l if len(l) > 1 else u"," for l in lines]

    # join lines if one contains the line break u"-"
    accumulator = []
    accumulator.append(lines[0])
    for i in range(1, len(lines)):
        if accumulator[-1].endswith(u"-"):
            accumulator[-1] = accumulator[-1][:-1] + lines[i]
        else:
            accumulator.append(lines[i])

    # join everything together
    accumulator = u" ".join(accumulator)

    # remove numbers if they occur before a letter
    accumulator = re.sub(r"[0-9]([a-z])", repl, accumulator)

    # remove double spaces
    accumulator = re.sub(r" [ ]*", u" ", accumulator)

    # tweak a bit to simplify splitting later
    accumulator = accumulator[2:] + u","
    accumulator = re.sub(r", ,", u",", accumulator)
    accumulator = re.sub(r"\. ,", u".,", accumulator)
    accumulator = re.sub(r" comando,", u" comando.,", accumulator)
    accumulator = re.sub(r" s.m,", u" s.m.,", accumulator)
    accumulator = re.sub(r" sigla,", u" sigla.,", accumulator)
    accumulator = re.sub(r" agg. inv.", u" agg.inv.", accumulator)
    accumulator = re.sub(r" pron. indef.", u" pron.indef.", accumulator)
    accumulator = re.sub(r" pron. interr.", u" pron.interr.", accumulator)

    # split again
    words = (re.sub(r"\.,", u".,|||", accumulator)).split(u"|||")
    words = [w.strip() for w in words if len(w.strip()) > 0]

    # join words if one does not contain a space
    accumulator = []
    accumulator.append(words[0])
    for i in range(1, len(words)):
        if words[i][:-1] in GRAMMAR:
            accumulator[-1] += (u" %s" % words[i])
        else:
            accumulator.append(words[i])

    if split:
        # split word from the grammar
        accumulator = [a.split(u" ") for a in accumulator]
        accumulator = [(a[0], u" ".join(a[1:])) for a in accumulator]
        if split_justify:
            # left justify, padded words
            max_length = max([len(a[0]) for a in accumulator])
            accumulator = [u"%s %s" % (a.ljust(max_length), b) for a, b in accumulator]
        else:
            # just use a tab character
            accumulator = [u"%s\t%s" % (a, b) for a, b in accumulator]
    elif words_only:
        # keep only word
        accumulator = [a.split(u" ")[0] for a in accumulator]
        # NOTE: doing:
        #       accumulator = sorted(set(accumulator))
        #       would put "Ferragosto" and "TG" before "a",
        #       and we do not want it, so we do the uniq()
        #       "naively" as follows
        unique = []
        unique.append(accumulator[0])
        for a in accumulator[1:]:
            if a != unique[-1]:
                unique.append(a)
        accumulator = unique

    print(u"[INFO] Generated %d lemmas" % len(accumulator))

    out = u"\n".join(accumulator)
    if not words_only:
        # restore tweaked stuff as in the raw text
        out = out.replace(u"sigla.", u"sigla")
        out = out.replace(u"loc. di comando.", u"loc. di comando")
        out = out.replace(u",\n", u"\n")
        out = out[:-1]

    # write output file
    with io.open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(out)

    print(u"[INFO] File '%s' written" % output_file_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
