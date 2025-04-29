import json
import os
import sys
from regex_to_postfix import regex_to_postfix
from nfa_builder import thompson_construction
from nfa_to_dfa import subset_construction, simulate_dfa

def process_test_json(test):
    name = test['name']
    regex = test['regex']
    test_strings = test['test_strings']
    
    # try catch to convert regex to postfix
    try:
        postfix_not = regex_to_postfix(regex)
        # print(f"Postfix notation: {postfix_not}")
    except Exception as e:
        return {
            'name': name,
            'success': False,
            'error': f"Error converting to postfix: {str(e)}"
        }
    
    # build NFA using Thompson's algorithm
    try:
        nfa = thompson_construction(postfix_not)
    except Exception as e:
        return {
            'name': name,
            'success': False,
            'error': f"Error building NFA: {str(e)}"
        }
    
    # convert NFA-2-DFA using subset construction
    try:
        dfa = subset_construction(nfa)
    except Exception as e:
        return {
            'name': name,
            'success': False,
            'error': f"Error converting to DFA: {str(e)}"
        }
    
    # test if the DFA works with json test file
    results = []
    for test in test_strings:
        input_string = test['input']
        expected = test['expected']
        result = simulate_dfa(dfa, input_string)
        
        if result == expected:
            status = "PASS"
        else:
            status = "FAIL"
        
        results.append({
            'input': input_string,
            'expected': expected,
            'output': result,
            'status': status
        })
        
        # print(f"Test '{input_string}': expected={expected}, output={result}, status={status}")
    
    return {
        'name': name,
        'success': True,
        'results': results
    }

def process_test_file(file_path):
    try:
        with open(file_path, 'r') as f:
            tests = json.load(f)
    except Exception as e:
        print(f"Error loading test file: {str(e)}")
        return

    print(f"Tests loaded: {len(tests)} tests")

    results = []
    for test in tests:
        result = process_test_json(test)
        results.append(result)

    success_count = sum(1 for r in results if r['success'] == True)
    print("Tests passed:", success_count, "/", len(tests))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # test file path provided as command line argument
        test_file = sys.argv[1]
    else:
        # default test file path, test file provided by teacher
        test_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 "regex2dfa/LFA-Assignment2_Regex_DFA_v2.json")
    
    # print(f"test file: {test_file}")
    process_test_file(test_file)