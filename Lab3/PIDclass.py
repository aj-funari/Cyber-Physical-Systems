class pidclass(object):

    def __init__(self):
        self.f = open('data.csv', 'w')
        self.data = []

    def loginfo(self, timestamp, dev, error, pterm, iterm, dterm, left, right):
        self.data.append(timestamp)
        self.data.append(dev)
        self.data.append(error)
        self.data.append(pterm)
        self.data.append(iterm)
        self.data.append(dterm)
        self.data.append(left)
        self.data.append(right)
        self.f.write(str(self.data) + '\n')
        del self.data[:]

    def freq(self, a, b):
        target_freq = 1/a  # frequency from time.sleep() function
        real_freq = 1/b  # real frequency of loop
        out = ((target_freq - real_freq) / target_freq) * 100
        return(out)
