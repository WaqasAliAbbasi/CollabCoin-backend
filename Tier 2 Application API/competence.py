from blockchain import get_order_details, get_all_assets
import random, math


def competence():
    initial_val = get_all_assets()
    total = {}
    count = {}
    for i in initial_val:
        if i['data']['deal']['transactionAmount'] > 0:
            original_purchase = -1*get_order_details(i['data']['deal']['txID'])[2]
            if i['data']['deal']['playerID'] not in total:
                total[i['data']['deal']['playerID']] = i['data']['deal']['transactionAmount']/original_purchase
                count[i['data']['deal']['playerID']] = 1
            else:
                total[i['data']['deal']['playerID']] += i['data']['deal']['transactionAmount']/original_purchase
                count[i['data']['deal']['playerID']] += 1

    for k in total:
        total[k] = round(total[k]/count[k],2)
    s = [(k, total[k]) for k in sorted(total, key=total.get, reverse=True)]
    sorted_total = {}
    print("Competence:")
    count = 0
    for k, v in s:
        count += 1
        sorted_total[k] = v
        print(str(count) + ": " + str(k) + ": " + str(sorted_total[k]))
    return sorted_total

total = competence()
money_division = []
actual_division = []
for i in total:
    money_division.append(len(money_division))
    actual_division.append(0)


def divide(capital,money_division):
    length = len(money_division)
    if (length == 1):
        actual_division[money_division[0]] = round(capital,2)
    else:
        divide(0.90 * capital,money_division[:-1])
        divide(0.10 * capital, money_division[-1:])


capital = 100
#for i in range(0,len(actual_division)):
    #if i > 0:
        #divide(capital-sum(actual_division[:i]),money_division[i:])
    #else:
        #divide(capital, money_division)

scores = list(total.items())
count = 1
for i in range(0,len(actual_division)):
    if i < len(scores) - 1:
        if scores[i][1] == scores[i+1][1]:
            count += 1
        else:
            difference_to_next = count * (scores[i][1] - (sum(e[1] for e in scores[(i + 1):]) / len(scores[i + 1:])))
            difference_till_end = scores[i][1] - scores[len(scores)-1][1]
            if difference_till_end == 0:
                difference_till_end = scores[i][1]
            division = (difference_to_next / (difference_to_next + difference_till_end))
            if i == len(scores) - 2:
                division = scores[i][1] / (scores[i][1] + scores[len(scores)-1][1])
            division_money = round((division * capital) / count,2)
            while count != 1:
                actual_division[i - count + 1] = division_money
                capital -= division_money
                count -= 1
            actual_division[i] = division_money
            capital -= division_money
            count = 1
    else:
        division = 1
        division_money = round((division * capital) / count, 2)
        while count != 1:
            actual_division[i - count + 1] = division_money
            capital -= division_money
            count -= 1
        actual_division[i] = division_money
        capital -= division_money
        count = 1

print("\nMoney Division:")
total_money = 0
for i, item in enumerate(actual_division):
    total_money += item
    print(str(i+1) + ": " + list(total.keys())[i] + ": " + str(item))
print("Total Money: " + str(round(total_money,2)))