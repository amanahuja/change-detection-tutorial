import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


class BlankDetector(object):
    """
    This is a very simple detector which we look at in
    Section 00 (Introduction) of this tutorial. This serves as a
    good skeleton on how to override the methods of our base
    ChangeDetector class.
    """
    def __init__(self):
        super(BlankDetector, self).__init__()
        # Initialize all variables needed here
        self.total_val = 0

        # Initialize residuals here.
        #   All attributes ending with underscore '_' are treated
        #   as residuals.
        self.mean_ = np.nan

    def update_residuals(self, new_signal_value):
        """This method is called for every new signal value.
        Use this space to update variables and residuals"""
        self._update_base_residuals(new_signal_value)

        # Update your attributes here
        self.total_val += new_signal_value

        # Update your residuals here
        #  Here's an example residual that calculates mean
        self.mean_ = self.total_val / self.signal_size

    def check_stopping_rules(self, new_signal_value):
        """This method is called for every new signal value,
        AFTER the attributes and residuals have been updated.
        Use this space to check if a stopping rule has been
        triggered. Set self.rules_triggered to True or False
        accordingly."""
        self.rules_triggered = False


class ChangeDetector(object):
    """
    A change detection algorithm.

    The algorithm calculates residuals and updates them for each new value
    passed. Residuals are checked against stopping rules at each change,
    yielding either True or False, accordingly.
    """

    def __init__(self):
        self.rules_triggered = False
        # Interim and calculated values
        self.signal_size = 0

        # Residuals
        #   All attributes ending in underscore (_) are treated as
        #   residual values (for plotting, printing, etc)
        #   e.g. self.mean_ = np.nan
        pass

    def update_residuals(self, new_signal_value):
        """
        Updates residuals.
        Override this method when writing your own change detector based on
        this class.
        """
        self._update_base_residuals(new_signal_value)
        # Update your residuals here
        pass

    def check_stopping_rules(self, new_signal_value):
        """
        Check Stopping Rules.
        Override this method when writing your own change detector based on
        this class
        """
        # Implemente your stopping rules here
        # Set self.rules_triggered to True when triggered
        pass

    """
    Internal methods
    -------------------
    leave the following methods alone. You should only need to override or edit
    above this line in order to implement your own change detector.
    """

    @property
    def residuals_(self):
        return self._get_residual_dict()

    def _update_base_residuals(self, x):
        """
        Input
         x: scalar, float.
            is the new signal value obtained for this step.
        Base residuals
         k: int
            the total signal size seen so far.
            TEMP: Currently called signal_size for clarity
        """
        # We'll always use these
        self.signal_size += 1

    def _get_residual_dict(self):
        """create a dictionary of residuals to return.
        Inclues all class and instance variables ending in '_'
        """
        residuals_dict = {}
        for k, v in self.__dict__.iteritems():
            if k.endswith('_'):
                residuals_dict[k] = v

        return residuals_dict

    def _step(self, new_signal_value):
        """Internal method to "step", digest one new signal point."""

        # Update residuals
        self.update_residuals(new_signal_value)

        # Compare residuals to stopping_rules
        self.check_stopping_rules(new_signal_value)

        yield self._get_residual_dict()

    def step(self, new_signal_value):
        return self._step(new_signal_value)

    def __repr__(self):
        return "Change Detector(triggered={}, residuals={})".format(
            self.rules_triggered,
            self.residuals_
            )

    def run(self, signal, plot=True, **kwargs):
        """
        Function that simulates an online streaming scenario for change
        detection experiments.

        Given a signal and a change detector, this simulator passes one signal
        data point at a time to the change detector and processes the results.

        inputs
        ------------------------
        signal: np.array
        change_detector: class change_detector
        """

        # Run simulation
        all_residuals = defaultdict(list)
        for value in signal:
            # Step to get residuals and check stopping rules
            res = next(self.step(value))

            # Store all residuals for printing only
            for k, v in res.iteritems():
                all_residuals[k].append(v)

            if self.rules_triggered is True:
                break

        def dict_to_arrays(ddict):
            """Convenience func to bundle residuals into a dict"""
            new_dict = {}
            for k, v in ddict.iteritems():
                new_dict[k] = np.array(v)
            return new_dict

        residuals = dict_to_arrays(all_residuals)

        # Display results
        if plot is True:
            self.print_sim_results(signal, residuals, **kwargs)

        return self.rules_triggered

    def print_sim_results(self, signal, all_residuals, signal_name='Signal'):
        """Print out the results of our experiment. """

        print "Residuals: {}".format([res for res in all_residuals.viewkeys()])

        # Print results
        if self.rules_triggered is True:
            # Length of any residual array tells us when the rule was triggered
            some_res = all_residuals.itervalues().next()
            stop_point = len(some_res)
            # Quick sanity check
            assert (stop_point > 0) & (stop_point <= len(signal))
            print "Change detected. Stopping Rule triggered at {}.\n".format(
                stop_point)
        else:
            stop_point = None
            print "Stopping rule not triggered."

        # Generate axes to plot signal and residuals"""
        plotcount = 1 + len(all_residuals)
        fig, axes = plt.subplots(nrows=plotcount, ncols=1, sharex=True,
                                 figsize=(12, plotcount*3))

        # Plot the signal
        if plotcount > 1:
            ax = axes[0]
        elif plotcount == 1:
            ax = axes

        ax.plot(signal, 'b.')
        ax.plot(signal, 'b-', alpha=0.15)
        ax.set_title(signal_name)

        # Scale signal
        ax.set_ylim(signal.min()*.5, signal.max()*1.5)
        ax.set_xlim(0, len(signal))

        # Plot a horizontal line where the stop_point is indicated
        if self.rules_triggered is True:
            ax.vlines(x=stop_point, ymin=0, ymax=ax.get_ylim()[1],
                      colors='r', linestyles='dotted')

        # Plot each residual
        for ii, (res_name, res_values) in enumerate(all_residuals.iteritems()):
            ax = axes[ii+1]
            ax.plot(res_values, 'g.', alpha=0.7)
            ax.set_title("Residual #{}: {}".format(ii+1, res_name))
            ax.set_ylim(res_values.min()*0.5, res_values.max() * 1.5)
            if stop_point is not None:
                ax.vlines(x=stop_point, ymin=0, ymax=ax.get_ylim()[1],
                          colors='r', linestyles='dotted')
