
import numpy as np


def return_predict(self, im):
    assert isinstance(im, np.ndarray), 'Image is not a np.ndarray'
    h, w, _ = im.shape

    im = self.framework.resize_input(im)

    this_inp = np.expand_dims(im, 0)


    feed_dict = {self.inp : this_inp}

    out = self.sess.run(self.out, feed_dict)[0]

    boxes = self.framework.findboxes(out)


    threshold = self.FLAGS.threshold


    boxesInfo = list()

    for box in boxes:
        tmpBox = self.framework.process_box(box, h, w, threshold)

        if tmpBox is None:
            continue
        boxesInfo.append({
            "label": tmpBox[4],
            "confidence": tmpBox[6],
            "topleft": {
                "x": tmpBox[0],
                "y": tmpBox[2]},
            "bottomright": {
                "x": tmpBox[1],
                "y": tmpBox[3]}
        })
    return boxesInfo
