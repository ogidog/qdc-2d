import sys

template = {}


def read_template_file(file):
    def switch(line):
        match line:
            case 'SYNTHETIC':
                template["SYNTHETIC"] = float(line[1])
            case 'STEP':
                template['STEP'] = line[1]
            case 'METHOD':
                template['METHOD'] = line[1]
            case _:
                return 0

    f = open(template_file)

    while True:
        line = f.readline()
        if line == "":
            f.close()
            break
        switch(line.split(";"))


def main(template_file="TEMPLATE.txt"):
    read_template_file(template_file)
    print()


if __name__ == "__main__":
    [template_file] = sys.argv[1:]

    main(template_file)
