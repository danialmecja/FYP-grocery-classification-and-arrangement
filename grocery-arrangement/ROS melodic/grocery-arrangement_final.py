#!/usr/bin/env python
import rospy
from std_msgs.msg import String

# Import libraries
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


class grocery:
    def __init__(self, name, parent, code, height, width):
        # Initialize the size of the bin
        self.name = name
        self.parent = parent
        self.code = code
        self.height = height
        #self.weight = 1
        self.width = width
        if width >=15:
            self.weight = 2
        else:
            self.weight = 1

    def get_weight(width): # implement when get proper size of groceries
        if width != None:
            weight = 1 
        
    def get_parent(self):
        if self.parent == 27:
            return "packaged_foods"
        elif self.parent == 25:
            return "snack_foods"
        elif self.parent == 26:
            return "drinks"
        else:
            return "no parent"
    
    def get_height(self):
        if self.height >= 15:
            return "large"
        elif self.height >=5:
            return "medium"
        else:
            return "small"
    
class Bin:
    def __init__(self, size):
        # Initialize the size of the bin
        self.size = size

        # Create an empty list of items in the bin
        self.items = []
        self.grocery = []

    # Add an item to the bin
    def add_item(self, item):
        # Add the item to the list of items in the bin
        self.items.append(item)
        
    # Add a grocery item to the bin
    def add_grocery(self, grocery):
        # Add the item to the list of items in the bin
        self.grocery.append(grocery)
        

    # Check if the bin is full
    def is_full(self):
        # Return True if the sum of the sizes of the items in the bin is equal to the size of the bin,
        # otherwise return False
        return sum(self.items) == self.size

def bin_packing(items, bin_size):
    # Create a list of empty bins
    bins = []

    # Iterate over the items
    for item in items:
        # Try to find a bin where the item fits
        item_weight = item.weight
        
        for bin in bins:
            if not bin.is_full() and ((sum(bin.items) + item_weight) <= bin_size):
                # If the item fits, add it to the bin and move to the next item
                bin.add_item(item_weight)
                bin.add_grocery(item.name)
                
                break
        else:
            # If no bin was found, create a new bin and add the item to it
            bins.append(Bin(bin_size))
            bins[-1].add_item(item_weight)
            bins[-1].add_grocery(item.name)
            

    # Return the list of bins
    return bins

def sort_height(grocery):
    return grocery.height

def sort_width(grocery):
    return grocery.width

def sort_code(grocery):
    return grocery.code

def visualise_arrangement(bins):
    
    num_bins = []
    for bin in bins:
        num_bins.append(len(bin))
        
    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    
    layout_height = 50
    layout_width = 75

    ax.set_xlim([0, layout_width])
    ax.set_ylim([0, layout_height])


    colors = ['red', 'green', 'blue']
    x = 0 # initialise to arrange from left
    for num in range(len(num_bins)):
        y=25 # always arrange from top (inside of shelf)
        for i in range(num_bins[num]):
            if i == 0: # first pass
                pass
            elif i%2 == 0:
                x+=15
                y=25
            else:
                y=10

            # print category bins
            print("bin:", num_bins[num], "i:", i, "x,y: ", x ,y)
            ax.add_patch(Rectangle((x,y),15,15,edgecolor ='black',facecolor=colors[num]))
            
            prev_w = 0
            j = 0
            # print items in category
            for ind,grocery_item in enumerate(bins[num][i].grocery):
                weight = bins[num][i].items[ind] # weight
                
                    
                if j%4 == 0:
                    X = x+1.2
                    Y = y+10.5
                elif j%4 == 1 :
                    X = x+9.2
                    Y = y+10.5
                elif j%4 == 2:
                    X = x+1.2
                    Y = y+3.5
                else:
                    X = x+10.2
                    Y = y+3.5

                if weight == 2:
                    
                    ax.text(X, Y, grocery_item, fontsize = 20)
                    j+=1
                else :
                    ax.text(X, Y, grocery_item, fontsize = 15)
                j+=1     
        #reset new column for new category
        x += 15
    

    # Add title  and legend
    plt.title("Top view of shelf arrangement")
    leg = ax.legend (['Packaged Food', 'Snack Food', 'Drinks'])
    leg.legendHandles[0].set_color('red')
    leg.legendHandles[1].set_color('green')
    leg.legendHandles[2].set_color('blue')

    # Add shelf boundary
    ax.axhline(y=40,color='black')
    ax.axhline(y=10,color='black')
    ax.text(30, 45, 'back of shelf', style='italic',
        bbox={'facecolor': 'None', 'alpha': 0.5, 'pad': 10})
    ax.text(30, 5, 'front of shelf', style='italic',
        bbox={'facecolor': 'None', 'alpha': 0.5, 'pad': 10})

    plt.show()

def main():
    # import grocerylist
    os.chdir(r'/home/mustar/catkin_ws/src/mad_fyp/src/') # only directory
    with open('size.txt') as file: # replace with grocery list # error due to width
        lines = file.readlines()

    # Get all groceries into their parent classes (category)
    packaged_food = []
    snack_food = []
    drinks = []

    for line in lines:
        name, parent, code, height, width = line.strip().split(":")
        
        #creating classes
        name = grocery(name, int(parent),int(code), float(height), float(width))
        
        #separating them into categories
        if parent == "27":
            packaged_food.append(name)
        elif parent == "25":
            snack_food.append(name)
        else:
            drinks.append(name)

    # sort same items together
    packaged_food = sorted(packaged_food,key=sort_code)
    #print ("Items in packaged_food: ")
    #for items in packaged_food:
    #    print(items.name)
    snack_food = sorted(snack_food,key=sort_code)
    drinks = sorted(drinks,key=sort_code)

    # sort from tall to short sort descending(list)
    packaged_food_sorted = sorted(packaged_food,key=sort_height,reverse=True)
    print ("\nItems in packaged_food_sorted: ")
    #for items in packaged_food_sorted:
    #    print(items.name)
    snack_food_sorted = sorted(snack_food,key=sort_height,reverse=True)
    drinks_sorted = sorted(drinks,key=sort_height,reverse=True)
    
    # sort from largest width descending(list)
    packaged_food_sorted = sorted(packaged_food_sorted,key=sort_width,reverse=True)
    print ("\nItems in packaged_food_sorted: ")
    #for items in packaged_food_sorted:
    #    print(items.name)
    snack_food_sorted = sorted(snack_food_sorted,key=sort_width,reverse=True)
    drinks_sorted = sorted(drinks_sorted,key=sort_width,reverse=True)

    # feed it into bin packing algo -> get how many bins and what each one contains
    bin_size = 4
    bin_width = 2
    bin_height = 2
    packaged_food_bin = bin_packing(packaged_food_sorted,bin_size)
    snack_food_bin = bin_packing(snack_food_sorted,bin_size)
    drinks_bin = bin_packing(drinks_sorted,bin_size)

    print(" ")
    for i in packaged_food_bin:
        print("packaged_food_bin", packaged_food_bin.index(i)+1, " includes:  ", i.grocery)   
    print(" ")
    for j in snack_food_bin:
        print("snack_food_bin", snack_food_bin.index(j)+1, " includes:  ", j.grocery) 
    print(" ")
    for k in drinks_bin:
        print("drinks_bin", drinks_bin.index(k)+1, " includes:  ", k.grocery)  


    # output how many bins and grocery arrangement
    total_bins = [packaged_food_bin, snack_food_bin,drinks_bin]
    #print(total_bins)
    visualise_arrangement(total_bins)
    

if __name__=="__main__":
    main()
