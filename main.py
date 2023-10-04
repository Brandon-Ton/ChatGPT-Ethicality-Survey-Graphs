import matplotlib.pyplot as plt #uses this library to construct graphs
import csv #uses this library to readd csv file of the survey
import numpy as np
import classes #custom class in seperate file with two classes

'''
  Questions of the Survey
  Q0. What Is your Age?
  Q1. What is your gender?
  Q2. What is your Ethnicity?
  Q3. Employment Status
  Q4. What Faculty Are You Part of?
  Q5. How much do you know about ChatPT?
  Q6. How often do you use ChatGPT?
  Q7. How do you think ChatGPT will affect the learning process at post-secondary schools?
  Q8. ChatGPT has potential for misuse with malicious intent. How necessary do you think censorship is for ChatGPT?
  Q9. All ChatGPT generated text should be 'watermarked'
  Q10. For what do you think the use of ChatGPT counts as plagiarism? Check all that apply.
  Q11. ChatGPT should be incorporated into the post-secondary curriculum.
'''

responses = [] #list of response objects
#list of pruned lists of possible answers to demographic questions #0-5
answers = [["< 18", "18 - 24", "25 - 34", "35 - 44", "45 - 54", "55+"],
           ["Male", "Female", "Non - Binary", "Prefer not to say"],
           ["White / Caucasian", "Black / African American", "Arab / Middle Eastern", "Hispanic / Latino", "Asian", "Prefer not to say"],
           ["Full-time student", "Employed part-time", "Unemployed", "Retired"],
           ["Faculty of Engineering and Architectural Sciences", "Faculty of Science", "Faculty of Business", "N/A"], 
           [1, 2, 3, 4, 5, 6, 7, 8, 9]  ]

#function for opening csv file and storing each response into a response object
def read_csv():
  with open('ChatGPT Ethicality Survey.csv') as csv_file: #opens file results
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    line = []

    for row in csv_reader:
      for i in range(1, len(row)):  #ignores timestamp of each response
        if line_count != 0: #skips line of questions that are not responses
          line.append(row[i]) #

      if line_count != 0: #skips line of questions
        obj = classes.response(line) #creates response object
        responses.append(obj) #adds the new response to the list of responses
      line = [] #clears variable for next loop
      line_count += 1

#function for creating a scatterplot with Q5(The only linear-scale demographic question) for the x-axis
def scatterplot(question, title="", x_axis="Knowledge of ChatGPT", y_axis=""):

  x = classes.response.getAnswers(responses, 5) #list of answers to Q5
  y = classes.response.getAnswers(responses, question) #list of answers to the input question
  dict = {} #to tally overlapping points
  size = [] #size of the point based on number of overlapping points

  #prints statistics to console
  print("The mean is", classes.statistics.getMean(y))
  print("The median is", classes.statistics.getMedian(y))
  print("The std is", classes.statistics.getStd(y))

  for index in range(len(x)): #tallies up overlapping points up in dict
    i = x[index]
    j = y[index]
    if ((i, j) not in dict):
      dict[(i, j)] = 0
    dict[(i, j)] += 1

  x = [] #clear variables for reuse as axis labels
  y = []

  for point in dict: #dictionary of 2 ordered tuples
    x.append(point[0]) #list of x coordinates of each point
    y.append(point[1]) #list of y coordinates of each point
    size.append(30 * (dict[point])) #list of appropriate sizes for each point

  #construct plot
  plt.scatter(x, y, s=size)
  plt.title(title)
  plt.ylabel(y_axis)
  plt.xlabel(x_axis)
  plt.show()

