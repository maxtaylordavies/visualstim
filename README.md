# visualstim

## Getting started

1. clone this repo: `git clone https://github.com/maxtaylordavies/visualstim.git` and `cd visualstim`
2. create conda environment: `conda env create -f environment.yml`
   - if this fails, you can add the required packages manually with `conda install -c conda-forge pywinhook` and then `conda install -c conda-forge psychopy`
   - you can verify the package installations with `conda list` - you should see (amongst other things) `psychopy 2021.2.3`
3. run `python test.py` to see the GUI

## Basic usage

### Control window vs display window

After creating an instance of the `Interface` class and calling its `.start()` method, you should be greeted with a window that looks like this:

![screenshot of the visualstim GUI](./screenshots/v0.1/main-view.png)

This is the **visualstim control window**. It contains elements for interactively controlling the visual stimulation. By default, the **visualstim display window** is the same as the control window; i.e. when you click ![play](./screenshots/v0.1/play.png), the GUI elements of the control window disappear and are replaced by the stimulus, and return after the stimulus is complete. If you have more than one display available (e.g. you're running visualstim on a laptop connected to an external monitor), you can click ![switch screen](./screenshots/v0.1/switch-screen.png) to spin out a separate display window. This lets you show the control window on one screen while displaying the stimulus on another screen.

### Stimulus type

The **stimulus type** panel lets you choose the stimulus you want to display. Currently, the options are

- _drifting grating_: a sinusoidal grating that moves across the display window
- _static grating_: a sinusoidal grating that does not move (i.e. is static)
- _movie_: an arbitrary video file - should be placed in the `movies/` folder and be in a format supported by [AVbin](https://avbin.github.io/docs/) (e.g. `.mp4`, `.avi`, `.mov` etc)

More stimulus types will be added in future updates.

### Stimulus parameters

The **stimulus parameters** panel lets you adjust the parameters of the visual stimulation. The set of parameters available to control depends on which stimulus type is currently selected - e.g. for **drifting grating** we need to know the `temporal frequency`, for **movie** we need to know the `filename` etc

### Sync parameters

The **sync parameters** panel contains controls for synchronisation/triggering. If you don't need to synchronise your visual stimulation with any external system (e.g. 2P imaging, behavioural recording etc) then you can safely ignore this panel.

**Sync mode** is disabled by default. If you enable it by toggling ![sync: FALSE](./screenshots/v0.1/sync-false.png) to ![sync: TRUE](./screenshots/v0.1/sync-true.png), you should see two small black squares appear in the bottom left corner of the **display window**. These are the **trigger square** and **sync square**, and are intended to provide an interface to external systems via the use of photodiodes attached to the stimulus display monitor.

In **sync mode**, clicking ![play](./screenshots/v0.1/play.png) will not begin playing the visual stimulus immediately, but will instead activate a **trigger period**

- The purpose of the trigger period is to allow time for external systems (such as a 2P microscope) to activate, so that they start performing their function at the same time as the stimulus onset
- The length of the trigger period can be set within the sync panel
- At the start of the trigger period, the trigger square flashes white for 3 frames, producing a voltage pulse in the photodiode covering the trigger square
- This photodiode should be connected to the appropriate input(s) of whatever external system(s) you want to trigger

After the user-defined trigger duration has elapsed, the selected stimulus will begin playing as normal. In **sync mode**, while the stimulus is playing, the **sync square** will flash white every `n` frames (where `n` is the value supplied for `sync interval`). This allows the user to send a regular synchronisation pulse to an external clock system, in order to align the stimulus frame timestamps with data from any other systems (e.g. 2P imaging data).
