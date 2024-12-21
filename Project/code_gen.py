import random as r

class CodeGenerator:

    # constructor
    def __init__(self):
        pass

    '''
    This method generates a one time password (no timer, that will be in a different class)
    
    parameters: nothing
    
    returns: the generated one time password
    '''
    def generate_code(self):
        otp = ""
        for i in range(0, 6):
            otp += str(r.randint(0, 9))

        return int(otp)