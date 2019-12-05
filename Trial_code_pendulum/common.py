
from random import randint
import time

# for live plot 
import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation


class PID:
    """
    The PID controller for the inverted pendulum
    """

    def __init__(self,kp, kd, ki):
        """
        Initialising the PID variables

        :param kp: (int) Proportional Kp constant
        :param kd: (int) Derivative Kd Constant
        :param ki: (int) Integral Ki Constant

        """
        self.pid_i = 0 
        self.pid_d = 0
        self.pid_p = 0
        # PID constants
        self.kp = kp
        self.kd = kd
        self.ki = ki
        # Errors
        self.previous_error = 0 
        self.error = 0 
        self.pid = 0 

        # time variables
        self.elapsed_time = 0
        self.time_now = time.perf_counter()
        self.time_prev = 0

        # Values
        self.desired_value = 0
        self.measured_value = 0

    def run(self,desired_value = 0, measured_value = 0):
        """
        Computing the PID controller 

        :param desired_value: (int) desired_value = 0 by default
        :param measured_value: (int) measured_value = 0 by default

        :return: (int) pid controller output value

        """
        self.desired_value = desired_value
        self.measured_value = measured_value
        # the previous time is stored before the actual time read
        self.time_prev = self.time_now
        # actual time read
        self.time_now = time.perf_counter()
        # The elapsed_time is the time that elapsed since the previous loop
        self.elapsed_time = (self.time_now - self.time_prev)
        # calculate the error between the desired value and the real measured value
        self.error = self.measured_value - self.desired_value
        # proportional value of the PID is just a proportional constant multiplied by the error
        self.pid_p = self.kp*self.error

        # To integrate we just sum the previous integral value with the error multiplied by  the integral constant. 
        # This will integrate (increase) the value each loop till we reach the 0 point
        self.pid_i = self.pid_i +(self.ki*self.error)

        # For taht we will use a variable called previous_error. We substract that value from the actual error and divide all by the elapsed time. 
        # Finnaly we multiply the result by the derivate constant
        self.pid_d = self.kd*((self.error - self.previous_error)/self.elapsed_time) 

        # The final PID values is the sum of each of this 3 parts
        self.pid = self.pid_p + self.pid_i + self.pid_d
        
        # Setting the min and max value of the controller to 0 and 2000 mBar
        if self.pid < 0 :
            self.pid = 0
        if self.pid > 2000 :
            self.pid = 2000

        # Remember to store the previuos error 
        self.previous_error = self.error

        return self.pid





def main():
    """
    An example of the use of the PID class with live plot on Matplotlib

    """

    plt.style.use( 'fivethirtyeight')
    x_vals = []
    y_vals = []
    pid_vals = []
    controller = PID(10,0,0)

    index = count()

    # animate(i, x_vals,y_vals,index)
    def animate(i):
        # data = pd.read_csv('test.csv')
        # x = data['Pressure1']
        # y1 = data['Sensor4']
        # y2 =data['Sensor3']
        x_vals.append(next(index))
        value_ = randint(0,15)
        y_vals.append(value_)
        pid_value = controller.run(0,value_)
        pid_vals.append(pid_value)
        # x_vals.append(next(index))
        # y_vals.append(randint(0,5))

        plt.cla()
        
        plt.plot(x_vals , y_vals , label='Sensor')
        plt.plot(x_vals , pid_vals, label='pid')

        plt.legend(loc= 'upper left')
        plt.tight_layout()


    ani = FuncAnimation(plt.gcf(), animate,interval=1000)


    plt.show()

if __name__ == "__main__":
    main()