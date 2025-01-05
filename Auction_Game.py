import numpy as np
#from bidder_kennedy import Bidder

class User:
    '''Class to represent a user with a secret probability of clicking an ad.'''

    def __init__(self):
        '''Generating a probability between 0 and 1 from a uniform distribution'''
        self.__probability = np.random.uniform() #Create a probability of opening an ad - secret and random

    def __repr__(self):
        '''User object with secret probability'''
        return "User with probability " + str(self.__probability) + " of clicking ad"

    def __str__(self):
        '''User object with a secret likelihood of clicking on an ad'''
        return "User with probability " + str(self.__probability) + " of clicking ad"

    def show_ad(self): 
        '''Returns True to represent the user clicking on an ad or False otherwise'''
        result = np.random.choice([True, False], p = [self.__probability, 1-self.__probability])
        return result

class Auction:
    '''Class to represent an online second-price ad auction'''
    
    def __init__(self, users, bidders):
        '''Initializing users, bidders, and dictionary to store balances for each bidder in the auction'''
        self.__users = users
        self.bidders = bidders
        self.num_bidders = len(bidders)
        self.num_users = len(self.__users)

        self.balanceval = [0 for i in range(self.num_bidders)]
        self.history = np.zeros((1, self.num_bidders))

        self.balances= {bidder: 0 for bidder in self.bidders}

    def __repr__(self):
        '''Return auction object with users and qualified bidders'''
        return "Auction class to simulate game, currently " + str(self.num_users) + "users, and " + str(self.num_bidders) + " bidders are playing"

    def __str__(self):
        '''Return auction object with users and qualified bidders'''
        return "Auction class to simulate game, currently " + str(self.num_users) + "users, and " + str(self.num_bidders) + " bidders are playing"

    def execute_round(self):
        '''Executes a single round of an auction, completing the following steps:
            - random user selection
            - bids from every qualified bidder in the auction
            - selection of winning bidder based on maximum bid
            - selection of actual price (second-highest bid)
            - showing ad to user and finding out whether or not they click
            - notifying winning bidder of price and user outcome and updating balance
            - notifying losing bidders of price'''
        
        #Assign user ids from 0 to n-1
        user_id_dict = {self.__users[i]: i for i in range(self.num_users)}
        user_id = list(user_id_dict.values())
        
        #Select random user
        selecteduser = np.random.choice(user_id)

        #Track qualified bidders. If bidder has balance >= -1000 they are eligible to bid
        self.qualified_bidders = []

        for indbidders, balance in self.balances.items():
            if balance >= -1000:
                self.qualified_bidders.append(indbidders)

        #Run bids from qualified bidders in the auction
        bids = [bidder.bid(selecteduser) for bidder in self.qualified_bidders]

        #Select winning bidder based on maximum bid
        max_bid = 0 #track winning bid amount
        actual_price = 0 #track price that will be charged (second-highest)
        bestbids = [] #list to hold highest bids, useful in case of a tie

        for i in range(len(bids)):
            if bids[i] == max_bid:
                bestbids.append(bids[i])
                actual_price = max_bid
            if bids[i] > max_bid:
                bestbids.append(bids[i])
                actual_price = max_bid
                max_bid = bids[i]
            else:
                if bids[i] > actual_price:
                    actual_price = bids[i]
            
        best = max_bid

        #Create dictionary with bidder objects and their corresponding bid
        bidder_bids_dict = dict(zip(self.qualified_bidders, bids))

        #If only one bidder is left, then that bid will be both the max and the actual price paid
        if len(bids) == 1:
            actual_price = max_bid

        #In the event of a tie, use matching keys in the bidder_bid_dict and randomize selection of winning object
        matching_keys = [k for k, v in bidder_bids_dict.items() if v == best]

        if len(matching_keys) > 1:
            winning_bidder = np.random.choice(matching_keys) # Randomly select the winning bidder if there's a tie
        else:
            winning_bidder = matching_keys[0] # If there's no tie, just pick the bidder with the highest bid
        
        #Confirm whether user clicked the ad; 0 if not, 1 if they did
        clicked = self.__users[selecteduser].show_ad()

        #Evaluate winning bidder, update their balance, and send appropriate notifications to all bidders
        for i, qualbidder in enumerate(self.bidders):
            if qualbidder == winning_bidder:
                if self.balanceval[i] <= -1000: #No notification for bidders that aren't qualified
                    self.balanceval[i] += 0 #No change in balance for unqualified bidders
                else:
                    self.balanceval[i] += clicked #Winning qualified bidder
                    self.balanceval[i] -= actual_price
                    self.bidders[i].notify(True, actual_price, clicked)
            else:
                if self.balanceval[i] <= -1000: #Nonwinning, nonqualified bidders
                    self.balanceval[i] += 0 #No change in balance for unqualified bidders
                else:
                    self.bidders[i].notify(False, actual_price, None) #Nonwinning, qualified bidder notification

        #Update history, useful for future visualizations
        self.history = np.vstack((self.history, self.balanceval))

        #Update balance dictionary
        self.balances = dict(zip(self.bidders, self.balanceval))

    def execute_game(self, num_rounds):
        '''Executes game based on determined set of rounds'''
        for i in range(num_rounds):
            self.execute_round()