import math
import random
def getTrack(intX):
    t1 = intX*(10+random.randint(2,7))
    t0 = 0
    superrate = 0
    g = lambda t:math.tanh(1.5*(t-t0)/(t1-t0))
    track_raw = []
    for t in range(t1):
        track_raw.append(int(intX/g(t1)*g(t)))

    index = 0
    track = [[random.randint(77,86),random.randint(270,290),random.randint(50,120)]]

    while index < len(track_raw):
        show = track_raw[index + min(200,len(track_raw) - index - 1)] - track_raw[index]
        #print(len(track_raw)-index)
        index += 200
        if random.randint(1,20) == 20:
            superrate = random.randint(100,300)
        else:
            superrate = 0
        track.append([show,random.randint(-1,1) + random.randint(-1,1),random.randint(15,20) + superrate])

    for i in range(5):
        track.append([random.randint(-2, 2), 0, random.randint(10, 30)])

    #print(track)
    return track

if __name__ == "__main__":
    print(getTrack(int(504)))