#function for creating a boxplot for visualizing demographical impact of filterQuestion on question
def boxplot(question, filterQuestion, title="", x_axis="", y_axis="", setX_Label=None, figsize=(11,4), fontsize=8):
  
  data = []
  labels = answers[filterQuestion] #default x-axis labels are the possible answers
  if setX_Label != None: #customize x-axis label
    labels = setX_Label
  
  
  for answer in answers[filterQuestion]: #fills out data with responses filtered with each possible answer
    #appends list of answers to input question that replied to filterQuestion with the current answer
    data.append(classes.response.getAnswers(responses, question, filterQuestion, answer))

  #construct graph
  plt.rcParams.update({'font.size': fontsize})
  plt.figure(figsize=figsize)
  plt.boxplot(data, labels=labels)
  plt.title(title)
  plt.ylabel(y_axis)
  plt.xlabel(x_axis)
  plt.show()

#function for creating a quantity barchart (like a histogram) for non-demographical questions
def barchart(question, filterQuestion=None, filterAnswer=None, title="", x_axis="", y_axis=""):
  
  entries = classes.response.getAnswers(responses, question, filterQuestion, filterAnswer) #list of answers of those who answered with the filterAnswer to the filterQuestion
  x = ['1', '2', '3', '4', '5', '6', '7', '8', '9'] #x-axis label is always this
  y = []
  dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0} #for tallying

  #prints statistics to console
  print("The mean is", classes.statistics.getMean(entries))
  print("The median is", classes.statistics.getMedian(entries))
  print("The std is", classes.statistics.getStd(entries))
  
  for index in range(len(entries)): #tallies the answers
    i = entries[index]
    if (i not in dict):
      dict[i] = 0
    dict[i] += 1 #MAKE SURE NOT IN UNDER THE IF STATEMENT!!!
  
  for v in dict: #appends the values to list y
    y.append(dict[v])

  #constructs chart
  plt.bar(x, y)
  plt.title(title)
  plt.ylabel(y_axis)
  plt.xlabel(x_axis)
  plt.show()
  
#function for creating horizontal barcharts for Q10 (the only multiselect question)
def HBarchart(question, filterQuestion=None, filterAnswer=None, x_axis="", y_axis=""):

  #pruned list possible answers to Q10
  Q10Answers = ["For Generating Ideas", "For Essays", "For Homework (for completion mark)", "For Computer Code", "For Feedback"]
  
  dict = {x: 0 for x in Q10Answers} #sets values as 0 for each of the keys
  count = 0 #a count of the number of responses that passed the filter to get % of respondents
  
  for response in responses:
    multipleAnswers = response.getAnswer(question).split(";") #splits input string into array, each respondent can choose more than 1 answer
    once = 1 #to help count number of respondents passing filter
    for answer in multipleAnswers:
      if answer in Q10Answers:
        if filterQuestion == None or filterAnswer == response.getAnswer(filterQuestion): #checks if the respondent is part of the target demographic
          dict[answer] += 1 #tally the result in dictionary
          count += once
          once = 0
  
  y = dict.keys()
  x = dict.values()
  temp = [] #to help set x to % of demographic

  #sets x to % of demographic
  for value in x:
    temp.append(100*value/count)
  x = temp

  #constructs graph
  plt.rcdefaults()
  y_pos = np.arange(len(y))
  plt.barh(y_pos, x, align='center')
  plt.yticks(y_pos, labels=y)
  plt.xlabel(x_axis)
  plt.title(y_axis)
  
  plt.show()
  
