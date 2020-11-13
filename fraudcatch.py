import json
import os

totalTrumpLost = 0
totalBidenLost = 0
totalThirdLost = 0
totalTrump2Biden = 0
totalTrump2Third = 0
totalBiden2Trump = 0
totalBiden2Third = 0
totalThird2Trump = 0
totalThird2Biden = 0

def findfraud(NAME):
    with open('/home/timmanz/NYTTmeSeries/' + NAME + '.json', encoding="utf8") as f:
        x = json.load(f)
    TotalVotesLostTrump = 0
    TotalVotesLostBiden = 0
    TotalVotesLostThird = 0
    TrumpToThird = 0
    TrumpToBiden = 0
    BidenToTrump = 0
    ThirdToTrump = 0
    ThirdToBiden = 0
    BidenToThird = 0
    global totalTrumpLost
    global totalBidenLost
    global totalThirdLost
    global totalTrump2Biden
    global totalTrump2Third
    global totalBiden2Trump
    global totalBiden2Third
    global totalThird2Trump
    global totalThird2Biden
    series = x["data"]["races"][0]["timeseries"]
    for i in range(len(series)):
            if i == 0:
                i=1
            thirdPartyNow = series[i]["votes"] * (1 - series[i]["vote_shares"]["bidenj"] - series[i]["vote_shares"]["trumpd"])
            thirdPartyThen = series[i-1]["votes"] * (1 - series[i-1]["vote_shares"]["bidenj"] - series[i-1]["vote_shares"]["trumpd"])
            TrumpNow = series[i]["votes"] * series[i]["vote_shares"]["trumpd"]
            TrumpThen = series[i-1]["votes"] * series[i-1]["vote_shares"]["trumpd"]
            BidenNow = series[i]["votes"] * series[i]["vote_shares"]["bidenj"]
            BidenThen = series[i-1]["votes"] * series[i-1]["vote_shares"]["bidenj"]
            if i != 0 and TrumpNow < TrumpThen and (TrumpThen - TrumpNow) > (0.00049999 * series[i]["votes"]) + 50:
                if BidenNow > BidenThen or thirdPartyNow > thirdPartyThen:
                    if TrumpNow - TrumpThen <= BidenNow - BidenThen or TrumpNow - TrumpThen <= thirdPartyNow - thirdPartyThen:
                        TrumpLostNow = TrumpThen - TrumpNow
                        TrumpLostTotal = TrumpThen - TrumpNow
                        if BidenNow > BidenThen and TrumpNow - TrumpThen <= BidenNow - BidenThen:
                            if BidenNow - BidenThen > TrumpLostTotal:
                                TrumpToBiden += TrumpLostTotal
                                TrumpLostTotal = 0
                            else:
                                TrumpToBiden += BidenNow - BidenThen
                                TrumpLostTotal -= BidenNow - BidenThen
                        if thirdPartyNow > thirdPartyThen and TrumpNow - TrumpThen <= thirdPartyNow - thirdPartyThen:
                            if thirdPartyNow - thirdPartyThen > TrumpLostTotal:
                                TrumpToThird += TrumpLostTotal
                                TrumpLostTotal = 0
                            else:
                                TrumpToThird += thirdPartyNow - thirdPartyThen
                                TrumpLostTotal -= thirdPartyNow - thirdPartyThen
                        if TrumpLostNow < 0:
                            TrumpLostNow = 0
                        TotalVotesLostTrump += TrumpLostNow - TrumpLostTotal
            if i != 0 and BidenNow < BidenThen and (BidenThen - BidenNow) > (0.00049999 * series[i]["votes"]) + 50:
                if TrumpNow > TrumpThen or thirdPartyNow > thirdPartyThen:
                    if BidenNow - BidenThen <= TrumpNow - TrumpThen or BidenNow - BidenThen <= thirdPartyNow - thirdPartyThen:
                        BidenLostNow = BidenThen - BidenNow
                        BidenLostTotal = BidenThen - BidenNow
                        if TrumpNow > TrumpThen and BidenNow - BidenThen <= TrumpNow - TrumpThen:
                            if TrumpNow - TrumpThen > BidenLostTotal:
                                BidenToTrump += BidenLostTotal
                                BidenLostTotal = 0
                            else:
                                BidenToTrump += TrumpNow - TrumpThen
                                BidenLostTotal -= TrumpNow - TrumpThen
                        if thirdPartyNow > thirdPartyThen and BidenNow - BidenThen <= thirdPartyNow - thirdPartyThen:
                            if thirdPartyNow - thirdPartyThen > BidenLostTotal:
                                BidenToThird += BidenLostTotal
                                BidenLostTotal = 0
                            else:
                                BidenToThird += thirdPartyNow - thirdPartyThen
                                BidenLostTotal -= thirdPartyNow - thirdPartyThen
                        if BidenLostNow < 0:
                            BidenLostNow = 0
                        TotalVotesLostBiden += BidenLostNow - BidenLostTotal
            if i!= 0 and thirdPartyNow < thirdPartyThen and (thirdPartyThen - thirdPartyNow) > (0.00049999 * series[i]["votes"]) + 50:
                if thirdPartyNow < thirdPartyThen:
                    if thirdPartyNow - thirdPartyThen <= TrumpNow - TrumpThen or thirdPartyNow - thirdPartyThen <= BidenNow - BidenThen:
                        ThirdLostTotal = thirdPartyThen - thirdPartyNow
                        ThirdLostNow = thirdPartyThen - thirdPartyNow
                        if BidenNow > BidenThen and thirdPartyNow - thirdPartyThen <= BidenNow - BidenThen:
                            if BidenNow - BidenThen > ThirdLostTotal:
                                ThirdToBiden += ThirdLostTotal
                                ThirdLostTotal = 0
                            else:
                                ThirdToBiden += BidenNow - BidenThen
                                ThirdLostTotal -= BidenNow - BidenThen
                        if TrumpNow > TrumpThen and thirdPartyNow - thirdPartyThen <= TrumpNow - TrumpThen:
                            if TrumpNow - TrumpThen > ThirdLostTotal:
                                ThirdToTrump += ThirdLostTotal
                                ThirdLostTotal = 0
                            else:
                                ThirdToTrump += TrumpNow - TrumpThen
                                ThirdLostTotal -= TrumpNow - TrumpThen
                        if ThirdLostNow < 0:
                            ThirdLostNow = 0
                        TotalVotesLostThird += ThirdLostNow - ThirdLostTotal
                        
    print (str(round(TotalVotesLostTrump))  + " TRUMP LOST")
    print (str(round(TrumpToBiden)) + " Trump to Biden")
    print (str(round(TrumpToThird)) + " Trump to Third")
    print (str(round(TotalVotesLostBiden))  + " BIDEN LOST")
    print (str(round(BidenToTrump)) + " Biden to Trump")
    print (str(round(BidenToThird)) + " Biden to Third")
    print (str(round(TotalVotesLostThird))  + " 3RD PARTY LOST")
    print (str(round(ThirdToBiden)) + " Third to Biden")
    print (str(round(ThirdToTrump)) + " Third to Trump")
    
    netTrumpState = BidenToTrump + ThirdToTrump - TrumpToBiden - TrumpToThird
    netBidenState = TrumpToBiden + ThirdToBiden - BidenToTrump - BidenToThird
    netThirdState = TrumpToThird + BidenToThird - ThirdToTrump - ThirdToBiden
    
    print (str(round(netTrumpState)) + " NET Trump")
    print (str(round(netBidenState)) + " NET Biden")
    print (str(round(netThirdState)) + " NET Third")
        
    totalTrumpLost += TotalVotesLostTrump
    totalBidenLost += TotalVotesLostBiden
    totalThirdLost += TotalVotesLostThird
    totalTrump2Biden += TrumpToBiden
    totalTrump2Third += TrumpToThird
    totalBiden2Trump += BidenToTrump
    totalBiden2Third += BidenToThird
    totalThird2Trump += ThirdToTrump
    totalThird2Biden += ThirdToBiden
    
    
        
