import re
import pathlib
import os
import logging

def convert_number_string_to_number_array(number_string):
    """Converts a string of numbers to an array of integers.
    
    :param number_string: list of numbers in string form
    :return: list of numbers parsed from number_string
    """
    return [int(num) for num in number_string.split()]

def calculate_scratch_card_points(scratch_card_results, scratch_card_predictions):
    """
    Takes parameters scratch_card_results - a list of scratch card results in number form and scratch_card_predictions - 
    a list of scratch card predictions in number form. It then compares the values contained within scratch_card_results against those in scratch_card_predictions. 
    For every match found, a win_count variable is incremented. Once the lists have been compared, the total points won is then calculated, by using the following formula:
    The first win gives one point and each win after the first doubles the total number of points.

    :param scratch_card_results: list of scratch card results in number form
    :param scratch_card_predictions: list of scratch card predictions in number form
    :return: the total amount of scratchcard points won 
    """ 
    win_count = 0
    total_points_won = 0
    
    # Iterate through all elements of scratch_card_results and for each element, search for the element's value in scratch_card_prediction_values, incrementing win_count by 1 on each occurence
    for scratch_card_result in scratch_card_results:
        for scratch_card_prediction_value in scratch_card_predictions:
            if (scratch_card_result == scratch_card_prediction_value):
                print("Matching number: {} found between scratch card results and predictions, incrementing points multiplier by 1".format(scratch_card_prediction_value))
                win_count += 1
                break
            # Since both lists are sorted, we know there's no point continuing to check the list if the current prediction element value being checked is greater than the current result element value being checked
            elif (scratch_card_prediction_value > scratch_card_result):
                break    
    
    # Iterate through the count of wins in the range of win_count, using a 2x multiplier for every win past the first win.
    for win in range(win_count):
        if (win == 0):
            total_points_won = 1
        else:
            total_points_won = 2 * total_points_won
            
    return total_points_won

def parse_and_calculate_scratch_card_points(scratch_card):
    """
    Takes parameter scratch_card, a list of scratch card predictions and results in string form, parses out the predictions and results from this string into a list of number predictions 
    and number results, sorts each list, searches for all matches in the results against the predictions and calculates and returns the total points won based off these scratch card matches

    :param scratch_card: list of scratch card predictions and results in string form
    :return: total points won based off scratch card matches
    """ 
    
    """ 
        Get the scratch card result values by stripping out everything on the right hand side of "|" character in the scratch_card string, 
        then feed this into convert_number_string_to_number_array function to convert the string of numbers into an array of numbers.
    """
    scratch_card_results = convert_number_string_to_number_array(scratch_card[0:scratch_card.find("|") -  1])
    
    # Sort the array of numbers
    scratch_card_results.sort()

    """
        Get the scratch card prediction values by stripping out everything on the left hand side of "|" character in the scratch_card string, 
        then feed this into convert_string_list_to_number_array function to convert the string of numbers into an array of numbers.
    """
    scratch_card_predictions = convert_number_string_to_number_array(scratch_card[scratch_card.find("|") +  1:len(scratch_card)])
    
    # Sort the array of numbers
    scratch_card_predictions.sort()
    
    return calculate_scratch_card_points(scratch_card_results, scratch_card_predictions)


# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

script_directory = pathlib.Path(__file__).parent.resolve()
os.chdir(script_directory)
scratch_cards = []
total_scratch_card_points = 0

# Parse the input data into scratch_cards, an in memory list object
with open("input.txt") as input_file:
    for line in input_file:
        # We don't care about the "Card <No>: " on the left hand side of each line of input data, so can scrub this out
        scratch_cards.append(line[line.find(":") + 1:len(line)].strip())
    
"""
    Iterate through each line of scratch card data in scratch cards, calculate the total points score for each line 
    of scratch card data and add this to the total sum total_scratch_card_points
"""
total_scratch_card_points = sum(parse_and_calculate_scratch_card_points(scratch_card) for scratch_card in scratch_cards)

print(total_scratch_card_points)