#function for creating a pie chart for the demographical questions
def piechart(question, title="", x_axis="", y_axis=""):
  #Unpruned possible answers
  pieAnswers = [["< 18", "18 - 24", "25 - 34", "35 - 44", "45 - 54", "55+"], #Q0
           ["Male", "Female", "Non - Binary", "Prefer not to say"], #Q1
           ["White / Caucasian", "Black / African American", #Q2
             "Arab / Middle Eastern", "Hispanic / Latino", "Asian",
             "Native American", "Other", "Prefer not to say"],
           ["Full-time student", "Employed full-time", "Employed part-time", #Q3
             "Self-employed", "Unemployed", "Retired"],
           ["Faculty of Arts", "Faculty of Community Services", #Q4
             "Faculty of Engineering and Architectural Sciences",
             "Faculty of Law", "Faculty of Science",
             "Faculty of Communication and Design", "Faculty of Business",
             "N/A"], 
           [1, 2, 3, 4, 5, 6, 7, 8, 9]  ] #Q5
  
  # Tally the possible answers
  dict = {x: 0 for x in pieAnswers[question]}
  for i in responses:
    if i.getAnswer(question) in pieAnswers[question]:
      dict[i.getAnswer(question)] += 1

  # Create the pie chart with labels and percentages
  fig, ax = plt.subplots()
  #checks if the percentage is greater than 0
  def my_autopct(num):
    if (num > 0):
      return ('%.2f%%' % num)
    else: ''
  
  #plots the point
  ax.pie(dict.values(), autopct=my_autopct)
  #Creates the labels that are non-zero
  non_zero_labels = [label for label, value in dict.items()   if value > 0]
  non_zero_values = [value for value in dict.values() if value > 0]
  ax.pie(non_zero_values, labels=non_zero_labels, autopct=my_autopct, labeldistance=1.1)
  
  # Set chart title and axis labels
  plt.title(title)
  plt.xlabel(x_axis)
  plt.ylabel(y_axis)
  plt.show()


