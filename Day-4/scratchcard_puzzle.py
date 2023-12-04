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
    For every match found, a win_count variable is incremented. Once the lists have been compared, the total points won is then calculated, 
    by using the following formula: pow(2, (total_points_won - 1)).

    :param scratch_card_results: list of scratch card results in number form
    :param scratch_card_predictions: list of scratch card predictions in number form
    :return: a matrix containing (1) the total amount of scratchcard points won and (2) the total score of scratchcard points won, using the formula: pow(2, (total_points_won - 1))
    """ 
    win_count = 0
    winning_points = [0,0]
    
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
    
    winning_points[0] = win_count
    
    if (win_count > 1):
        winning_points[1] = pow(2, (win_count - 1))
    else:
        winning_points[1] = win_count
            
    return winning_points

def parse_and_calculate_scratch_card_points(scratch_card):
    """
    Takes parameter scratch_card, a list of scratch card predictions and results in string form, parses out the predictions and results from this string into a list of number predictions 
    and number results, sorts each list, searches for all matches in the results against the predictions and calculates and returns the total matches and points won based off the scratch 
    card's matches as a 2D matrix

    :param scratch_card: list of scratch card predictions and results in string form
    :return: 2D matrix of total matches and points won based off the scratch card's matches
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

def main():
    # Configure logging for debugging
    logging.basicConfig(level=logging.DEBUG)

    script_directory = pathlib.Path(__file__).parent.resolve()
    os.chdir(script_directory)

    total_scratchcard_score = 0
    total_scratch_card_win_instances = 0
    scratch_cards = []
    scratch_card_win_instances = {}

    # Parse the input data into scratch_cards, an in memory list object
    with open("input.txt") as input_file:
        for line_index, line in enumerate(input_file):
            # We don't care about the "Card <No>: " on the left hand side of each line of input data, so can scrub this out
            scratch_cards.append(line[line.find(":") + 1:len(line)].strip())
            
            # Initialise all scatch card win instances to default of 1 (A card with no matches has a win instance count of 1)
            scratch_card_win_instances[line_index] = 1
        
    """
        Iterate through each line of scratch card data in scratch cards, calculate the total points score for each line 
        of scratch card data and add this to the total sum total_scratch_card_points
    """
    for scratch_card_index, scratch_card in enumerate (scratch_cards):
        print("Checking scratchcard number: {}...\n".format(scratch_card_index))
        
        scratch_card_win_index = scratch_card_index + 1
        scratch_card_winning_points = parse_and_calculate_scratch_card_points(scratch_card)
        scratch_card_win_count = scratch_card_winning_points[0]
        total_scratchcard_score = total_scratchcard_score + scratch_card_winning_points[1]
        
        print("Matches found against scratchcard {}: {}".format(scratch_card_index, scratch_card_win_count))
        print("Points won for scratchcard {}:{}".format(scratch_card_index, scratch_card_winning_points[1]))
        
        # No point running win instance incrementation check logic if the element after current element is out of range of the scratch card array
        if ((scratch_card_index + 1) <= len(scratch_card_win_instances)):
            # If the range we're checking for win instance incrementation is out of range of the len of the scratch card array, we'll simply use a range that goes as far as the last element in the scratch card array instead 
            if ((scratch_card_index + scratch_card_win_count) < len(scratch_cards)): 
                scratch_card_win_index_range = scratch_card_win_index + scratch_card_win_count
            else:
                scratch_card_win_index_range = (scratch_card_win_index + scratch_card_win_count) - len(scratch_card_win_instances)
    
            for win_instance_index in range (scratch_card_win_index, scratch_card_win_index_range):
                scratch_card_win_instances[win_instance_index] += scratch_card_win_instances[scratch_card_index]
        
        print("\n")

    for scratch_card_win_instance in scratch_card_win_instances.items():
        total_scratch_card_win_instances += scratch_card_win_instance[1]

    print("Total points won for all scratchcards: {}".format(total_scratchcard_score))
    print("Total scratchcard win instances: {}".format(total_scratch_card_win_instances))
    
if __name__ == '__main__':
    main()