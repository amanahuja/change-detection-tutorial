change-detection-tutorial
=========================

## Goals

We want to be able to detect change in a signal, or an ordered/chronological collection of data points. We'll probably use scalar values for each data point, but perhaps we can also consider vector values as well. 

## Approach
We'll start with the simplest signal we can imagine, and the simplest change detection method(s). From there we'll add signal complexity step by step in such a way that we demonstrate the limitations of previously discussed methods and have an excuse to consider more sophisticated approaches. 

The solutions we use will be self-wrought code or imported from open source libraries, whatever seems appropriate for the moment. 

## Lesson Plan

* Section 0: Introduction

 * Introduction  (what is change detection)
 * Justification (why does change detection matter)
 * Offline vs. Online change detection
 * References and Further Reading
[View in ipynb nbviewer] [1]


* Section 1

 * A trivial signal
  * Signal 1
 * A "static mean" change detector
   * Recent (amplitude) vs global (mean) detector 
 * Framing the problem and some utility code  #maybe move this to an appendix?
[View in ipynb nbviewer] [2]

* Section 2
 * Limitation of the static mean detector
  * Outliers 
  * Noise
 * A noisy signal (with outliers?)
  * Signal 2
 * Streaming windows
 * Wilford's algorithm
 * A Z-score based detector
[View in ipynb nbviewer] [3]

* Section 3 
 * Limitations of the Z-score change detector
 * Trend, slowly moving signals
  * Signal 3
 * 
[View in ipynb nbviewer] [4] 

[1]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_00_Introduction.ipynb
[1]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_00_Introduction.ipynb
[1]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_00_Introduction.ipynb
[1]: http://nbviewer.ipython.org/github/amanahuja/change-detection-tutorial/blob/master/ipynb/section_00_Introduction.ipynb

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
    
    Michèle Basseville
      - "Statistical methods for change detection" (2002)
      - "Detecting Changes in Signals and Systems: A Survey" (1988) Automation, Vol. 2,t, No. 3, pp. 309-326
    Aggarwall. 
      - "Outlier Detection" (2013 **check** )

Also see 

Aman Ahuja
http://pafnuty.wordpress.com/2013/02/05/reading-log-change-detection-papers-by-basseville/

