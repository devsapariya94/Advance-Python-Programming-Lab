from os import listdir

global valid_reviews
valid_reviews = 0
global invalid_reviews
invalid_reviews = 0


global product_rating
product_rating = {}


def isdate(date):
    try:
        year, month, day = date.split('-')
        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            return True
        if int(month) < 1 or int(month) > 12:
            return True
        if int(day) < 1 or int(day) > 31:
            return True
        return False
    except:
        return True

def check_valid(one_file):
    global valid_reviews, invalid_reviews 
    with open(one_file, "r") as f:
        for line in f:
            review = [word.strip() for word in line.split(",")]
            if len(review) != 5:
                invalid_reviews += 1
                continue
            if len(review[0]) != 6:
                invalid_reviews += 1
                continue
            if len(review[1]) != 10:
                invalid_reviews += 1
                continue
            if isdate(review[2]):
                invalid_reviews += 1
                continue
            if int(review[3]) < 1 or int(review[3]) > 5:
                invalid_reviews += 1
                continue
            if len(review[4]) < 1:
                invalid_reviews += 1
                continue
            valid_reviews += 1

            if review[1] not in product_rating:
               product_rating[review[1]] = [[],[],[],[],0]
            
            tempconst = product_rating[review[1]][0]
            tempdate = product_rating[review[1]][1]
            tempstar = product_rating[review[1]][2]
            tempword = product_rating[review[1]][3]
            tempavgrating = product_rating[review[1]][4]

            tempconst.append(review[0])
            tempdate.append(review[2])
            tempstar.append(review[3])
            tempword.append(review[4])
            tempavgrating = (tempavgrating * (len(tempconst) - 1) + int(review[3])) / len(tempconst)
            product_rating[review[1]] = [tempconst, tempdate, tempstar, tempword, tempavgrating]

review_path = 'Reviews/'
allfiles = [f for f in listdir(review_path)]
for one_file in allfiles:
    one_file = review_path + one_file
    check_valid(one_file)

print("Total valid reviews: ", valid_reviews)
print("Total invalid reviews: ", invalid_reviews)
print("Total products: ", len(product_rating))


sorted_product_rating = sorted(product_rating.items(), key=lambda x: x[1][4], reverse=True)

print("Top 3 products with its avarage rating: " )
for i in range (3):
    print(sorted_product_rating[i][0], sorted_product_rating[i][1][4])



with open ("summarry.txt", "w") as f:
    f.write("Total valid reviews: " + str(valid_reviews+invalid_reviews) + "\n")
    f.write("Total valid reviews: " + str(valid_reviews) + "\n")
    f.write("Total invalid reviews: " + str(invalid_reviews) + "\n")
    f.write("Total products: " + str(len(product_rating)) + "\n")
    f.write("Top 3 products with its avarage rating: " + "\n")
    for i in range (3):
        f.write(sorted_product_rating[i][0] + " " + str(sorted_product_rating[i][1][4]) + "\n")
        