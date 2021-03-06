import vanidl
from vanidl.analyzer import VaniDL
import argparse
parser = argparse.ArgumentParser(description='TensorFlow CIFAR10 Example')
parser.add_argument('darshan', type=str, default="./profile.darshan", metavar='N',
                    help='input batch size for training (default: 64)')
args = parser.parse_args()
profile = VaniDL()
#Load darshan file
import string
import random
N = 7
res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))    
status = profile.Load(args.darshan, preprocessed_dir = "/tmp/hzheng_%s"%res)
#Get Job Summary
summary = profile.GetSummary()
tl = profile.CreateIOTimeline()
import matplotlib.pylab as plt
# Print High level summary 
profile.PrintSummary()

## I/O timeline 
plt.figure(figsize=(20,4))
plt.grid()
plt.plot(tl['time_step']/1000, tl['read_count'], label='read')
plt.plot(tl['time_step']/1000, tl['write_count'], label='write')
plt.xlabel("Time (second)")
plt.ylabel("# of IO operation")
plt.savefig("timeline.png")
#plt.show()

import pprint
pp = pprint.PrettyPrinter(indent=1)

print("Size of dataset (bytes)")
pp.pprint(profile.GetFileSizes())
df = profile.GetDXTAsDF()
pp.pprint("Files used in the application")
pp.pprint(df['Filename'].unique().tolist())

for file in df['Filename'].unique():
    print("I/O performed on file {}: {:0.2f} MB".format(file,float(profile.GetIOSize(filepath=file))/1024.0/1024.0))

##  Generate Timeline
profile.CreateChromeTimeline(location="./", filename="timeline.json")
tensorboard_dir="log_dir"
val = profile.CreateMergedTimeline(tensorboard_dir, "./", "merge", save=True, timeshift=2.745017)
