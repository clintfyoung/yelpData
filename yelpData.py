import json
import math
import numpy as np
import matplotlib.pyplot as plt

REarth = 6371. #Earth radius in kilometers

#Ranges of latitudes and longitudes of Las Vegas, unfortunately a city I know little about:
minLong = -115.55
maxLong = -114.9
minLat = 35.95
maxLat = 36.4

NLong = 20
NLat  = 10

dLat = (maxLat-minLat)/NLat
dLong = (maxLong-minLong)/NLong

#This will make a heat map of the reviews of restaurants:
starsFastFood = [[0. for i in range(0, NLong)] for j in range(0, NLat)]
numberOfReviewsFastFood = [[0. for i in range(0, NLong)] for j in range(0, NLat)]


def binRestaurant(lat, longitude, stars, reviews):
    latBin = int(math.floor((lat-minLat)/dLat))
    longBin = int(math.floor((longitude-minLong)/dLong))

    if (latBin>=0 and longBin>=0 and latBin<NLat and longBin<NLong):
        starsFastFood[latBin][longBin] += stars*reviews
        numberOfReviewsFastFood[latBin][longBin] += reviews

    return


counter = 0
businesses = open("yelp_academic_dataset_business.json", 'rb')
for line in businesses:
    counter += 1
    jsonLine = json.loads(line)

    if "Fast Food" in jsonLine['categories']:
        latitude = float(jsonLine['latitude'])
        longitude = float(jsonLine['longitude'])
        stars = float(jsonLine['stars'])
        reviews = float(jsonLine['review_count'])
        binRestaurant(latitude, longitude, stars, reviews)

weightedAverageOfReviewsFastFood = [['null' for j in range(NLong)] for i in range(NLat)]
for i in range(NLat):
    for j in range(NLong):
        if numberOfReviewsFastFood[i][j]>0.:
            weightedAverageOfReviewsFastFood[i][j] = starsFastFood[i][j]/numberOfReviewsFastFood[i][j]

nonzeroReviews = []

#For sorting:
def lastElement(s):
    return s[-1]

for i in range(NLat):
    for j in range(NLong):
        if weightedAverageOfReviewsFastFood[i][j] != 'null':
            nonzeroReviews.append([minLat+(i+0.5)*dLat, minLong+(j+0.5)*dLong, numberOfReviewsFastFood[i][j], weightedAverageOfReviewsFastFood[i][j]])

sortedReviews = sorted(nonzeroReviews, key=lastElement)
#print sortedReviews

N = len(sortedReviews)/20 #Only a sample of the average reviews
averageReviews = []
timesReviewed = []
latAndLong = []
for i in range(N):
    averageReviews.append(sortedReviews[20*i+18][3])
    timesReviewed.append(sortedReviews[20*i+18][2]/20.)
    latAndLong.append(str(sortedReviews[20*i+18][0])+", "+str(sortedReviews[20*i][1]))

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, averageReviews, width, color='r')
rects2 = ax.bar(ind + width, timesReviewed, width, color='b')

# add some text for labels, title and axes ticks
ax.set_ylabel('Stars')
ax.set_xlabel('Latitude, Longitude')
ax.set_title('Stars and times reviewed')
ax.set_xticks(ind + width)
ax.set_xticklabels(latAndLong)

ax.legend((rects1[0], rects2[0]), ('Stars', 'Times reviewed/20'))


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % height,
                ha='center', va='bottom')

#autolabel(rects1)
#autolabel(rects2)

plt.show()

counter = 0.
bestCounter = 0.
worstCounter = 0.
businesses = open("yelp_academic_dataset_review.json", 'rb')
for line in businesses:
    counter += 1.
    jsonLine = json.loads(line)

    if 'best' in jsonLine['text']: bestCounter += 1.
    elif 'Best' in jsonLine['text']: bestCounter += 1.
    if 'worst' in jsonLine['text']: worstCounter += 1.
    elif 'Worst' in jsonLine['text']: worstCounter += 1.

print "The fraction of reviews containing the word 'best' =", bestCounter/counter
print "The fraction of reviews containing the word 'worst' =", worstCounter/counter
