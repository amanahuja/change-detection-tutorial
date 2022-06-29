# change-detection-tutorial

```md
Update June 2022
---
Hi folks! Thanks for continued interest in this tutorial. 

Much has changed this this tutorial was written, over a couple of free weekends, in 2014. Change detection is even more relevant. There are exciting new tools and libraries available.  Most folks who stumble across this tutorial are already familiar with the basic ideas. 

The python and jupyter ecosystem has also progressed, leaving the notebooks in this tutorial clunky or broken.

I do not have a plan to update the tutorial, as there hasn't been sufficient indication that this would be valuable. However:
* There are 50+ forks which I have not explored; you may find some of them to be usefully updated. 
* I will happily review and merge PRs to help update this tutorial. 
* Please submit an issue if you have a specific questions or request. 

Thanks again!

@amanqa
```

## Goals

We want to detect change in a signal, in an ordered/chronological collection of data points. We'll consider the case where each data point is a scalar value. 

## Tutorial Approach

We'll start with the simplest signals we can imagine, and the simplest change detection method(s). This will allow us to introduce some basic concepts easily. With the fundamentals set, we'll try to tackle some problems that are inspired by "real world" problems. This may add a lot of complexity quickly, and will question some assumptions we made earlier, but hopefully there will be sufficient context to pull that off. 

We  will either fabricate the data or use freely available public data sources. Python (python 2.7) will be used for coding and visualization, from within IPython Notebooks. although the principles are agnostic to choice of programming language. We may use open source python libraries along the way.  


## How to use this Tutorial

The simplest way to use this tutorial is to (only) view the output. You will not be able to edit or experiment with the code, but you will be able to follow along. 

***Simply follow the links to nbviewer.ipython.org to view the IPython notebooks. These links are located in the "Lesson Plan" section of this README. ***


However, the recommended way to use this tutorial is to clone the repo to your machine and run the ipython notebooks locally. Follow these steps: 

    ## 1. Clone this repo to a new directory on your machine
    
    ## 2. Set up a virtual environment using virtualenv or conda, and activate it. 

    ## 3. Install prerequisites listed under requirements.txt

    ## 4. Start an ipython notebook server and navigate to the notebooks in your browser
    
You'll be able to follow along with the tutorial and edit the code as you go, like any IPython Notebook. For more information see http://ipython.org/ipython-doc/stable/notebook/index.html


## Lesson Plan

Includes links to nbviewer.ipython.org to view the tutorial online. 

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


## More things to cover

If there's interest, I may add additional sections to cover these topics:

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

## References: 

Papers / Books: 

    Michèle Basseville
      - "Statistical methods for change detection" (2002)
      - "Detecting Changes in Signals and Systems: A Survey" (1988) Automation, Vol. 2,t, No. 3, pp. 309-326
    Aggarwall. 
      - "Outlier Detection" (2013 **check** )

Also see:

 - Aman Ahuja (blog post) -- http://pafnuty.wordpress.com/2014/05/29/change-detection-tutorial/
 - Aman Ahuja (blog post) -- http://pafnuty.wordpress.com/2013/02/05/reading-log-change-detection-papers-by-basseville/
 - Ted Dunning's Anomaly Detection solution (github repo): https://github.com/tdunning/anomaly-detection/

