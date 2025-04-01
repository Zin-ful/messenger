import random
import re
int_to_char = {
                1: "a",
                2: "b",
                3: "c",
                4: "d",
                5: "e",
                6: "f",
                7: "g",
                8: "h",
                9: "i",
                10: "j",
                11: "k",
                12: "l",
                13: "m",
                14: "n",
                15: "o",
                16: "p",
                17: "q",
                18: "r",
                19: "s",
                20: "t",
                21: "u",
                22: "v",
                23: "w",
                24: "x",
                25: "y",
                26: "z",
                27: "a",
                28: "a",
                29: "A",
                30: "B",
                31: "C",
                32: "D",
                33: "E",
                34: "F",
                35: "G",
                36: "H",
                37: "I",
                38: "J",
                39: "K",
                40: "L",
                41: "M",
                42: "N",
                43: "O",
                44: "P",
                45: "Q",
                46: "R",
                47: "S",
                48: "T",
                49: "U",
                50: "V",
                51: "W",
                52: "X",
                53: "Y",
                54: "Z",
                55: "@",
                56: "%",
                57: "*",
                58: ")",
                59: ":",
                60: "|"

}

def test(inp):
    print(len(inp))
    print(len(list(inp)))

def enc(inp):
    hash = random.randint(5, 20)
    char_list = ["="]
    inp = list(inp)
    pos = 0
    
    for char in range(len(inp)):
        pos += 2
        index = random.randint(1, 60)
        char_list.append(str(index) + ":")
        print(pos, int_to_char.get(index))
        inp.insert(pos, int_to_char.get(index))
    res = ''.join(inp)
    inp_len = str(len(inp))
    return res + ''.join(char_list) + f"-{hash}" + f"+{inp_len}"

def dec(inp):
    pos = 0
    char_list = []
    inp, char_pos = inp.split("=")
    char_pos, hash = char_pos.split("-")
    hash, char_len = hash.split("+")
    hash = int(hash)
    char_pos = re.split(f"(?<!:):(?!:)", char_pos)

    char_pos.pop(len(char_list) - 1)

    inp = list(inp)

    for char in range(len(inp)):
        pos += 2
        if pos <= len(inp):
            print(pos, inp[pos])
            del inp[pos]
    return ''.join(inp)

msg = enc("man i love men")
print(msg)
print(dec(msg))
