import sys, subprocess, json
src, od = sys.argv[1], sys.argv[2]
W = [("P1",0,7.24),("G1",7.24,8.65),("P2",8.65,21.24),("G2",21.24,22.83),("P3",22.83,35.77),("G3",35.77,37.27),
     ("P4",37.27,43.15),("G4",43.15,44.58),("P5",44.58,75.03)]
T = [("Pa",75.03,76.60),("Ga",76.60,78.03),("Pb",78.03,83.60),("Gb",83.60,85.19),("Pc",85.19,90.61)]
for name,a,b in W+T:
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(a),"-i",src,"-t",str(round(b-a,3)),"-vn","-ac","1","-ar","44100",f"{od}/{name}.wav"],check=True)
json.dump({"P":[f"{od}/P{i}.wav" for i in range(1,6)],"G":[f"{od}/G{i}.wav" for i in range(1,5)]},open(f"{od}/w.json","w"))
json.dump({"P":[f"{od}/P{x}.wav" for x in "abc"],"G":[f"{od}/G{x}.wav" for x in "ab"]},open(f"{od}/t.json","w"))
print("ok")
