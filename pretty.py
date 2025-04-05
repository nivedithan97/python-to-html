import sys
import html
import tokenize
from io import BytesIO
import io
import keyword


"""
The function that takes in all the parameters from the function getmaterials
and create a file with the name of the input python filename
and write it with the content materials in the format of desired html code.

Paremeters:
        NoL = result from countNumOfLines
        MlL = result from countMaxLineLen
        MaxV = result from countMaxVarLen
        MinV = result from countMinVarLen
        MaxCmt = result from countMaxCmmtLine
        NoD = result from countNumOfDefs
        NoS = result from countNumOfStrs
        NoN = result from countNumOfNums
        NoR = result from countNumOfRepConst
        code = html formatted code of the codes part

Result: 
        open a html file with the original python file name, if not exist then create one.
        fill in the content with the result of stats and codes in the html code

"""
def getthehtml(NoL, MlL, MaxV, MinV, MaxCmt, NoD, NoS, NoN, NoR, code, filename):
    filename = filename[:-3]
    filename = filename+'.html' #convert from "filename.py" to "filename.html"
    output = open(filename, 'w')
    output.write(f"""<!doctype html>
        <html lang=en>
            <head>
                <meta charset=utf-8>
                <title>Pretty Python</title>
                <style>
                    pre {{font-size: 16pt}}
                    .variable {{color: black}}
                    .comment {{color: green}}
                    .keyword {{color: blue}}
                    .string {{color: orange}}
                    .number {{color: red}}
                    .operator {{color: purple}}
                </style>
            </head>
            <body>
                <h1>Python code inspector</h1>
                <ul>
                    <li>
                        <a href="#stats">Statistics</a ></li>
                    <li>
                        <a href="#code">Code</a ></li>
                </ul>
                <div id="stats">
                    <h2>Statistics</h2>
                    <ul>
                        <li> Number of lines:  {str(NoL)} </li>
                        <li> Maximum line length:  {str(MlL)} </li>
                        <li> Maximum variable name length:  {str(MaxV)} </li>
                        <li> Minimum variable name length: {str(MinV)} </li>
                        <li> Number of comment lines: {str(MaxCmt)}  </li>
                        <li> Number of definitions:   {str(NoD)}   </li>
                        <li> Number of strings:    {str(NoS)}    </li>
                        <li> Number of numbers:    {str(NoN)}    </li>
                        <li> Number of repeated constants:  {str(NoR)} </li>
                    </ul>
                </div>
                <div id="code">
                    <h2>Python code</h2>
                        
                            <code>
                                {code}
                            <code>
                    
                </div>
            </body>
        </html>
        """)
    output.close()

"""
Prepare the stat information and code for the html file

Paremeters:
        f is a string of original file content
        fl is a list of string where each element is a line from the original file's content
        lst is a list of tokens records the info in the generator that tokenize produced from the original file
        filename is the filename of the original file

Result:
        NoL = result from countNumOfLines 
        MlL = result from countMaxLineLen
        MaxV = result from countMaxVarLen
        MinV = result from countMinVarLen
        MaxCmt = result from countMaxCmmtLine
        NoD = result from countNumOfDefs
        NoS = result from countNumOfStrs
        NoN = result from countNumOfNums
        NoR = result from countNumOfRepConst
        code = html formatted code of the codes part, which is result from colouring

"""
def get_contents(f, fl, lst, filename):
    NoL = countNumOfLines(fl)
    MlL = countMaxLineLen(fl)
    MaxV = countMaxVarLen(lst)
    MinV = countMinVarLen(lst)
    MaxCmt = countMaxCmmtLine(lst)
    NoD = countNumOfDefs(lst)
    NoS = countNumOfStrs(lst)
    NoN = countNumOfNums(lst)
    NoR = countNumOfRepConst(lst)
    code = colouring(f, fl)
    # return all the output in to html
    getthehtml(NoL, MlL, MaxV, MinV, MaxCmt, NoD, NoS, NoN, NoR, code, filename)

"""
This function counts the number of lines

Parameter:
        ipt is the list of stings whose element is each line of the original .py file 
Result:
        counter is the lenth of the input list which is also the number of lines of the .py file

"""

def countNumOfLines(fl):
    # count the number of lines by list of string
    counter = len(fl)
    return counter

"""
This function calculates the number of characters

Parameter:
        ipt is the list of stings whose element is each line of the original .py file
Result:
        counter keeps track of the lenth of the longest line
"""
def countMaxLineLen(fl):
    counter = 0
    # ipt is list of strings
    # for each line, count the length
    for lines in fl:
        counter = max(counter, len(lines))
    return counter

"""
This function calculates the maximum length of a variable 

Parameter:
        lst_tk is the list of tokens generated by tokenizing the original .py file
Result:
        maxvarlen is the maximum length of the varible that is appeared in the original .py file, 
        it will be 0 if there is no varible in the original .py file.
        
"""
def countMaxVarLen(lst_tk):
    # tk is tokenized file
    maxvarlen = 0
    for token in lst_tk:
        # token[0] is type=1 (NAME), variable or keywords
        if token[0] == 1:
            # judge between variable or keywords
            if not keyword.iskeyword(token[1]):
                # same line different position
                maxvarlen = max(maxvarlen, token[3][1] - token[2][1])
    return maxvarlen

