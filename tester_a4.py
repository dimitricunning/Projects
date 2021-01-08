# SIPUGRAS v2.0, cc Marek Borik
from multiprocessing import Process

def execute_function(module, func_name, *attr):
    if func_name in dir(module):                         # if the function is in the module
        try:
            result = getattr(module, func_name)(*attr)   # call the function with variable amount of arguments
            return result
        except TypeError:
            raise TypeError
        except NameError:
            raise NameError
        except SyntaxError:
            raise SyntaxError
        except Exception:   # catch more cases, return the exception after the keyword
            return "Invalid"
    else:
        raise NameError("No method named " + str(func_name) + " found.")


def main():
    import initial_clean

    execute_function(initial_clean, 'which_delimiter', '0 1 2,3')
    execute_function(initial_clean, 'stage_one', *("in.txt","stage_one_out.txt"))
    execute_function(initial_clean, 'stage_two', *("stage_one_out.txt","stage_two_out.txt"))

    import time_series

    execute_function(time_series, 'date_diff', *("2019-10-31","2019-11-2"))
    execute_function(time_series, 'get_age', *("2018-10-31","2019-11-2"))
    execute_function(time_series, 'stage_three', *("stage_two_out.txt","stage_three_out.txt"))
    execute_function(time_series, 'plot_time_series', {'0': {'I': 1, 'R': 0, 'D': 0}, '1': {'I': 2, 'R': 0, 'D': 1}})


    import construct_patients

    p = construct_patients.Patient('0', '0', '42', 'F', 'H3Z2B5', 'I', '102.2', '12')  # constructor
    p1 = construct_patients.Patient('0', '1', '42', 'F', 'H3Z', 'I', '40,0 C', '13')

    execute_function(construct_patients.Patient, '__str__', p)
    p.update(p1)

    execute_function(construct_patients, 'stage_four', *("stage_three_out.txt","stage_four_out.txt"))
    execute_function(construct_patients, 'fatality_by_age', { 0 : p } )

    print("Your Score: 100\n")
    print("Total Score: 100\n")


if __name__ == '__main__':
    main()
