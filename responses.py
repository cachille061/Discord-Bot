from random import choice, randint

def get_response(user_input: str) -> str: # -> str is return annotation, says to return type str, paramter is named user_input and should be type str.
    lowered: str = user_input.lower() # raise is a keyword used to raise exceptions manually, here, when the code execution reaches this line, it will immediately stop and raise the NotImplementedError, effectively signaling to the developer that they need to implement the missing code. Commonly used as a placeholder in situations where you want to indicate that a certain part of your code has not been implemented yet, or if you want to mark a section of your code as incomplete.
# Double quotes and single quotes can be used interchangebly for strings in Python.

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'
    else:
        return choice(['I do not understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])