"""
This function calculates the minimum length of a variable 

Parameter:
        lst_tk is the list of tokens generated by tokenizing the original .py file
Result:
        minvarlen is the minimum length of the varible that is appeared in the original .py file, 
        it will be 0 if there is no varible in the original .py file.
        
"""
def countMinVarLen(lst_tk):
    # lst_tk is tokenized file
    minvarlen = 0
    for token in lst_tk:
        # token[0] is type=1 (NAME), variable or keywords
        if token[0] == 1:
            # judge between variable or keywords
            if not keyword.iskeyword(token[1]):
                if minvarlen == 0:
                # same line different position
                    minvarlen = token[3][1] - token[2][1]
                minvarlen = min(minvarlen, token[3][1] - token[2][1])
    return minvarlen

"""
This function calculates the total number of comment lines

Parameter:
        lst_tk is the list of tokens generated by tokenizing the original .py file
Result:
        counter is the conted number of maximum number of lines of a single comment
        
"""
def countMaxCmmtLine(lst_tk):
    counter = 0
    for token in lst_tk:
        # type=60 is comment
        if token[0] == 60:
            counter += 1
    return counter

"""
This function calculates the total number of function or method definitions

Parameter:
        lst_tk is the list of tokens generated by tokenizing the original .py file
Result:
        counter is the counted number of defs
        
"""
def countNumOfDefs(lst_tk):
    counter = 0
    for token in lst_tk:
        if token[0] == 1:
            # type = 1 Name, either variable or keywords: definitions are defines of functions
            if token[1] == 'def':
                counter += 1
    return counter

"""
This function counts the total number of string literals (string literals are surrounded in 
single/double or triple single/double quotes)

Parameter:
        lst_tk is the list of tokens generated by tokenizing the original .py file
Result:
        counter is the counted number of strings
        
"""
def countNumOfStrs(lst_tk):
    counter = 0
    for token in lst_tk:
        # type = 3 STRING
        if token[0] == 3:
            counter += 1
    return counter

"""
This function counts the total number of numeric literals

Parameter:
        lst_tk is the list of tokens generated by tokenizing the original .py file
Result:
        counter is the counted number of numbers
        
"""
def countNumOfNums(lst_tk):
    counter = 0
    for token in lst_tk:
        # type = 2 NUMBER
        if token[0] == 2:
            counter += 1
    return counter

"""
This function counts the number of string and numeric literal that occur more than once

Parameter:
        lst_tk is the list of tokens generated by tokenizing the original .py file
Result:
        maxcount is the counted number of repetad constants
        
"""
def countNumOfRepConst(lst_tk):
    # count repetitions
    def countdicrep(dic):
        counter = 0
        for entry in dic:
            if dic[entry] >= 2:
                counter += 1
        return counter

    # constants are numbers and strings
    dic1 = {}
    dic2 = {}
    for token in lst_tk:
        # type = 2 is NUMBER
        if token[0] == 2:
            if token[1] not in dic1:
                dic1[token[1]] = 1
            else:
                dic1[token[1]] += 1

    for token in lst_tk:
        # type = 3 is STRING
        if token[0] == 3:
            if token[1] not in dic2:
                dic2[token[1]] = 1
            else:
                dic2[token[1]] += 1

    maxcount = countdicrep(dic1)
    maxcount += countdicrep(dic2)
    return maxcount

def color_token(token):
    """
    Provides the token type and the token value for a given token and formats it accordingly for HTML syntax coloring

    Parameters:
        token: The token that needs to be formatted
        eg. TokenInfo(type=1 (NAME), string='def', start=(527, 0), end=(527, 3), line='def run_all_tests():\n')

    Result: 
        (token_type, token_value): A tuple containing the token's original string value and the type of token
        for eg. whether it is a COMMENT, OPERATOR, STRING, etc.
    """

    token_type = tokenize.tok_name[token.type].lower()
    token_value = html.escape(token.string) 

    if keyword.iskeyword(token_value):
            token_type = "keyword"
    elif token_type == "op":
        token_type = "operator"
    elif token_type == "name":
        token_type = "variable"
    
    return (token_type, token_value)

def count_spacing(prev_endtok,token_start):
    """
    Counts the spacing between two tokens by calculating the difference between the end position of the 
    previous token and the start position of the current token provided they are on the same line.
    If it is on a different line, the function will return an empty string.

    Parameters:
        prev_endtok: the end position of the previous token that stores the line and column number
        token_start: the start position of the current token that stores the line and column number

    Result:
        space_counter: amount of spacing between the given two tokens
        token_start: updated starting position of the token
    """

    if token_start[0] == prev_endtok[0]:
        num_spaces = token_start[1] - prev_endtok[1]
        space_counter = '&nbsp;' * num_spaces
    else:
        space_counter = ""
    return space_counter,token_start

