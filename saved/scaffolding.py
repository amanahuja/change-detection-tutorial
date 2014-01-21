
# In[1]:

# Modified Stylesheet for notebook.
from IPython.core.display import HTML
def css_styling():
    styles = open("custom.css", "r").read()
    return HTML(styles)

css_styling()


# Out[1]:

#     <IPython.core.display.HTML at 0x2e48210>

# #Change Detection Tutorial
# ##Some Scaffolding
# 
# 
#  * Offline vs. Online change detection
#  * We write some utility functions that allow us to 
#   * pass signals to a change detection algorithm in "online" simulation mode
#   * calculate residuals after receiving each new data point
#   * Test the stopping rules at each iteration
#   * Plot results and output conveniently.
# 

# In[4]:

get_ipython().magic(u'matplotlib')
import matplotlib.pyplot as plt
import numpy as np


# Out[4]:

#     Using matplotlib backend: module://IPython.kernel.zmq.pylab.backend_inline
# 

# In[5]:

from collections import defaultdict
np.random.seed(seed=111111)
np.set_printoptions(precision=3, suppress=True)


# ## Aside: Offline vs. Online algorithms
# 
# An "offline" change detection algorithm is one in which we are given the entire signal and are attempting to "look back" and recognize where the change occcured. 
# 
# An "online" algorithm is quite different, in which we imagine our signal as "streaming into" our detector, and at any given moment we only have knowledge of the most recent data point and whatever information we chose to retain about the history of the signal. 
# 
# Reference: Sequential Analysis http://en.wikipedia.org/wiki/Sequential_analysis
# 
# My interest is in the latter "online" class of algorithms. That means I want to make sure data points are passed to the algorithm one by one, and that I am interested in 
# 
#   1. detecting a change, 
#   2. in deciding whether a change is significant enough to trigger an alert, and 
#   3. in how quickly I can detect the change after it occurs. 
# 
# I also want to make sure that I am not cheating when I run my experiments. 
# 
# To do all this, it is helpful to write some code that helps me simulate the online streaming scenario of interest. 

# ## Thus we need some Scaffolding
# 
# 
# I want to be able to realistically simulate streaming data for my online algorithm experiments. That is, I want to write code that simulates a scenario in which 
# 
#  * each data point is passed to the algorithm one by one
#  * the algorithm performs its analysis on that new information along with any stored historical information
#  * the algorithm decides after each data point whether or not a change has been detected. 
# 
# The following code will provide this framework and enable us to run some experiments more conveniently. Feel free to skip this section. 
# 
# 

# An online simulation function might look something like this: 
# ----------------------
# (pseudocode)
# 
# function online_simulator(signal, cd_algorithm, stopping rules): 
#   
#   Iterate through the signal, passing data points to the algorithm. FOR EACH data point
#     Calculate residuals
#     Compare residuals with the stopping rule(s)
#     IF the stopping rule is triggered
#       RETURN (True, residuals, stopping_rule_triggered)
# 
#   At the end of the signal, IF the stopping rule is not triggered
#      THEN return (False, residuals)
# 

# I am not clear on 'Essentially the algorithm is just calculating residuals and updating them for each new value passed.'
#  -- [Blaine]

# What about the change detection algorithm, what does that look like? 
# 
# Essentially the algorithm is just calculating residuals and updating them for each new value passed. 
# -------------------------
# (pseudocode)
# 
# class cd_algorithm:
#    Initialization
#       initialize residuals
# 
#    METHOD step FOR EACH new_signal_value
#       Update residuals
#       Check if Stopping Rules have been triggered
#       IF rules_triggered
#         RETURN (True, residuals, signal_size, stopping_rule_triggered)
#       
# ----
# actually we'll make that step method into a generator, so we can yield values for each new value of the signal.

# In[6]:

def dict_to_arrays(ddict):
    """
    Convenience function used by online simulator to bundle 
    residuals into a dict before returning
    """
    new_dict = {}
    for k,v in ddict.iteritems():
        new_dict[k] = np.array(v)
    return new_dict


# In[7]:

def online_simulator(signal, change_detector): 
    """
    Function that simulates an online streaming scenario for change detection experiments.
    --- 
    Given a signal and a change detector, this simulator passes one signal data point at a time to
    the change detector and processes the results. 
    """
    #Initiate
    #change_detector = cd_algorithm()
    
    all_residuals = defaultdict(list)
    
    xx = 0
    #Iterate through the signal, passing data points to the algorithm. 
    for value in signal: 
        
        #calculate residuals, compare residuals with the stopping rule(s)
        check_results = next(change_detector.step(value))
        
        #process results
        rule_triggered    = check_results[0]
        res               = check_results[1]
        
        #store residuals
        for k,v in res.iteritems():
            all_residuals[k].append(v)
              
        if rule_triggered == True: 
            #stopping rule was triggered          
            return (True, dict_to_arrays(all_residuals))    

    #Rule wasn't triggered by end of signal
    return (False, dict_to_arrays(all_residuals))


# What is the type/object of the signal that is being iterated over?
# -- [Blaine]

# In[8]:

def run_online_simulation(signal, change_detector, scale=True): 
    """Run simulation and print results"""
    
    #Run simulation
    results = online_simulator(signal, change_detector)
    
    #Display results
    print_sim_results(signal, results, scale=scale)
    
    #Return residuals
    residuals = results[1]
    return residuals


