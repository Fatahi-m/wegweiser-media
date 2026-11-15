import sys, subprocess
src, od = sys.argv[1], sys.argv[2]
L = [("WG",0,5.34),("WORDS",5.34,13.06),("SENT",13.06,21.04),("Q0",21.04,26.04),("Q1",26.04,29.92),("Q2",29.92,34.76),
     ("Q3",34.76,39.52),("Q4",39.52,41.57),("Q5",41.57,43.46),("Q6",43.46,49.37)]
for n,a,b in L:
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(a),"-i",src,"-t",str(round(b-a,3)),"-vn","-ac","1","-ar","44100",f"{od}/{n}.wav"],check=True)
print("ok")
