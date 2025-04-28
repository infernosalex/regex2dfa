# regex infix notation to postfix notation using the Shunting Yard algorithm (polish notation)
def add_explicit_concatenation(regex):
    # add explicit concatenation operator '.' to a regex
    output = []
    for i in range(len(regex)):
        output.append(regex[i])
        if i < len(regex) - 1:
            left_concat = regex[i] not in '(|' and regex[i] != '\\'

            # if the previous character is a backslash, disable concatenation            
            if i > 0 and regex[i-1] == '\\':
                left_concat = False
            
            right_concat = regex[i+1] not in ')|?+*'

            # if the NEXT character is a backslash (and not the last char), treat it as something that CAN be concatenated like a normal character.
            if regex[i+1] == '\\' and i+1 < len(regex) - 1:
                right_concat = True
            
            if left_concat and right_concat:
                output.append('.')
    
    return ''.join(output)

def regex_to_postfix(regex):
    # add explicit concatenation operators
    regex = add_explicit_concatenation(regex)
    
    # precedence of operators
    precedence = {
        '|': 1,
        '.': 2,
        '?': 3,
        '*': 3,
        '+': 3
    }
    stack = []
    output = []

    i = 0
    while i < len(regex):
        c = regex[i]
        # handle escape characters
        if c == '\\' and i + 1 < len(regex):
            output.append(c + regex[i+1])
            i += 2
            continue
        
        if c.isalnum() or c in ['ε']:
            # append to output
            output.append(c)
        elif c == '(':
            # push onto stack
            stack.append(c)
        elif c == ')':
            # pop operators until matching left parenthesis
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
            else:
                raise ValueError("Mismatched parentheses")
        else:
            # pop operators with higher or equal precedence, then push
            # * (Kleene star) > . (concatenation) > | (union)
            while stack and \
                stack[-1] != '(' and \
                stack[-1] in precedence and \
                precedence[stack[-1]] >= precedence.get(c, 0):
                    output.append(stack.pop())
            stack.append(c)
        
        i += 1
    
    # pop any remaining operators
    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())
    
    return ''.join(output)

if __name__ == "__main__":
    test_expressions = [
        "a",
        "a*",
        "a|b",
        "ab",
        "(a|b)*",
        "a(b|c)*",
        "(a|b)(c|d)",
        "a?bc*",
        "(a+b)*c"
    ]
    
    for expr in test_expressions:
        with_concat = add_explicit_concatenation(expr)
        postfix = regex_to_postfix(expr)
        print(f"{expr:15} -> {with_concat:15} -> {postfix}")