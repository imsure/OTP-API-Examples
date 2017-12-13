import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('runtime_seq_1000.txt', delimiter=' ')
times = data[:,1]
avg = np.mean(times)
fig = plt.figure()
plt.hist(times, bins=50, color='y')
plt.xlabel('OTP Server Response Time (in ms)')
plt.ylabel('# of Hits')
plt.title('1000 API Requests Issued Sequentially\nAverage Response Time: {0:.2f} ms'.format(avg))
fig.savefig('runtime_seq_1000.png')
print ('run seq 1000:', avg)

for i in range(1,7):
    data = np.loadtxt('run{}.txt'.format(i), delimiter=' ')
    times = data[:,2]
    avg = np.mean(times)
    fig = plt.figure()
    plt.hist(times, bins=50, color='y')
    plt.xlabel('OTP Server Response Time (in ms)')
    plt.ylabel('# of Hits')
    plt.title('1000 API Requests Issued Concurrently\nAverage Response Time: {0:.2f} ms'.format(avg))
    fig.savefig('run{}.png'.format(i))
    print ('run {}:'.format(i), avg)
