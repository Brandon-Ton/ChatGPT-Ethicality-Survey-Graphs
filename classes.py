#this file contains two classes

class response:
  def __init__(self, line): #each response object is a list of one respondent's answer to each question 
    self.line = line

  def getAnswer(self, question): #returns the respondent's answer to the target question
    return (self.line[question])

  @staticmethod 
  #returns list of every respondent's answer to a question who answered filterQuestion with filterAnswer
  def getAnswers(responses, question, filterQuestion=None, filterAnswer=None):
    output = []
    if filterQuestion != None: #by default with no filter
      for entry in responses:
        if entry.getAnswer(filterQuestion) == filterAnswer:
          output.append(int(entry.getAnswer(question)))
    else:
      for entry in responses: #only returns the answers to those who answered filterQuestion with filterAnswer
        output.append(int(entry.getAnswer(question)))

    return output


class statistics: #useful metrics for analysis
  @staticmethod
  def getMean(list): #calculates the mean
      total = 0
      for i in list:
        total += i
      mean = total / len(list)
      return mean

  @staticmethod
  def getMedian(list): #calculates the median
    list = sorted(list)
    index = -0.5 + len(list)/2
    if(index) % 2 == 0:
      return list[index]
    else:
      return (list[int(index-0.5)] + list[int(index-0.5)])/2

  @staticmethod
  def getStd(list): #calculates std for a SAMPLE not for a population
    mean = statistics.getMean(list)
    total = 0
    for i in list:
      total += (i - mean)**2
    std = (total / (len(list)-1))**0.5
    return std
