



stored_hello_message='hello_from_agent'
stored_hello_pass='bletchelyPark'






def encription():
    pass

def decription():
    pass


def authentication_hello(rcv_message):
    if rcv_message['message']!=stored_hello_message or rcv_message['pass']!=stored_hello_pass:
        print("Wrong credentials")
        return False
    return True




def getAvailableScripts():
    return ["hello", "world"];

def formStartMessage():
    pass


def hello_processing(hello_message):

    if not hello_message:
        return False,{}

    hello_keys=['hostname','ip','message','pass']
    
    if not all(key in hello_message for key in hello_keys):
        print("Incoming message format not Ok")
        return False,{}
    

    if not authentication_hello(hello_message):
        return False,{}
    
    all(map(hello_message.pop,['message','pass']))  

    return True,hello_message
    





