import astropy.io.fits as pyfits
from astropy.io.fits import Header
from numpy.core import array

from external.cosmics import CosmicsImage
from common.image import Image
from skimage.measure import regionprops
from scipy.ndimage.measurements import label


def load(filepath, pos_filepath):
    """

    :param filepath: fits image path
    :return: an Image
    """

    # load image data information
    data = pyfits.getdata(filepath, hdu=0)
    primary = Header(pyfits.getheader(filepath, 0))
    headers = [primary]
    extcount = int(primary.get("NEXTEND", 0))

    for idx in range(1, extcount):
        ext = Header(pyfits.getheader(filepath, idx))
        headers.append(ext)

    # load position information
    pos_primary = Header(pyfits.getheader(pos_filepath, 0))
    pos_headers = [pos_primary]
    pos_extcount = int(pos_primary.get("NEXTEND", 0))

    for idx in range(1, pos_extcount):
        ext = Header(pyfits.getheader(pos_filepath, idx))
        pos_headers.append(ext)

    return Image(array(data), headers, pos_headers)


def clean_cr(raw, mask=None, iterations=4)->array:
    img = CosmicsImage(raw)
    img.clean(mask=mask)
    img.run(maxiter=iterations)

    return array(img.cleanarray), img.getmask()


def reduce_cr(cr_pixels, exptime):
    img = cr_pixels.astype(int) / exptime
    label_image, nf = label(img)
    props = regionprops(label_image)

    return props
