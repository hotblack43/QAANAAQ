#!/usr/bin/env python3

import os
from datetime import datetime

def prompt_for_input(prompt):
    return input(prompt + ": ")

def generate_man_page():
    name = prompt_for_input("Program Name")
    brief_description = prompt_for_input("Brief Description")
    synopsis = prompt_for_input("Synopsis")
    description = prompt_for_input("Detailed Description")
    options = []
    while True:
        option = prompt_for_input("Option (leave empty to finish)")
        if not option:
            break
        option_description = prompt_for_input("Option Description")
        options.append((option, option_description))
    examples = []
    while True:
        example = prompt_for_input("Example (leave empty to finish)")
        if not example:
            break
        example_description = prompt_for_input("Example Description")
        examples.append((example, example_description))
    author = prompt_for_input("Author")
    see_also = prompt_for_input("See Also")

    current_date = datetime.now().strftime("%Y-%m-%d")

    man_page = f"""
.TH {name} 1 "{current_date}" "1.0" "{name} Manual"
.SH NAME
{name} \- {brief_description}
.SH SYNOPSIS
.B {name}
{synopsis}
.SH DESCRIPTION
{description}
.SH OPTIONS
"""

    for option, option_description in options:
        man_page += f"""
.TP
.B {option}
{option_description}
"""

    man_page += """
.SH EXAMPLES
"""
    for example, example_description in examples:
        man_page += f"""
.TP
.B {example}
{example_description}
"""

    man_page += f"""
.SH AUTHOR
{author}
.SH SEE ALSO
{see_also}
"""

    return man_page

def save_man_page(man_page, output_file):
    with open(output_file, 'w') as f:
        f.write(man_page.strip())
    print(f"Man page written to {output_file}")

def move_man_page(output_file):
    os.system(f"sudo mv {output_file} /usr/local/share/man/man1/")
    print(f"Man page moved to /usr/local/share/man/man1/{output_file}")

def update_man_database():
    os.system("sudo mandb")
    print("Man database updated.")

if __name__ == "__main__":
    man_page = generate_man_page()
    output_file = prompt_for_input("Output file name (without extension)") + ".1"
    save_man_page(man_page, output_file)
    move_man_page(output_file)
    update_man_database()

