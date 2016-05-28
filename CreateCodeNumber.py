import sys  

def Main(argv):
    assert len(argv) == 2 and argv[1].islower()
    input = argv[1]
    output = ""
    for i in range(0, 3):
        output = output + format(ord(input[i]), "02x")

    output = list(output)
    output[1], output[2] = output[2], output[1]
    output = "".join(output)
    print(input + "." + input[0].capitalize() + output)
    
if __name__ == '__main__':
    sys.exit(Main(sys.argv));