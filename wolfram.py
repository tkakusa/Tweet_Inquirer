import wolframalpha
import re

"""
Function establishes a connection with the Wolfram Alpha Computational Knowledge
    Engine (CKE) and asks it the question provided in the "query" argument. It
    returns a Python list of the answers received from the CKE, or the list will
    contain just an error [ERR] message if an error occurred.
    This function requires that "wolframalpha" and "re" are both imported.
"""

def wolframQuery(query):
    try:
        # create wolfram alpha client service
        wolframService = wolframalpha.Client("9KL76E-2P62RRAAJ2")
        print("[DBG] Asking Wolfram the question.")

        # send the question through the wolfram alpha api
        answerPackage = wolframService.query(query)
    except Exception:
        return ["[ERR] There was a problem connecting to Wolfram Alpha."]
    else:
        print("[DBG] Got answer back.")

        # get answer from wolfram alpha
        try:
            results, = answerPackage.results
        except AttributeError:
            return ["[ERR] Wolfram Alpha did not understand your query."]
        else:
            print("[DBG] Extracting results.")
            # Extract the actual text of the answer
            answer = results.text

            # Split multiple answers
            answerList = re.split("\n[0-9] \| ", answer)

            # Put the numbers back on the front of the multiple answers that split() removed
            i = 1
            for multAnswer in answerList:
                if(i > 1):
                    answerList[i - 1] = (str(i) + " | " + multAnswer)
                i = i + 1;

            # Return the complete list of answers
            return answerList

while(1):
    answers = wolframQuery(input("Please ask a question: "))

    for subanswer in answers:
        print("ANSWER: " + subanswer)
