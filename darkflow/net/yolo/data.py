from ...utils.pascal_voc_clean_xml import pascal_voc_clean_xml
from numpy.random import permutation as perm
from .predict import preprocess
# from .misc import show
from copy import deepcopy
import pickle
import numpy as np
import os 

def parse(self, exclusive = False):
    meta = self.meta
    ext = '.parsed'
    ann = self.FLAGS.annotation
    if not os.path.isdir(ann):
        msg = 'Annotation directory not found {} .'
        exit('Error: {}'.format(msg.format(ann)))
    print('\n{} parsing {}'.format(meta['model'], ann))
    dumps = pascal_voc_clean_xml(ann, meta['labels'], exclusive)
    return dumps




def shuffle(self):
    batch = self.FLAGS.batch
    data = self.parse()
    size = len(data)

    print('Dataset of {} instance(s)'.format(size))
    if batch > size: self.FLAGS.batch = batch = size
    batch_per_epoch = int(size / batch)

    for i in range(self.FLAGS.epoch):
        shuffle_idx = perm(np.arange(size))
        for b in range(batch_per_epoch):
            # yield these
            x_batch = list()
            feed_batch = dict()

            for j in range(b*batch, b*batch+batch):
                train_instance = data[shuffle_idx[j]]
                try:
                    inp, new_feed = self._batch(train_instance)
                except ZeroDivisionError:
                    print("This image's width or height are zeros: ", train_instance[0])
                    print('train_instance:', train_instance)
                    print('Please remove or fix it then try again.')
                    raise

                if inp is None: continue
                x_batch += [np.expand_dims(inp, 0)]

                for key in new_feed:
                    new = new_feed[key]
                    old_feed = feed_batch.get(key, 
                        np.zeros((0,) + new.shape))
                    feed_batch[key] = np.concatenate([ 
                        old_feed, [new] 
                    ])      
            
            x_batch = np.concatenate(x_batch, 0)
            yield x_batch, feed_batch
        
        print('Finish {} epoch(es)'.format(i + 1))

