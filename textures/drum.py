import numpy as np

from constants import WINDOW_WIDTH, PIXEL_SIZE, DISP_WIDTH

drumgrating_contrast = 1
drumgrating_MeanLum = 35
GammaFactor = 2.455466
AmpFactor = 0.000197
drumgrating_Amp_sinu = 5
drumgrating_SpatFreqVal = 0.1
drumgrating_tempFreqVal = 0.4


def drumTexture(frameRate):
    pixelangle = np.empty(
        shape=[1, WINDOW_WIDTH]
    )  # pixel has to be 2D since the image is 2D
    temp = np.array(range(WINDOW_WIDTH))
    temp.reshape(1, WINDOW_WIDTH)  # the temp must be 2D
    tempPixelAngle = (
        np.degrees(
            np.arctan((temp - (WINDOW_WIDTH / 2.0)) * PIXEL_SIZE * (2.0 / DISP_WIDTH))
        )
        + 45
    )  # calculating the pixel angle for first monitor

    for i in range(1):
        pixelangle[:, i * WINDOW_WIDTH : (i + 1) * WINDOW_WIDTH] = (
            tempPixelAngle + 90 * i
        )  # taking specific ranges within the full winWidth and replacing the values with the corresponding angles

    pixelformeanlum = (
        2 * (np.exp(np.log(drumgrating_MeanLum / AmpFactor) / GammaFactor) / 255.0) - 1
    )
    drumgrating_gray = drumgrating_MeanLum
    inc = drumgrating_gray * drumgrating_contrast

    # frames to be calculated per period
    frames = round(frameRate / drumgrating_tempFreqVal)

    phase = np.array(range(int(frames)))
    phase = (
        drumgrating_Amp_sinu
        * np.sin((phase / frames) * 2 * np.pi)
        * drumgrating_SpatFreqVal
        * 2
        * np.pi
    )

    # generating the pixel values for the stimulus
    texdata1D = []  # list that will hold all frames
    for i in range(int(frames)):
        texdata1DTmp = np.exp(
            np.log(
                (
                    drumgrating_gray
                    + inc
                    * np.sin(
                        pixelangle * drumgrating_SpatFreqVal * 2 * np.pi + phase[i]
                    )
                )
                / AmpFactor
            )
            / GammaFactor
        )
        pixVal = (
            2 * (texdata1DTmp / 255) - 1
        )  # converting the pixel values from 0:255 to -1:1
        texdata1D.append(pixVal)

    return texdata1D