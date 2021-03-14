# SYSC4005-Project
GitHub Link: https://github.com/sarahlamonica/SYSC4005-Project/

Milestone2.xlsx contains distributions of each set of data and evaluation of the identified distributions with Q-Q plots, and chisquare goodness-of- fit test. From the histograms of the given data sets, an exponential distribution was found to be acceptable using chi-square tests and Q-Q plots. 

Data collection and input modeling is done using scripts in the Simulation folder.The inputmodel.py code takes in the .dat files as input and reads the numbers into a list. Then, the random number is generated by the calculate_pdf_list() function which takes the data and uses the numpy.random.exponential function to calculate the drawn samples from the exponential distribution using the mean which is calculated by taking the average of all of the data. 

