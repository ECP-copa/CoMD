# -*- coding: utf-8 -*-

import argparse

def parse_arguments():
    arg_parser = argparse.ArgumentParser(
            description = "Specify CoMD output file and file to be written to")
    arg_parser.add_argument(
            "comd_output",
            type = str,
            help = "CoMD output file")
    arg_parser.add_argument(
            "timing",
            type = str,
            default = "timing_output.dat",
            help = "Timing file to write to")
    args = vars(arg_parser.parse_args())
    return args

if __name__ == "__main__":
    args = parse_arguments()
    in_file = args["comd_output"]
    out_file = args["timing"]

    with open(in_file) as f:
        lines = f.read().splitlines()
    
    timing_lines = []

    valid = False

    for line in lines:
        if not valid:
            if "Timings for Rank 0" in line:
                timing_lines.append("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n")
                timing_lines.append("┃ " + line.ljust(78) + "┃\n")
                valid = True
        else:
            timing_lines.append("┃ " + line.ljust(78) + "┃\n")
            if "commReduce" in line and ":" in line:
                valid = False
                timing_lines.append("┗ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n")
    
    with open(out_file,"w") as f:
        for line in timing_lines:
            f.write(line)
