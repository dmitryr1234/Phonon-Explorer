ls -lah#Custom errors for RSE

#Errors specific to input parameter parsing
class InputValidationError(Exception):
    def __init__(self, *args, **kwargs):

        #Validation errors and messages
        e_a = "error a";
        e_b = "error b";
        e_c = "error c";
        
        default_value = "there has been a validation error";
        result = {
            'a': e_a,
            'b': e_b,
            'c': e_c
        }.get(args[0],default_value);

        print(result);
        
        Exception.__init__(self,*args,**kwargs);
