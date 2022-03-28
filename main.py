import sys

template = {}


def read_template_file(file):
    def switch(line):
        if line[0] == 'SYNTHETIC':
            template["SYNTHETIC"] = float(str.strip(line[1]))
        if line[0] == 'STEP':
            template['STEP'] = int(str.strip(line[1]))
        if line[0] == 'METHOD':
            template['METHOD'] = str.strip(line[1])
        if line[0] == 'INPUT':
            template['INPUT'] = str.strip(line[1])
        if line[0] ==  'OUTPUT':
            template['OUTPUT'] = str.strip(line[1])

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
