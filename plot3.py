import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

base_dir = 'data_plots3'

data = np.loadtxt(os.path.join(base_dir, 'run_ec2elb_seq_1000_2.txt'), delimiter=' ')
times = data[:,2]
avg = np.mean(times)
fig = plt.figure()
plt.hist(times, bins=50, color='y')
plt.xlabel('OTP Server Response Time (in ms)')
plt.ylabel('# of Hits')
plt.title('1000 API Requests Issued to ELB Sequentially from a EC2 instance\nAverage Response Time: {0:.2f} ms'.format(avg))
fig.savefig(os.path.join(base_dir, 'runtime_ec2elb_seq_1000_2.png'))
print ('run seq 1000:', avg)

for i in range(1,2):
    data = np.loadtxt(os.path.join(base_dir, 'run_ec2elb_con_1000_{}.txt'.format(i)), delimiter=' ')
    times = data[:,2]
    avg = np.mean(times)
    fig = plt.figure()
    plt.hist(times, bins=50, color='y')
    plt.xlabel('OTP Server Response Time (in ms)')
    plt.ylabel('# of Hits')
    plt.title('1000 API Requests Issued Concurrently to ELB from a EC2 instance\nAverage Response Time: {0:.2f} ms'.format(avg))
    fig.savefig(os.path.join(base_dir, 'run_ec2elb_con_1000_{}.png'.format(i)))
    print ('run {}:'.format(i), avg)
