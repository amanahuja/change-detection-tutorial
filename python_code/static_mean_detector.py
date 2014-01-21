# coding: utf-8
class cd_static_mean_detector(change_detector):
    """
    A change detection algorithm. 
    
    The algorithm calculates residuals and updates them for each new value passed. 
    Residuals are checked against stopping rules at each change, yielding either True or False, accordingly. 
    
    """
    
    def __init__(self, threshold=0.05): 
        #hyper-parameter(s)
        self.threshold = threshold
            
        #Interim and calculated values
        self.signal_size = 0
        self.total_val = 0
        
        #... and residuals
        self.diff_ = np.nan #np.zeros(1)
        self.mean_ = np.nan #np.zeros(1)
    
    def update_residuals(self, new_signal_value): 
        #Update residuals 
        self.signal_size += 1
        self.total_val += new_signal_value
        self.mean_ = self.total_val / self.signal_size
        self.diff_ = np.absolute(self.mean_ - new_signal_value)
    
    def check_stopping_rules(self, new_signal_value): 
        rules_triggered = False
        #check if new value is more than % different from mean
        threshold_level = self.mean_ * self.threshold
        
        if self.diff_ > threshold_level:
            #import pdb; pdb.set_trace();
            rules_triggered = True
        return rules_triggered
          
    def step(self, new_signal_value):
        return self._step(new_signal_value)
