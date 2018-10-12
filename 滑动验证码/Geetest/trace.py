import random


def get_trace_fast(distance):
    track = [[random.randint(19, 30), random.randint(20, 25), 0]]
    rand_x = int(distance * random.randint(5, 8) / 10)
    track.append([rand_x, random.randint(-2, 2), random.randint(300, 500)])
    track.append([distance - rand_x, random.randint(-2, 2), random.randint(300, 500)])
    track.append([0, 0, random.randint(300, 400)])
    return track


def get_trace_normal(distance):
    track = [[random.randint(19, 30), random.randint(20, 25), 0]]
    count = 0
    scale = [0.2, 0.5, random.randint(6, 8) / 10]
    while count < distance:
        if count < distance * scale[0]:
            x = random.randint(1, 2)
        elif count < distance * scale[1]:
            x = random.randint(3, 4)
        elif count < distance * scale[2]:
            x = random.randint(5, 6)
        elif count < distance * 0.9:
            x = random.randint(2, 3)
        elif count < distance:
            x = 1
        count += x
        track.append([
            x,
            random.choice([0, 0, 0, 0, 0, 0, -1, 1]),
            random.randint(10, 20)
        ])

    track.append([0, 0, random.randint(300, 400)])
    return track