def multiline_string(prev_endtok, current_line, token_start,token_value):
    """
    This function deals with handling multiline strings. It splits the multiline string
    into individual lines and then iterates over each line and adds it to the final_string.

    Parameters:
        prev_endtok: the end position of the previous token that stores the line and column number
        current_line: current line number the program is at
        token_start: the start position of the current token that stores the line and column number
        token_value: the string value that contains the multi-line comments
    
    Result:
        enterMultiLine: A flag that keeps track of whether there was a multi-line comment in the program, in essence, if the program has entered this function,
        it means there is a multi-line comment
        prev_endtok: updated ending position of the previous token
        current_line: updated current line number
        final_string: string that contains the formatted multi-line comments

    """

    final_string = ""
    enterMultiLine = True
    linenoIncrement = 0
    stringSplit = token_value.splitlines()
    for stringline in stringSplit:
        updatedLineNo = token_start[0] + linenoIncrement
        if linenoIncrement == 0:
            if  current_line != updatedLineNo:
                final_string += f"<tr><td><span id=\'line'>{updatedLineNo:<10}</span><span class='string'>{stringline}\n</span></td></tr>"
            else:
                final_string += f"<tr><td><span class='string'>{stringline}\n</span></td></tr>"
        else:
            final_string += f"<tr><td><span id=\'line'>{updatedLineNo:<10}</span><span class='string'>{stringline}\n</span></td></tr>"
        linenoIncrement += 1
    current_line = updatedLineNo
    prev_endtok = token_start
    return enterMultiLine, prev_endtok, current_line, final_string

def colouring(f, fl):
    """
    This function tokenizes the input file contents with the help of 'tokenize' module.
    color the tokens, adds the formatted tokens into a HTML table with each line of code in the file
    represented as a row in the table.

    Parameters:
        f: contents in a file in a string
        f1: a list consisting each line of the contents of a file

    Result:
        table_body: a string containing a HTML table representing the input file
        with color-coded tokens        
    """

    table_body = ""
    final_string = "\n"
    current_line = None
    prev_endtok = (1, 0)
    enterMultiLine = False
    file_contents = f
    space_counter = ""
    lines = file_contents.split("\n")
    in_comment = False

    # tokenizer doesn't recognise backslash character, so adding an escape character to the backslash character

    #to ignore if the backslash is in multi-line comment
    for idx in range(len(lines)):
        if "'''" in lines[idx] or "''" in lines[idx]:
            in_comment = not in_comment
        if in_comment:
            continue

        #to ignore if it is in a print statement or if the backslash is within quotes    
        if lines[idx].endswith("\\") and "print(" not in lines[idx] and "'\\'" not in lines[idx] and "'''\\" not in lines[idx] and not lines[idx].startswith('"\\') and not lines[idx].endswith('\\"'):
            lines[idx] = lines[idx].replace("\\", "\\\\")

    file_contents = "\n".join(lines)
    num_lines = len(fl)

    for token in tokenize.generate_tokens(io.StringIO(file_contents).readline):
        #coloring the tokens
        token_type, token_value = color_token(token)
        line_number = token.start[0]
        token_start = token.start
        
        # terminate the program once we have reached the end of the file
        if line_number > num_lines:
            break
        if line_number== num_lines and token_type == "newline":
            break
        
        #if there are backslashes, output the backslash and go to the next line
        if token_value == "\\":
            token_value = "\\\n"

        # calculate number of spaces between tokens
        if token_value == '\n' or token_value == '\\\n':
            prev_endtok = (token.end[0] + 1, 0)

        else:
            space_counter, token_start = count_spacing(prev_endtok,token_start)
            prev_endtok = token.end

        # handle line numbering if it is for multi comments
        if enterMultiLine == True and token_value == "\n":
            enterMultiLine = False
            continue
        if token_type == "string" and token_value.count("\n") > 0:
            enterMultiLine, prev_endtok, current_line, string_html = multiline_string(prev_endtok, current_line, token_start, token_value)
            final_string += string_html

        # adding tokens to the string while ensuring that the format is kept intact if the tokens belong in the same line
        elif current_line == line_number:
            final_string += f"<tr><span class='{token_type}'>{space_counter}{token_value}</span></tr>"

        else:
            final_string += f"<tr><span id=\'line'>{line_number:<10}</span><span class='{token_type}'>{space_counter}{token_value}</span></tr>"
        current_line = line_number
    # append the formatted tokens to table_body
    table_body += f"<pre>\n{final_string}</pre>"
    
    return table_body  



if __name__ == '__main__':
    filename = sys.argv[1]  # to take file name form terminal()
    #filename = 'pretty.py'

    with open(filename, 'r') as file:
        # global contents, str
        contents = file.read()
        # global contents, list of str
        contentslines = contents.split('\n')
        # tokenize str
        tokens = tokenize.tokenize(BytesIO(contents.encode('utf-8')).readline)
        # to make a list of tokens because tokens are iterable once
        lst = list(tokens)

    get_contents(contents, contentslines, lst, filename)