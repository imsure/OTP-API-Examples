import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

base_dir = 'data_plots2'

locations = ('metropia', 'ec2')
runs = (500, 1000, 5000, 10000)

data = np.loadtxt(os.path.join(base_dir, 'routing_1000_seq_ec2.txt'), delimiter=' ')
times = data[:, 2]
avg = np.mean(times)
fig = plt.figure()
plt.hist(times, bins=50, color='y')
plt.xlabel('OTP Server Response Time (in ms)')
plt.ylabel('# of Hits')
plt.title('1000 API Requests Issued Sequentially from a EC2 instance\nAverage Response Time: {0:.2f} ms'.format(avg))
fig.savefig(os.path.join(base_dir, 'routing_1000_seq_ec2.png'))
print('run seq 1000 ec2:', avg)


for run in runs:
    for loc in locations:
        data = np.loadtxt(os.path.join(base_dir, 'routing_{}_{}.txt'.format(run, loc)), delimiter=' ')
        times = data[:, 2]
        avg = np.mean(times)
        fig = plt.figure()
        plt.hist(times, bins=50, color='y')
        plt.xlabel('OTP Server Response Time (in ms)')
        plt.ylabel('# of Hits')
        plt.title('{} API Requests issued concurrently from {}\n'
                  'Average Response Time: {:.2f} ms'.format(run, loc, avg))
        fig.savefig(os.path.join(base_dir, 'routing_{}_{}.png'.format(run, loc)))
        print('{} requests: avg response time {} ms'.format(run, avg))