directory = r'/home/timmanz/NYTTmeSeries'
for filename in os.listdir(directory):
    state = filename.replace(".json", "")
    print(" ")
    print(" *** " + state + " *** ")
    findfraud(state)


print("Total Trump Lost:: " + str(round(totalTrumpLost)))
print("Total Biden Lost: " + str(round(totalBidenLost)))
print("Total Third Lost: " + str(round(totalThirdLost)))
print(" ")
print("Total Trump -> Biden: " + str(round(totalTrump2Biden)))
print("Total Trump -> Third: " + str(round(totalTrump2Third)))
print("Total Biden -> Trump: " + str(round(totalBiden2Trump)))
print("Total Biden -> Third: " + str(round(totalBiden2Third)))
print("Total Third -> Trump: " + str(round(totalThird2Trump)))
print("Total Third -> Biden: " + str(round(totalThird2Biden)))

netTrump = totalBiden2Trump + totalThird2Trump - totalTrump2Biden - totalTrump2Third
netBiden = totalTrump2Biden + totalThird2Biden - totalBiden2Trump - totalBiden2Third
netThird = totalTrump2Third + totalBiden2Third - totalThird2Trump - totalThird2Biden
print(" ")
print("Total Net Trump: " + str(round(netTrump)))
print("Total Net Biden: " + str(round(netBiden)))
print("Total Net Third: " + str(round(netThird)))