# Hey, Jetson!
## Automatic Speech Recognition Inference
### By Brice Walker

[View full notebook on nbviewer](https://nbviewer.jupyter.org/github/bricewalker/Hey-Jetson/blob/master/Speech.ipynb)

![audio](app/static/images/raw.png)

This project builds a scalable attention based speech recognition platform in Keras/Tensorflow for inference on the Nvidia Jetson Embedded Computing Platform for AI at the Edge. This real-world application of automatic speech recognition was inspired by my previous career in mental health. This project begins a journey towards building a platform for real time therapeutic intervention inference and feedback. The ultimate intent was to build a tool that can give therapists real time feedback on the efficacy of their interventions, but on-device speech recognition has many applications in mobile, robotics, or other areas where cloud based deep learning is not desirable. The focus of this project is applied data science rather than academic research.

The final production model consists of a deep neural network with 3 layers of dilated convolutional neurons, 7 layers of bidirectional recurrent neurons (GRU cells), a single attention layer and 2 layers of time distributed dense neurons. This model makes use of a CTC loss function, the Adam optimizer, batch normalization, dilated convolutions, recurrent dropout, bidirectional layers, and attention based mechanisms. The model was trained on an Nvidia GTX1070(8G) GPU for 30 epochs for a total training time of roughly 6.5 days. The overall cosine similarity of the model's predictions with the ground truth transcriptions in the test set is about 78% (80% on validation set), while the overall word error rate is around 18% on the test set (16% on the validation set).

This project also includes a flask web server for deploying an applied speech inference engine using a REST API.

## Outline
- [Getting started](#start)
- [Introduction](#intro)
- [Tools](#tools)
- [Dataset](#data)
- [Feature Extraction/Engineering](#features)
- [Recurrent Neural Networks](#rnn)
- [Performance](#performance)
- [Inference](#inference)
- [Conclusion](#conclusion)

<a id='start'></a>

## Getting Started

I have provided full instructions for downloading the project, preparing the data, training the model and deploying the web app using Ubuntu 18.04 LTS. This has not been tested on other platforms.

#### Downloading the code repository

You will need to clone the repo with git (you will also need git-lfs), to do so, run:

```
sudo apt-get update
sudo apt-get install git
sudo apt-get install git-lfs
git clone https://github.com/bricewalker/Hey-Jetson.git
```

#### Preparing the dataset

Download the data set from the [LibriSpeech ASR corpus](http://www.openslr.org/12/).

Be sure to download the train-clean-100, train-clean-360, and train-other-500 datasets and combine them into one folder, named 'train' within the LibriSpeech directory. You will also want to combine the test-clean/test-other data sets into a folder named 'test', and dev-clean/dev-other data sets into a folder named 'dev'.

The audio files are prepared using a set of scripts borrowed from [Baidu Research's Deep Speech GitHub Repo](https://github.com/baidu-research/ba-dls-deepspeech).

flac_to_wav.sh converts all flac files to .wav format and create_desc_json.py will create a corpus for each data set: This will be a JSON formatted dictionary that includes the filepath, the length of the file, and the ground truth label.

For this script to work, you will need to obtain the ffmpeg/libav package.
Use the following command:

```sudo apt-get install ffmpeg```

Alternatively: You can download and build from [source](https://www.ffmpeg.org).

Run flac_to_wav.sh from the directory containing the dataset. This might take a while depending on your machine: 

```flac_to_wav.sh```

Now navigate to your code repo and run create_desc_json.py, specifying the path to the dataset and the names for the corpus files, the commands should look like this:

```
python create_desc_json.py /home/brice/LibriSpeech/train train_corpus.json
python create_desc_json.py /home/brice/LibriSpeech/dev valid_corpus.json
python create_desc_json.py /home/brice/LibriSpeech/test test_corpus.json
```

#### Preparing the Development Environment
It is recommended that you use Python 3.6+ in a conda environment for the training server. 

You can download anaconda from [anaconda.com](https://www.anaconda.com/) or miniconda from [conda.io](https://conda.io/en/latest/miniconda.html).

To prepare the development environment, first navigate to the conda folder in the repo in your terminal, then create the environment with the provided conda environment file:

```
cd conda
conda env create -f environment.yml
```

> Note: This relies on some pre-built conda packages for [SoundFile](https://pypi.org/project/SoundFile/) and [python_speech_features](https://pypi.org/project/python_speech_features/). You may have problems with these, so I have included [conda build](https://conda.io/projects/conda-build/en/latest/index.html) recipes for building the packages if you have problems downloading the pre-compiled packages. Soundfile has a dependency on [libsndfile](http://www.mega-nerd.com/libsndfile/) which may give you trouble so I have included a dll file that sometimes fails to install on Windows. You may need to manually install libsndfile on linux/unix based systems.

Then activate the environment with:

```conda activate heyjetson```

If you would prefer to use pip to install and manage dependencies, you can create a virtual environment and install the dependencies using the provided requirements file.
Linux/Unix based systems:

```
python -m venv venv
source venv/bin/activate
pip install -r server_requirements.txt
```

Or on Windows:

```
python -m venv venv
venv/scripts/activate.bat
pip install -r server_requirements.txt
``` 

> Note: To take advantage of the GPU compute capabilities within Tensorflow/Keras, you will need to install the required Nvidia dependencies, [CUDA 9.0](https://developer.nvidia.com/cuda-zone) and [cuDNN 7](https://developer.nvidia.com/cudnn).

#### Training the model

Now you can run the train_model.py script to train the full RNN: 

```python train_model.py```

Optionally, you can run through the provided notebook in Jupyter for a walk through of the modeling process and an in depth exploration of automatic speech recognition.

#### Preparing the Jetson based production server for deployment
To prepare the Jetson for deployment of the inference engine, you will need to flash it with the latest version of L4T. It is recommended that you do this by downloading and installing [JetPack 4.2](https://developer.nvidia.com/embedded/jetpack) on an Ubuntu server and then following the included instructions for flashing the Jetson. You will need to make sure to select the options to pre-install [CUDA 10.0](https://developer.nvidia.com/cuda-toolkit), and [cuDNN 7.6.0](https://developer.nvidia.com/cudnn) on to the device. 

You will then need to install pip and python-dev with: 

```sudo apt-get install python3-pip python3-dev``` 

It is recommended that you use Python 3.5+ in a virtual environment for the inference engine. To do so, navigate to the project directory and run: 

```python -m venv venv```

Then activate the environment with:

```source venv/bin/activate```

Then you can install the required dependencies: 
```pip install -r jetson_requirements.txt``` 

> Note: You may need to install some libraries using apt-get with a command like this: ```sudo apt-get install python3-<libraryname>```

You will need to build TensorFlow from source on the TX2:

To build TensorFlow from source, follow the instructions from [JetsonHacks](https://github.com/jetsonhacks/installTensorFlowTX2).

You may be able to install TensorFlow from a wheel file provided by [Jason at Nvidia](https://github.com/JasonAtNvidia/JetsonTFBuild).

#### Running the inference server
Begin by navigating to the project repo and exporting the path to the server as an environment variable:

```echo "export FLASK_APP=inference.py" >> ~/.profile```

Finally, initialize the web app with: 

```flask run```

Now you can access and test the inference engine in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000) or [http://localhost:5000](http://localhost:5000).

#### Publishing the Web App
The Flask server is not recommended for deployment in production. It is recommended to use a more robust server like [gunicorn](http://gunicorn.org/). You can then use a reverse proxy like [NGINX](https://www.nginx.com/) to publish your local web server to the internet. You can use a program like [Supervisor](http://supervisord.org/) to automate this process.

 To do so, run: 

 ```
 sudo apt-get -y update
 sudo apt-get -y install supervisor nginx
 ```

You should test out the gunicorn webserver by running: 

```gunicorn -b localhost:8000 -w 1 inference:app```

This should initiate 1 instance of the webserver (which will not allow multiple people to access the website at the same time). You should be able to access the server at [http://127.0.0.1:8000](http://127.0.0.1:8000) or [http://localhost:8000](http://localhost:8000).

If this works, you can set up Supervisor to monitor the server and ensure it is always running by creating a config file with:

```sudo gedit /etc/supervisor/conf.d/inference.conf```

The contents of the file should look something like this:

```
[program:inference]
command=/home/brice/Hey-Jetson/venv/bin/gunicorn -b localhost:8000 -w 1 inference:app
directory=/home/brice/Hey-Jetson
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```
> Note: Here, I have created a separate user account to run the server to prevent outsiders from getting access to the local device. This was done with:
 ```
 sudo adduser --gecos "" ubuntu
 sudo usermod -aG sudo ubuntu
 ```

Now, you will need to reload the supervisor service with:

```sudo supervisorctl reload```

Your server should now be running and monitored.

To set up the NGINX reverse proxy, first you will need to create temporary self-issued ssl certificates with the following commands:

```
mkdir certs
openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
  -keyout certs/key.pem -out certs/cert.pem
```

Now, you can create the config file for NGINX with these commands:

```
sudo rm /etc/nginx/sites-enabled/default
sudo gedit /etc/nginx/sites-enabled/inference
```

The contents of the config file should look like this:

```
server {
    # listen on port 80 (http)
    listen 80;
    server_name heyjetson.com;
    location / {
        # redirect any requests to the same URL but on https
        return 301 https://$host$request_uri;
    }
}
server {
    # listen on port 443 (https)
    listen 443 ssl;
    server_name heyjetson.com;

    # location of the self-signed SSL certificate
    ssl_certificate /home/brice/Hey-Jetson/certs/cert.pem;
    ssl_certificate_key /home/brice/Hey-Jetson/certs/key.pem;

    # write access and error logs to /var/log
    access_log /var/log/inference_access.log;
    error_log /var/log/inference_error.log;

    location / {
        # forward application requests to the gunicorn server
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        # handle static files directly, without forwarding to the application
        alias /home/brice/Hey-Jetson/app/static;
        expires 30d;
    }
}
```

Once you've saved the file, you can reload the NGINX server with:

```sudo service nginx reload```

Before pointing your domain at your local server, you will want to get a proper SSL certificate, which can be done with certbot. This can be done with the following commands:

```
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx
sudo certbot --nginx
```

Alternatively, you can run the server using the handy script I have provided. You will need to change the directory the script points to and then run it with:

```./server.sh```

Your webserver should now be live.

<a id='intro'></a>
## Introduction

This end-to-end machine learning project explores methods for preparing audio files for machine learning algorithms, then constructs a series of increasingly complex sequence-to-sequence neural networks for character-level phonetics sequencing models. For this project, I have chosen Recurrent Neural Networks, as they allow us to harness the power of deep neural networks for time sequencing issues and allow fast training on GPU's compared to other models. I chose character level phonetics modeling as it provides a more accurate depiction of language and would allow building a system that can pick up on the nuances of human-to-human communication in deeply personal conversations. Additionally, this project explores measures of model performance and makes predictions based on the trained models. Finally, I build an inference engine for a web app for real time predictions on speech.

### Automatic Speech Recognition
Speech recognition models are based on a statistical optimization problem called the fundamental equation of speech recognition. Given a sequence of observations, we look for the most likely sequence. So, using Bayes Theory, we are looking for the word or character sequence which maximizes the posterior probability of the word or character given the observation. The speech recognition problem is a search over this model for the best sequence.

Character level speech recognition can be broken into two parts; the acoustic model, that describes the distribution over acoustic observations, O, given the character sequence, C; and the language model based solely on the character sequence which assigns a probability to every possible character sequence. This sequence to sequence model combines both the acoustic and language models into one neural network, though pretrained language models are available from [kaldi](http://www.kaldi-asr.org/downloads/build/6/trunk/egs/) if you would like to speed up training and improve performance.

### Problem Statement
My goal was to build a character-level ASR system using a recurrent neural network in TensorFlow that can run inference on an Nvidia Pascal/Volta based GPU with a word error rate of <20%.

<a id='libraries'></a>
## Tools
The tools used in this project include:

- Ubuntu
- Python
- Anaconda
- HTML
- CSS
- JavaScript
- VS Code
- Jupyter Notebook
- Keras
- TensorFlow
- Sci-kit Learn
- matplotlib
- seaborn
- Azure Cognitive Services Speech API
- gunicorn
- CUDA
- cuDNN
- NGINX
- Supervisor
- Certbot

<a id='data'></a>
## Dataset
The primary dataset used is the [LibriSpeech ASR corpus](http://www.openslr.org/12/) which includes 1000 hours of recorded speech. A 960 hour subset of the dataset of 10-15 second audio files was used for training the models. The dataset consists of 16kHz audio files of spoken English derived from read audiobooks from the LibriVox project. The dataset consists of 16kHz audio files between 2-15 seconds long of spoken English derived from read audiobooks from the LibriVox project. The audio files were converted to single channel (mono) WAV/WAVE files (.wav extension) with a 64k bit rate, and a 16kHz sample rate. They were encoded in PCM format, and then cut/padded to an equal length of 10 seconds. The pre-processing techniques used for the text transcriptions included the removal of any punctuation other than apostrophes, and transforming all characters to lowercase. An overview of some of the difficulties of working with data such as this can be found <a href="https://awni.github.io/speech-recognition/">here</a>.

<a id='features'></a>
## Feature Extraction/Engineering
There are 3 primary methods for extracting features for speech recognition. This includes using raw audio forms, spectrograms, and mfcc's. For this project, I have created a character level sequencing model. This allows me to train a model on a data set with a limited vocabulary that can generalize to more unique/rare words better. The downsides are that these models are more computationally expensive, more difficult to interpret/understand, and they are more susceptible to the problems of vanishing or exploding gradients as the sequences can be quite long.

This project explores the following methods of feature extraction for acoustic modeling:

### Raw Audio Waves
This method uses the raw wave forms of the audio files and is a 1D vector of the amplitude where X = [x1, x2, x3...].

![raw](app/static/images/raw.png)

### Spectrograms 
![3dspectrogram](app/static/images/3dspectrogram.png)
<br>
This transforms the raw audio wave forms into a 2D tensor where the first dimension corresponds to time (the horizontal axis), and the second dimension corresponds to frequency (the vertical axis) rather than amplitude. We lose a little bit of information in this conversion process as we take the log of the power of FFT. This gives us 161 features, so each feature corresponds to something between 99-100 Hz. This can be written as log |FFT(X)|^2.

![spectrogram](app/static/images/spectrogram.png)

### MFCC's
Like the spectrogram, this turns the audio wave form into a 2D array. This works by mapping the powers of the Fourier transform of the signal, and then taking the discrete cosine transform of the logged mel powers. This produces a 2D array with reduced dimensions when compared to spectrograms, effectively allowing for compression of the spectrogram and speeding up training, as we are left with 13 features.

![mfcc](app/static/images/mfcc.png)

<a id='rnn'></a>
## Recurrent Neural Networks
For this project, the architecture chosen is a (Recurrent) Deep Neural Network (RNN) as it is easy to implement, and scales well. At its core, this is a machine translation problem, so an encoder-decoder model is an appropriate framework choice. Recurrent neurons are similar to feedforward neurons, except they also have connections pointing backward. At each step in time, each neuron receives an input as well as its own output from the previous time step. Each neuron has two sets of weights, one for the input and one for the output at the last time step. Each layer takes vectors as inputs and outputs some vector. This model works by calculating forward propagation through each time step, t, and then back propagation through each time step. At each time step, the speaker is assumed to have spoken 1 of 29 possible characters (26 letters, 1 space character, 1 apostrophe, and 1 blank/empty character used to pad short files since inputs will have varying length). The output of this model at each time step will be a list of probabilities for each possible character.

### Model Architecture

Hey, Jetson! is comprised of an acoustic model and language model. The acoustic model scores sequences of acoustic model labels over a time frame and the language model scores sequences of characters. A decoding graph then maps valid acoustic label sequences to the corresponding character sequences. Speech recognition is a path search algorithm through the decoding graph, where the score of the path is the sum of the score given to it by the decoding graph, and the score given to it by the acoustic model. So, to put it simply, speech recognition is the process of finding the character sequence that maximizes both the language and acoustic model scores. The model architecture is loosely based on Baidu's Deep Speech 2 project and includes 1 layer of convolutional neurons for early pattern detection, 2 layers of dialated convolutions, 7 layers of bidirectional GRU units, and 2 layers of time distributed dense neurons.

### CNN's
The deep neural network in this project explores the use of a Convolutional Neural Network consisting of 256 neurons for early pattern detection. The initial layer of convolutional neurons conducts feature extraction for the recurrent network.

### Dilated Convolutions
The model also uses a dilated CNN layer. Dilation introduces gaps into the CNN's kernels, so that the receptive field must encircle areas rather than simply slide over the window in a systematic way. This means that the convolutional layer can pick up on the global context of what it is looking at while still only having as many weights/inputs as the standard form.

### Batch Normalization
Hey, Jetson! also uses batch normalization, which normalizes the activations of the layers with a mean close to 0 and standard deviation close to 1. This reduces gradient expansion and prevents the network from overfitting.

### LSTM/GRU Cells
My RNN explores the use of layers of Long-Short Term Memory Cells and Gated Recurrent Units. LSTM's include forget and output gates, which allow more control over the cell's memory by allowing separate control of what is forgotten and what is passed through to the next hidden layer of cells. GRU's are a simplified type of Long-Short Term Memory Recurrent Neuron with fewer parameters than typical LSTM's. These work via a single memory update gate and provide most of the performance of traditional LSTM's at a fraction of the computing cost.

### Bidirectional Layers
This project explores connecting two hidden layers of opposite directions to the same output, making their future input information reachable from the current state. To put it simply, this creates two layers of neurons; 1 that goes through the sequence forward in time and 1 that goes through it backward through time. This allows the output layer to get information from past and future states meaning that it will have knowledge of the letters located before and after the current utterance. This can lead to great improvements in performance but comes at a cost of increased latency.

### Recurrent Dropout
This model also employs randomized dropout of units to prevent the model from over fitting.

### Attention Mechanism
The decoder portion of the model includes the ability to "attend" to different parts of the audio clip at each time step. This lets the model learn what to pay attention to based on the input and what it has predicted the output to be so far. Attention allows the network to refer back to the input sequence by giving the network access to its internal memory, which is the hidden state of the encoder (the RNN layers).

### Time Distributed Dense Layers
The ASR model explores the addition of layers of normal Dense neurons to every temporal slice of the input sequence. 

### Loss Function
The loss function I am using is a custom implementation of Connectionist Temporal Classification (CTC), which is a special case of sequential objective functions that addresses some of the modeling burden in cross-entropy that forces the model to link every frame of input data to a label. CTC's label set includes a "blank" symbol in its alphabet so if a frame of data doesn’t contain any utterance, the CTC system can output "blank" indicating that there isn't enough information to classify an output. This also has the added benefits of allowing us to have inputs/outputs of varying length as short files can be padded with the "blank" character. This function only observes the sequence of labels along a path, ignoring the alignment of the labels to the acoustic data.

<a id='performance'></a>
## Performance
Language modeling, the component of a speech recognition system that estimates the prior probabilities of spoken sounds, is the system's knowledge of what probable character sequences are. This system uses a class based language model, which allows it to narrow down its search field through the vocabulary of the speech recognizer (the first part of the system) as it will rarely see a sentence that looks like "the dog the ate sand the water" so it will assume that 'the' is not likely to come after the word 'sand'. We do this by assigning a probability to every possible sentence and then picking the characters with the highest prior probability of occurring. Language model smoothing (often called discounting) will help us overcome the problem that this creates a model that will assign a probability of 0 to anything it hasn't witnessed in training. This is done by distributing non-zero probabilities over all possible occurrences in proportion to the unigram probabilities of characters. This overcomes the limitations of traditional n-gram based modeling and is all made possible by the added dimension of time sequences in the recurrent neural network.

The best performing model is considered the one that gives the highest probabilities to the characters that are found in a test set, since it wastes less probability on characters that don't actually occur.

The overall <a href="https://en.wikipedia.org/wiki/Cosine_similarity">cosine similarity</a> of the model's predictions with the ground truth transcriptions in the test set is about 78% (80% on validation set), while the overall <a href="https://en.wikipedia.org/wiki/Word_error_rate">word error rate</a> is around 18% on the test set (16% on the validation set).
![performance](app/static/images/performance.png)

<a id='inference'></a>
## Inference
Finally, I demonstrate exporting the model for quick local inference. The model can produce text transcriptions within a range between 1-5 seconds, allowing for sub real-time inferencing. The project is deployed to the web as a flask web app using a python based REST API. The web app is built using HTML and CSS and then published using a gunicorn server and NGINX reverse proxy. The web application includes an inference engine to allow users to upload custom recorded speech for fast inferencing using the production neural network. The app also includes performance and visualization engines that allow users to more closely inspect the data sets used in the development process and to benchmark the model's performance. Functionality has been included to interface with the Microsoft Azure Cognitive Services API's speech to text so that users can benchmark the model against other cloud based speech services. A JavaScript API for automatic speech recognition utilizing the Microsoft Speech-To-Text platform is provided as well. Finally, a sentiment engine was developed using Microsoft's Cognitive Services to allow users to assess how sentiment analysis can be conducted on the model's predicted transcriptions to begin to derive a measure of conversational and therapeutic interactions. It is hypothesized that sentiment analysis could be useful in determining whether or not someone is responding positively to a therapeutic intervention as the content of their responses may be more positive rather than negative.

<a id='conclusion'></a>
## Conclusion

This concludes the model construction demo. You have now trained a strong performing recurrent neural network for speech recognition, from scratch, with a word error rate of <20% and have deployed it to the web with the flask web app framework.

#### Next Steps

Next steps for this project, and things you can try on your own, include: 
- Build a deeper model with more layers.
- Train the model on [audio with background noise](https://www.tensorflow.org/versions/master/tutorials/audio_recognition).
- Train the model on [Mozilla's Common Voice](https://voice.mozilla.org/) dataset to identify the speaker's gender and accent using this [reference project](https://github.com/mozilla/DeepSpeech).
- Train the model on conversational speech, like that found in the [Buckeye Corpus](https://buckeyecorpus.osu.edu/), [Santa Barbara Corpus](http://www.linguistics.ucsb.edu/research/santa-barbara-corpus), or [COSINE Corpus](http://melodi.ee.washington.edu/cosine/).
- Develop a production system for handling speech with sensitive personal information like in this reference [paper](resources/privateconversations.pdf).  
- Store user recorded audio for online training of the model to improve performance.
- Recreate the model in [TensorFlow](https://www.tensorflow.org/) for [improved performance](https://github.com/tensorflow/tensorflow). [Mozilla](https://github.com/mozilla/DeepSpeech) has demonstrated the incredible power of TensorFlow for ASR.
- Train the model using just the raw audio files, like this project from [Pannous](https://github.com/pannous/tensorflow-speech-recognition).
- Train the model to [identify individual speakers](resources/speakeridentification.pdf) like [Google](resources/googlespeaker.pdf) using the [VoxCeleb](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/) dataset.
- Train the model to identify the speaker's level of [emotion](resources/emotionrecognition.pdf). There are many examples on [Github](https://github.com/).
- Convert the inference engine to Nvidia's [TensorRT](https://developer.nvidia.com/tensorrt) inference platform using their [Developer Guide](http://docs.nvidia.com/deeplearning/sdk/tensorrt-developer-guide/index.html) and the [RESTful interface](https://devblogs.nvidia.com/tensorrt-container/).
- Train the model on other languages, like [Baidu's Deep Speech 2](resources/deepspeech2.pdf).
- Try out a [transducer model](resources/transducers.pdf), like Baidu is doing in [Deep Speech 3](http://research.baidu.com/deep-speech-3%EF%BC%9Aexploring-neural-transducers-end-end-speech-recognition/).
- Build a more traditional [encoder/decoder](resources/encoderdecoder.pdf) model as outlined by [Lu et al](resources/encoderdecoder2.pdf). 
- Add other [augmentation methods](https://distill.pub/2016/augmented-rnns/) besides just attention to the model.
- Add [peephole connections](resources/peepholes.pdf) to the [LSTM cells](https://www.tensorflow.org/api_docs/python/tf/contrib/rnn/LSTMCell).
- Add a [Hidden Markov Model](resources/hmm.pdf)/[Gaussian Mixture Model](resources/gmm.pdf).
- Use a pretrained language model like this one from [kaldi](http://www.kaldi-asr.org/downloads/build/6/trunk/egs/).
- Build a measure for calculating character level error rates.
- Reduce the word error rate to [<10%](https://hacks.mozilla.org/2017/11/a-journey-to-10-word-error-rate/).
- Include [entity extraction](https://towardsdatascience.com/entity-extraction-using-deep-learning-8014acac6bb8) in the model so that it can begin to identify the topic of discussion.
- Implement a [wake-word detection engine](https://github.com/Picovoice/Porcupine).

### Special Thanks

I want to thank the following people/organizations for their support and training:

- The instructional staff including Charles Rice, Riley Davis, and David Yerrington at [General Assembly](https://generalassemb.ly/) for their fantastic training in data science and machine/deep learning.
- Andrew Ng with [deeplearning.ai](https://www.deeplearning.ai/), for developing the [Coursera Course on Sequence Models](https://www.coursera.org/learn/nlp-sequence-models) which helped me understand the mathematics behind recurrent neural networks.
- [Microsoft ](https://www.microsoft.com/en-us/)for putting together the [edX course on Speech Recognition Systems](https://www.edx.org/course/speech-recognition-and-synthesis) which helped me understand the history of and theory behind speech recognition systems.
- Alexis Cook and the staff at [Udacity](https://www.udacity.com/), [IBM's Watson team](https://www.ibm.com/watson/), and the [Amazon Alexa](https://developer.amazon.com/alexa) team for the course on [Artificial Intelligence on Udacity](https://www.udacity.com/course/artificial-intelligence-nanodegree--nd889) which helped me learn how to apply my knowledge on a real world dataset.
- Paolo Prandoni and Martin Vetterli at [École Polytechnique Fédérale de Lausanne](https://www.epfl.ch/) for teaching the course on [Digital Signal Processing on Coursera](https://www.coursera.org/learn/dsp/) that helped me understand the mathematics behind the Fourier transform.
- The staff at [Nvidia](http://www.nvidia.com/page/home.html) who have helped me learn how to run inference on the Jetson.
- The Seattle DSI-3 Cohort at General Assembly for supporting my journey and giving me good constructive feedback in the development phase of this project.
- [Miguel Grinberg](https://blog.miguelgrinberg.com/index) whose book and online tutorial on Flask helped me learn how to deploy web apps in Flask.
- [Jetson Hacks](http://www.jetsonhacks.com/) for providing several tutorials and repos that helped me learn how to develop on the Jetson.

### Contributions

If you would like to contribute to this project, please fork and submit a pull request. I am always open to feedback and would love help with this project.
