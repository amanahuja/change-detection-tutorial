change-detection-tutorial
=========================

## Goals

We want to be able to detect change in a signal, or an ordered/chronological collection of data points. We'll probably use scalar values for each data point, but perhaps we can also consider vector values as well. 

## How to use this Tutorial

The simplest way to use the tutorial is to view the output only. You will not be able to edit and experiment with the code, but you will be able to follow along. 

 1. Use the links to nbviewer.ipython.org to view the ipython notebooks. 
 2. (Coming soon) Navigate to the PDF directory to view the notebooks auto-converted to PDF format. 

The recommended way to use this tutorial is to clone the repo to your machine and run the ipython notebooks locally. Follow these steps: 

    ## 1. Clone the repo to a new directory on your machine
    include command line example code
    
    ## 2. Set up a virtual environment using virtualenv or conda, and activate it. 
    # using conda
    # using virtualenv
    
    ## 3. Install prerequisites
    # TODO: insert a requirements.txt

    ## 4. Start an ipython notebook server
    ipython notebook 
    
    ## 5. Navigate to the nb server url in a browser


## Tutorial Approach
We'll start with the simplest signal we can imagine, and the simplest change detection method(s). From there we'll add signal complexity step by step in such a way that we demonstrate the limitations of previously discussed methods and have an excuse to consider more sophisticated approaches. 

The solutions we use will be self-wrought code or imported from open source libraries, whatever seems appropriate for the moment. 

## Lesson Plan

* Section 00: Scaffolding
[View in ipynb nbviewer] [1]

 * Offline vs. Online change detection
 * ChangeDetector a custom class used for tutorial


* Section 01: Introduction
[View in ipynb nbviewer] [2]

 * Introduction  (what is change detection)
 * Justification (why does change detection matter)

* Section 02
[View in ipynb nbviewer] [3]

 * A "static mean" change detector
 * Recent (amplitude) vs global (mean) detector 

* Section 03: Windows
[View in ipynb nbviewer] [4]

 * Outliers 
 * Noise
 * Streaming windows
 * A Z-score based detector

* Section 04: Welford's Method
[View in ipynb nbviewer] [5] 

 * Welford's method

* Section 05: CUSUM
[View in ipynb nbviewer] [6] 

 * hyperparameter sensitivity
 * CUSUM

* (Use case) Section 06: EKG 
[View in ipynb nbviewer] [7] 

 * Anomaly detection in EKG signals
 * @tdunning's method: 
    * Divide signal into windows
    * Build a "dictionary" of windows from a normal signal using kmeans clustering
    * Reconstruct signals using dictionary
    * Devise a trigger based on reconstruction error


[1]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_00_scaffolding.ipynb
[2]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_01_Introduction.ipynb
[3]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_02_StaticMean.ipynb
[4]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_03_Windows.ipynb
[5]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_04_WelfordsMethod.ipynb
[6]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_05_CUSUM.ipynb
[7]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_06_tdunning_method.ipynb

##More things to cover
Add additional sections to cover these:

 - likelihood ratio and cumalative sum tests. 
 - the Page-Hinkley Stopping Rule
 - using local approaches and moving windows to reduce computation costs. 
 - spectral properties of the incoming signal
 - CUSUM
 - peak detection vs. drift detection

Criteria for designing detection algorithms
(or analyzing their performance)
 - mean time b/w false alarms
 - prob of wrong detection [false positives]
 - mean delay to detection 
 - prob of non-detection [false negatives] 
 - accuracy of the estimates of the fault onset time and of magnitude of change


##References: 

Papers / Books: 

    Michèle Basseville
      - "Statistical methods for change detection" (2002)
      - "Detecting Changes in Signals and Systems: A Survey" (1988) Automation, Vol. 2,t, No. 3, pp. 309-326
    Aggarwall. 
      - "Outlier Detection" (2013 **check** )

Also see:

 - Aman Ahuja (blog post) -- http://pafnuty.wordpress.com/2013/02/05/reading-log-change-detection-papers-by-basseville/
 - Ted Dunning's Anomaly Detection solution (github repo): https://github.com/tdunning/anomaly-detection/