def showFigure(figureNum):
  match figureNum:
    case 1:
      piechart(0, title="Age of Respondents")
    case 2:
      piechart(1, title="Gender of Respondents")
    case 3:
      boxplot(6, 1, x_axis="Respondent Gender", y_axis="Usage Frequency", title="Relationship of Gender and ChatGPT Usage Frequency")
    case 4:
      HBarchart(10, filterQuestion=1, filterAnswer="Male", x_axis="Percentage of Male Respondents", y_axis="ChatGPT Uses Male Respondents Consider as Plagiarism")
    case 5:
      HBarchart(10, filterQuestion=1, filterAnswer="Female", x_axis="Percentage of Female Respondents", y_axis="ChatGPT Uses Female Respondents Consider as Plagiarism")
    case 6:
      piechart(2, title="Ethnicity of Respondents")
    case 7:
      boxplot(6, 2, x_axis="Respondent Ethnicity", y_axis="Usage Frequency", title="Relationship of Ethnicity and ChatGPT Usage Frequency")
    case 8:
      boxplot(8, 2, x_axis="Respondent Ethnicity", y_axis="Agreeance of The Necessity of Cencorship", title="Relationship of Ethnicity and Opinion on The Necessity of Censorship for ChatGPT")
    case 9:
      boxplot(9, 2, x_axis="Respondent Ethnicity", y_axis="Agreeance With Watermarking", title="Relationship of Ethnicity and Opinion that ChatGPT Should be Watermarked")
    case 10:
      HBarchart(10, filterQuestion=2, filterAnswer="White / Caucasian", x_axis="Percentage of White Respondents", y_axis="ChatGPT Uses White Respondents Consider as Plagiarism")
    case 11:
      HBarchart(10, filterQuestion=2, filterAnswer="Asian", x_axis="Percentage of Asian Respondents", y_axis="ChatGPT Uses Asian Respondents Consider as Plagiarism")
    case 12:
      HBarchart(10, filterQuestion=2, filterAnswer="Arab / Middle Eastern", x_axis="Percentage of Middle Eastern Respondents", y_axis="ChatGPT Uses Arab/Middle Eastern Respondents Consider as Plagiarism")
    case 13:
      piechart(3, title="Employment Status of Respondents")
    case 14:
      boxplot(9, 3, x_axis="Respondent Employment Status", y_axis="Agreeance With Watermarking", title="Relationship of Employment Status and Opinion that ChatGPT Should be Watermarked")
    case 15:
      boxplot(11, 3, x_axis="Respondent Employment Status", y_axis="Agreeance on Incorporation", title="Relationship of Employment Status and Opinion that ChatGPT Should be Incorporated into The Curriculum")
    case 16:
      HBarchart(10, filterQuestion=3, filterAnswer="Full-time student", x_axis="Percentage of Full-time Students", y_axis="ChatGPT Uses Full-time Students Consider as Plagiarism")
    case 17:
      HBarchart(10, filterQuestion=3, filterAnswer="Employed part-time", x_axis="Percentage of Part-time Workers", y_axis="ChatGPT Uses Part-time Workers Consider as Plagiarism")
    case 18:
      HBarchart(10, filterQuestion=3, filterAnswer="Unemployed", x_axis="Percentage of Unemployed Respondents", y_axis="ChatGPT Uses Unemployed Respondents Consider as Plagiarism")
    case 19:
      piechart(4, title="Faculty of Respondents")
    case 20:
      boxplot(7, 4, x_axis="Respondent Faculty", y_axis="Respondent's View of ChatGPT's Positiveness", title="Relationship of Respondent's Faculty and Opinion on The Positiveness of ChatGPT's Impact on The Learning Process")
    case 21:
      boxplot(8, 4, x_axis="Respondent Faculty", y_axis="Agreeance of The Necessity of Cencorship", title="Relationship of Respondent's Faculty and Opinion on The Necessity of Censorship for ChatGPT")
    case 22:
      HBarchart(10, filterQuestion=4, filterAnswer="Faculty of Science", x_axis="Percentage of Faculty of Science Respondents", y_axis="ChatGPT Uses Faculty of Science Respondents Consider as Plagiarism")
    case 23:
      HBarchart(10, filterQuestion=4, filterAnswer="Faculty of Business", x_axis="Percentage of Faculty of Business Respondents", y_axis="ChatGPT Uses Faculty of Business Respondents Consider as Plagiarism")
    case 24:
      HBarchart(10, filterQuestion=4, filterAnswer="Faculty of Engineering and Architectural Sciences", x_axis="Percentage of Faculty of Eng. & Arch. Sci. Respondents", y_axis="ChatGPT Uses Faculty of Engineering and Architectural\n Sciences Respondents Consider as Plagiarism")
    case 25:
      scatterplot(6, title="Relationship of Knowledge of ChatGPT and Usage Frequency", y_axis="Usage Frequency")
    case 26:
      scatterplot(7, title="Relationship of Knowledge of ChatGPT and Opinion on The\n Positiveness of ChatGPT's Impact on The Learning Process", y_axis="Respondent's View of ChatGPT's Positiveness")
    case 27:
      barchart(6, title="How Often Respondents Use ChatGPT", x_axis="Usage Frequency", y_axis="Number of Respondents")
    case 28:
      barchart(7, title="How Respondents Think ChatGPT Will Affect The Learning Process", x_axis="Respondent's View of ChatGPT's Positiveness", y_axis="Number of Respondents")
    case 29:
      barchart(8, title="Respondents' Opinion on The Necessity of Censorship for ChatGPT", x_axis="Agreeance of The Necessity of Censorship", y_axis="Number of Respondents")
    case 30:
      barchart(9, title="Respondents' Opinion On Watermarking ChatGPT", x_axis="Agreeance With Watermarking", y_axis="Number of Respondents")
    case 31:
      barchart(11, title="Respondents' Opinion On Incorporating ChatGPT Into The Curriculum", x_axis="Agreeance With Incorporation", y_axis="Number of Respondents")
    case 32:
      HBarchart(10, x_axis="Percentage of Respondents", y_axis="ChatGPT Uses Respondents Consider as Plagiarism")
    case 33:
      print("This Figure is made in a text editor")
    case _: #default
      print("Figure does not exist")
      
'''
* Functions are called below *
'''

if __name__ == "__main__":
  read_csv() #file is read and responses stored
  showFigure(25) #Displays the selected figure for Figures 1-32
