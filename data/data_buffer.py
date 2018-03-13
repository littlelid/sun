import numpy as np
import scipy.io as sio

class Data_buffer:
    def __init__(self, window_size = 8, normalize = True):
        self.window_size = window_size
        self.normalize = normalize

    def load_csi_from_file(self, csi_1_filepath, csi_0_filepath, var_name = 'cfr_array', channel = 50):

        raw_data_bit1 = sio.loadmat(csi_1_filepath)[var_name]
        raw_data_bit1 = np.abs(raw_data_bit1)
        self.csi_bit1 = raw_data_bit1[:, channel]

        raw_data_bit0 = sio.loadmat(csi_0_filepath)[var_name]
        raw_data_bit0 = np.abs(raw_data_bit0)
        self.csi_bit0 = raw_data_bit0[:, channel]
        print('len of csi 1:', len(self.csi_bit1), ' len of csi 0:', len(self.csi_bit0))

        strip_size = 50   # just to ensure purity of data
        self.csi_bit1 = self.csi_bit1[strip_size : -strip_size]
        self.csi_bit0 = self.csi_bit0[strip_size : -strip_size]


        self.csi_bit1_train = self.csi_bit1[: int(0.9*len(self.csi_bit1)) ]
        self.csi_bit1_test  = self.csi_bit1[int(0.9*len(self.csi_bit1)):]
        self.csi_bit0_train = self.csi_bit0[: int(0.9*len(self.csi_bit0)) ]
        self.csi_bit0_test  = self.csi_bit0[int(0.9*len(self.csi_bit0)) :]

        self.normalize_mean = np.mean(np.concatenate((self.csi_bit1_train, self.csi_bit0_train)))
        self.normalize_var  = np.var(np.concatenate((self.csi_bit1_train, self.csi_bit0_train)))


    def next_batch(self, batch_size = 500, one_zero_rate = 0.5) :
        batch_csi_bit1 = []
        batch_csi_bit0 = []

        batch_size_1 = int(batch_size * one_zero_rate)
        batch_size_0 = batch_size - batch_size_1

        while len(batch_csi_bit1) < batch_size_1:
            idxs = list(range(len(self.csi_bit1_train)))
            np.random.shuffle(idxs)
            for i in range( int(len(idxs) / self.window_size) ):
                batch_csi_bit1.append(self.csi_bit1_train[idxs[i * self.window_size : (i + 1) * self.window_size]])
        batch_csi_bit1 = np.array(batch_csi_bit1[:batch_size_1])


        while len(batch_csi_bit0) < batch_size_0:
            idxs = list(range(len(self.csi_bit0_train)))
            np.random.shuffle(idxs)
            for i in range(int(len(idxs) / self.window_size)):
                batch_csi_bit0.append(self.csi_bit0_train[idxs[i * self.window_size: (i + 1) * self.window_size]])
        batch_csi_bit0 = np.array(batch_csi_bit0[:batch_size_0])

        batch_X = np.concatenate((batch_csi_bit1, batch_csi_bit0))
        batch_y = np.concatenate((np.ones(batch_size_1, dtype=np.uint8), np.zeros(batch_size_0, dtype=np.uint8)))
        batch_y = self.onehot(batch_y)

        if self.normalize:
            batch_X = (batch_X - self.normalize_mean) / self.normalize_var

        return batch_X, batch_y

    def get_test_set(self):

        test_csi_bit1 = np.array(
            [self.csi_bit1_test[i * self.window_size:(i + 1) * self.window_size] for i in range(int(len(self.csi_bit1_test) / self.window_size))])
        test_label_1 = [1 for i in range(int(len(self.csi_bit1_test) / self.window_size))]
        test_csi_bit0 = np.array(
            [self.csi_bit0_test[i * self.window_size:(i + 1) * self.window_size] for i in range(int(len(self.csi_bit0_test) / self.window_size))])
        test_label_0 = [0 for i in range(int(len(self.csi_bit0_test) / self.window_size))]

        X_test = np.concatenate((test_csi_bit1, test_csi_bit0))
        y_test = np.concatenate((test_label_1, test_label_0))
        y_test = self.onehot(y_test)

        if self.normalize:
            X_test = (X_test - self.normalize_mean) / self.normalize_var

        return X_test, y_test

    def get_train_set(self):
        X_train = []
        y_train = []

        for i in range(10):
            batch_X, batch_y = self.next_batch()
            X_train.append(batch_X)
            y_train.append(batch_y)

        X_train = np.concatenate(X_train)
        y_train = np.concatenate(y_train)

        return X_train, y_train

    def onehot(self, labels):
        ''' one-hot 编码 '''
        n_sample = len(labels)
        n_class = max(labels) + 1
        onehot_labels = np.zeros((n_sample, n_class))
        onehot_labels[np.arange(n_sample), labels] = 1

        return onehot_labels

if __name__ == "__main__":
    data_buffer = Data_buffer()
    csi1_filename = '/Users/wangweiguo/Desktop/zigfi/python_data/wifi10/dis1pow16.mat'
    csi0_filename = '/Users/wangweiguo/Desktop/zigfi/python_data/wifi10/dis1air2.mat'
    data_buffer.load_csi_from_file(csi1_filename, csi0_filename)
    z, v = data_buffer.next_batch()
    print(z.shape, v.shape)
    #print(.csi_bit1_train[idxs[i * self.window_size: (i + 1) * self.window_size]])