# In[9]:

class change_detector(object):
    """
    A change detection algorithm. 
    
    The algorithm calculates residuals and updates them for each new value passed. 
    Residuals are checked against stopping rules at each change, yielding either True or False, accordingly. 
    
    """
    
    def __init__(self): 
        #Interim and calculated values
        self.signal_size = 0
        self.total_val = 0
        
        self.mean_ = np.nan
    
    def update_residuals(self, new_signal_value): 
        #Update residuals
        self.signal_size += 1
        self.total_val += new_signal_value
        self.mean_ = self.total_val / self.signal_size
    
    def _get_residual_dict(self): 
        """create a dictionary of residuals to return. 
        Inclues all class and instance variables ending in '_'
        """
        residuals_dict = {}
        for k,v in self.__dict__.iteritems():
            if k.endswith('_'):
                residuals_dict[k] = v
        
        return residuals_dict
        
    def check_stopping_rules(self, new_signal_value): 
        rules_triggered = False
        
        #No rules implemented
        pass
        
        return rules_triggered
    
    def _step(self, new_signal_value): 
        
        #update residuals
        self.update_residuals(new_signal_value)
        
        ## compare residuals to stopping_rules
        rules_triggered = self.check_stopping_rules(new_signal_value)
        
        if rules_triggered: 
            yield (True, self._get_residual_dict())
        
        else: 
            yield (False, self._get_residual_dict())
      
    def step(self, new_signal_value):
        return self._step(new_signal_value)


# In[10]:

def print_sim_results(signal, results, **kwargs):
    """
    Another convenience function to print out the results of our experiment. 
    """
    #Get results
    stopped = results[0]
    residuals = results[1]
    print "Residuals: {}".format([res for res in residuals.viewkeys()])

    if stopped: 
        #length of residuals array tells us when the rule was triggered
        stop_point = len(residuals.itervalues().next())
          
        print "Change detected. Stopping Rule triggered at {}.\n".format(stop_point)
        plot_signal_and_residuals(signal, residuals, stop_point, **kwargs)
    else: 
        print "Stopping rule not triggered."
        plot_signal_and_residuals(signal, residuals, **kwargs)


# In[11]:

def plot_signal_and_residuals(signal, residuals=None, stop_point=None, scale=True):
    """Convenience function to generate plots of the signal and the residuals"""
    
    if residuals is None:
        plotcount = 1
    else: 
        plotcount = 1 + len(residuals)
    
    fig, axes = plt.subplots(nrows=plotcount, 
                             ncols = 1, 
                             sharex=True,
                             figsize=(6, plotcount*3)
                             )

    #First plot the signal
    if plotcount > 1: 
        ax = axes[0]
    elif plotcount == 1: 
        ax = axes
        
    ax.plot(signal)
    ax.set_title('Signal')
    
    #Scale signal
    ax.set_ylim(signal.min()*.5, signal.max()*1.5)
    ax.set_xlim(0, len(signal))
        
    #Plot a horizontal line where the stop_point is indicated
    if stop_point is not None: 
        assert (stop_point > 0) & (stop_point < len(signal))
        ax.vlines(x=stop_point, ymin=0, ymax=ax.get_ylim()[1], 
                  colors='r', linestyles='dotted')
    
    #Now plot each residual
    if residuals is not None: 
        for ii, (res_name, res_values) in enumerate(residuals.iteritems()):
            ax = axes[ii+1]
            ax.plot(res_values)
            ax.set_title("Residual #{}: {}".format(ii+1, res_name))
            if scale: 
                ax.set_ylim(res_values.min()*0.5, res_values.max() * 1.5)
            ax.vlines(x=stop_point, ymin=0, ymax=ax.get_ylim()[1], 
                      colors='r', linestyles='dotted')
        


# ## Demo the results

# In[16]:

"""
Uncomment the following code to output the demo.
"""

'''
sig1 = np.ones(1000)
sig1[:500] = sig1[:500] * 50
sig1[500:] = sig1[500:] * 40

blank_detector = change_detector()
residuals = run_online_simulation(sig1, blank_detector)
'''


# Out[16]:

#     '\nsig1 = np.ones(1000)\nsig1[:500] = sig1[:500] * 50\nsig1[500:] = sig1[500:] * 40\n\nblank_detector = change_detector()\nresiduals = run_online_simulation(sig1, blank_detector)\n'

# (Note that the stopping rule will not be triggered, because we haven't created a stopping rule yet.)

# ### Convert to ipynb
# Convert this ipynb to python file so we can import it from other notebooks in the tutorial

# In[28]:

if __name__ == "__main__": 
    get_ipython().system(u'ipython nbconvert --to python scaffolding.ipynb')


# Out[28]:

#     [NbConvertApp] Using existing profile dir: u'/home/aman/.config/ipython/profile_default'
#     [NbConvertApp] Converting notebook scaffolding.ipynb to python
#     [NbConvertApp] Support files will be in scaffolding_files/
#     [NbConvertApp] Loaded template python.tpl
#     [NbConvertApp] Writing 11152 bytes to scaffolding.py
# 

# In[29]:

print "NAME: :",  __name__


# Out[29]:

#     NAME: : __main__
# 

# In[ ]:



