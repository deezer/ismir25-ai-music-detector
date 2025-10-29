import pandas as pd

split = pd.read_csv('sonics/fake_songs.csv', low_memory=False)

s_train = split[split["split"]=="train"][["id", "source"]].to_numpy()
s_test = split[split["split"]=="test"][["id", "source"]].to_numpy()
s_valid = split[split["split"]=="valid"][["id", "source"]].to_numpy()

s_3_5 = split[split["algorithm"]=="chirp-v3.5"]["id"].to_numpy()
s_3 = split[split["algorithm"]=="chirp-v3"]["id"].to_numpy()
s_2 = split[split["algorithm"]=="chirp-v2-xxl-alpha"]["id"].to_numpy()
u_120 = split[split["algorithm"]=="udio-120s"]["id"].to_numpy()
u_30 = split[split["algorithm"]=="udio-30s"]["id"].to_numpy()

vsplit = {
    "suno_v3.5": [],
    "suno_v3": [],
    "suno_v2": [],
    "udio_v120": [],
    "udio_v30": [],
    "train": [],
    "test": [],
    "valid": [],
 }

for k, v in s_train:
    vsplit["train"].append( "fake_{:05d}_{}_0.mp3".format(k, v) )
    vsplit["train"].append( "fake_{:05d}_{}_1.mp3".format(k, v) )
for k, v in s_test:
    vsplit["test"].append( "fake_{:05d}_{}_0.mp3".format(k, v) )
    vsplit["test"].append( "fake_{:05d}_{}_1.mp3".format(k, v) )
for k, v in s_valid:
    vsplit["valid"].append( "fake_{:05d}_{}_0.mp3".format(k, v) )
    vsplit["valid"].append( "fake_{:05d}_{}_1.mp3".format(k, v) )

for k in s_3_5:
    vsplit["suno_v3.5"].append( "fake_{:05d}_suno_0.mp3".format(k) )
    vsplit["suno_v3.5"].append( "fake_{:05d}_suno_1.mp3".format(k) )
for k in s_3:
    vsplit["suno_v3"].append( "fake_{:05d}_suno_0.mp3".format(k) )
    vsplit["suno_v3"].append( "fake_{:05d}_suno_1.mp3".format(k) )
for k in s_2:
    vsplit["suno_v2"].append( "fake_{:05d}_suno_0.mp3".format(k) )
    vsplit["suno_v2"].append( "fake_{:05d}_suno_1.mp3".format(k) )
for k in u_120:
    vsplit["udio_v120"].append( "fake_{:05d}_udio_0.mp3".format(k) )
    vsplit["udio_v120"].append( "fake_{:05d}_udio_1.mp3".format(k) )
for k in u_30:
    vsplit["udio_v30"].append( "fake_{:05d}_udio_0.mp3".format(k) )
    vsplit["udio_v30"].append( "fake_{:05d}_udio_1.mp3".format(k) )


np.save("sonics_split.npy", vsplit)