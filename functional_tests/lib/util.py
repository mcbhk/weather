import logging
from datetime import datetime


def clean_screenshot_filename(scenario_name, suffix='fail'):
    """
    Create a filename for failed screenshots based on the scenario name
    and keeping any example reference ('@1.1', '@1.2', etc.)
    Also appends date to filename
    the suffix can be passed in e.g. 'search' to label a point in the scenario

    :param scenario_name:
    :return: cleaned up filename - as a string

    example returns:
    2017-08-17_10-58-51_Searching_for_Someth@1.6_fail.png
    """
    scenario_name = scenario_name.replace(" ", "_")
    scenario_name = scenario_name.replace('"', '')

    if len(scenario_name) > 20:
        our_file_name = scenario_name[:20]
    else:
        our_file_name = scenario_name

    example_ref_location = scenario_name.find("@")

    if example_ref_location:
        example_ref = scenario_name[example_ref_location:]
        our_file_name = our_file_name + example_ref

    scenario_new = our_file_name + str(suffix)
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    cleaned_up = now + '_' + scenario_new

    return cleaned_up


def clean_text_string_return_ascii(our_string):
    '''
    Remove unexpected characters from a strong and return as ascii
    '''
    ascii = our_string.encode('ascii', 'ignore')
    return ascii


def log_time_before_and_after(function_to_execute):
    """
    Use this function as a decorator in order to log the start and finish
    times for the named function you are executing
    """

    def log_function_timings(*args, **kwargs):
        logging.info("before:%s", datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        success = function_to_execute(*args, **kwargs)
        logging.info("after :%s", datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        return success

    return log_function_timings
