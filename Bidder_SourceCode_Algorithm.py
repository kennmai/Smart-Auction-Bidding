import numpy as np

class Bidder:
    '''Class to represent a bidder in an online second-price ad auction'''
    
    round_count = 0

    def __init__(self, num_users, num_rounds):
        '''Setting number of users, number of rounds, and round counter'''
        self.num_users = num_users
        self.num_rounds = num_rounds
        Bidder.round_count += 1 #initialize class attribute for round_count
        
        self.trials_per_user = [0 for i in range(num_users)] 
        self.clicks_per_user = [0 for i in range(num_users)]
        self.clickrate_per_user = [0 for i in range(num_users)]

        self.wins = [0 for i in range(num_users)]
        self.lose = [0 for i in range(num_users)]

    def __repr__(self):
       '''Return Bidder object'''
       return "A bidder participating in the class Auction."

    def __str__(self):
        '''Return Bidder object'''
        return "There are " + str(self.num_users) + " users considered in this bidder instance, and " + str(self.num_rounds) + " bidder rounds total"

    def bid(self, user_id):
        '''Returns a non-negative bid amount'''
        self.selected_user_id = user_id

        #The algorithm is epsilon greedy inspired by the multi-armed bandit problem; balancing exploration and exploitation for maximum results
        if self.trials_per_user[self.selected_user_id] < 3:
            self.bidamount = round(np.random.uniform(0.008, 10.000),3) ##If trials_per_user for the selected user were small, bidder can bid high
        elif np.random.uniform() < .05:
            self.bidamount = round(np.random.uniform(0.010, 15.000), 3) ##If random uniform guess is less than epsilon = 0.05, bidder should bid high
        else:
            #If more is known about the user, including clickrate and results, bid lower to maximize profit
            self.bidamount = self.clickrate_per_user[user_id] * np.random.uniform(0.000, 5.000)
            self.bidamount = round(self.bidamount, 3)

        return self.bidamount
    
    def notify(self, auction_winner, price, clicked):
        '''Updates bidder attributes based on results from an auction round'''
        self.price = price
        if auction_winner:
            self.trials_per_user[self.selected_user_id] += 1 #Update trial information for future learning if bidder wins
            self.clicks_per_user[self.selected_user_id] += float(clicked) #Update click information for future learning if bidder wins
            self.clickrate_per_user[self.selected_user_id] = self.clicks_per_user[self.selected_user_id] / self.trials_per_user[self.selected_user_id]
            #Return required notifications with the actual price the ad went for and whether or not the user clicked the ad (if winner)
            if clicked:
                return "Congratulations, you won! Your winning price is: $" + str(self.price) + "The user also clicked your ad."
            else:
                return "Congratulations, you won! Your winning price is: $" + str(self.price) + "The user did not click your ad."
        else:
            return "You did not win this round. The winning price was: $" + str(self.price) + ". Feel free to try again."