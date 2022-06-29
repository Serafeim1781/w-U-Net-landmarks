# Wave-U-Net with mouth landmarks (Pytorch)

Modified version of the [Wave-U-Net](https://arxiv.org/abs/1806.03185) for audio source separation, modified for audio-visual speach separation, implemented in Pytorch.

Click [here](https://github.com/f90/Wave-U-Net-Pytorch) for the original Wave-U-Net (Pytorch) implementation.

# Warning
* Some of the features of the [original](https://github.com/f90/Wave-U-Net-Pytorch) may be broken now.

# Installation

System requirements:
* Linux-based OS (Tested on Manjaro)
* Python 3.9
* [libsndfile](http://mega-nerd.com/libsndfile/) 
* [ffmpeg](https://www.ffmpeg.org/)
* CUDA 10.2 for GPU usage - Optional but 
strongly recommended

Dependencies:
* pytorch 1.9
* dlib 19.21
* imutils 0.5
* librosa 0.8

Please note that
dlib's pre-trained facial landmark dedector is also needed and can be found [here](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2).


Clone the repository:
```
git clone https://github.com/
```

Recommended: [Install *conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) and create a new virtual environment to install the required Python packages into.

```
conda env create --file waveunet-env.yml
```
then activate the virtual environment:
```
conda activate waveunet-env
```


# Download datasets

The [Audio-Visual Lombard GRID corpus](http://spandh.dcs.shef.ac.uk/avlombard/) is used for training and test. 

You can of course use your own datasets for training, but for this you would need to modify the code manually, which will not be discussed here.

# Training the models

To train a Wave-U-Net with mouth landmarks, the basic command to use is

```
python train.py --dataset_dir /PATH/TO/Lombardgrid 
```
where the path to Lombard GRID dataset needs to be specified. A ``train`` and ``test`` subfolders must be created and populated with the apropriet subset.
There will be a script to help split the dataset.

Add more command line parameters as needed:
* ``--cuda`` to activate GPU usage
* ``--hdf_dir PATH`` to save the preprocessed data (HDF files) to custom location PATH, instead of the default ``hdf`` subfolder in this repository
* ``--checkpoint_dir`` and ``--log_dir`` to specify where checkpoint files and logs are saved/loaded
* ``--load_model checkpoints/model_name/checkpoint_X`` to start training with weights given by a certain checkpoint

For more config options, see ``train.py``.

Training progress can be monitored by using Tensorboard on the respective ``log_dir``.
After training, the model is evaluated on the Lombard GRID test set, and SDR/SIR/SAR metrics are reported for all instruments and written into both the Tensorboard, and in more detail also into a ``results.pkl`` file in the ``checkpoint_dir``

<!-- # <a name="test"></a> Test trained models on songs!

We provide the default model in a pre-trained form as download so you can separate your own songs right away.

## Downloading our pretrained models

Download our pretrained model [here](https://www.dropbox.com/s/r374hce896g4xlj/models.7z?dl=1).
Extract the archive into the ``checkpoints`` subfolder in this repository, so that you have one subfolder for each model (e.g. ``REPO/checkpoints/waveunet``) -->

## Run pretrained model

<!-- To apply our pretrained model to any of your own songs, simply point to its audio file path using the ``input_path`` parameter:

```
python3.6 predict.py --load_model checkpoints/waveunet/model --input "audio_examples/Cristina Vane - So Easy/mix.mp3"
``` -->

* Add ``--cuda `` when using a GPU, it should be much quicker
* Point ``--input`` to the music file you want to separate

By default, output is written where the input music file is located, using the original file name plus the instrument name as output file name. Use ``--output`` to customise the output directory.

To run your own model:
* Point ``--load_model`` to the checkpoint file of the model you are using. If you used non-default hyper-parameters to train your own model, you must specify them here again so the correct model is set up and can receive the weights!
