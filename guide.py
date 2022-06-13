import os


def activate_dij(start, end, mode):
    cmd = "./graph.sh"

    with open("./input2c.txt", "w", encoding="utf-8") as f:
        f.write(start + "\n")
        f.write(end + "\n")
        f.write(mode)
    data = os.popen(cmd)
    print(data.read())


def read_meta_file():
    with open("./input2py.txt", "r", encoding="utf-8") as f:
        distance = f.readline()
        paths = f.readlines()
        for i in range(len(paths)):
            path = paths[i].split("\n")[0]
            paths[i] = path
        print(distance)
        print(paths)
    return distance, paths


if __name__ == "__main__":
    activate_dij("西土城运动场", "南区食堂", "1")
    read_meta_file()
