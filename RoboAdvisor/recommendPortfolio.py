# this function will run if the invocation sourse is "FulfillmentCodeHook"
def fulfill(event):
    slots = event["currentIntent"]["slots"]
    riskLevel = slots["riskLevel"]
    if riskLevel=="None":
        rec = "100% bonds (AGG), 0% equities (SPY)"
    elif riskLevel=="Low":
        rec = "60% bonds (AGG), 40% equities (SPY)"
    elif riskLevel=="Medium":
        rec = "40% bonds (AGG), 60% equities (SPY)"
    elif riskLevel=="High":
        rec = "0% bonds (AGG), 100% equities (SPY). You are going to the moon."
    
    return {"dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": f"Your investment recommendation is : {rec}"
                }
            }
            }
            

# This function will run if the invocation sourse is "DialogCodeHook".
def dialog(event):
    slots = event["currentIntent"]["slots"]
    print("Slots from Dialog Function:")
    print(slots)
    age = slots["age"]
    investmentAmount = slots["investmentAmount"]
    
    # If the age slot has been entered, ensure the age is over 21, if not send back an "ElicitSlot" reponse
    if age is not None:
        age = float(age)
        
        if age<0 or age>65:
            slots["age"] = None
            return {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slots": slots,
                        "slotToElicit": "age",
                        "message": {"contentType": "PlainText", "content": "Please Enter a Valid Age"},
                        "intentName":event["currentIntent"]["name"]
                    }   
                }


    # If the InventmentAmount has been entered, check to make sure it is greater than 0, if it isnt, send an "elicitSlot" response back to Lex
    if investmentAmount is not None:
        investmentAmount = float(investmentAmount)
        
        if investmentAmount < 6500:
            slots["investmentAmount"] = None
            return {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slots": slots,
                        "slotToElicit": "investmentAmount",
                        "message": {"contentType": "PlainText", "content": "Our Minumum Investment is $6500, Please Enter a Valid Investment Amount."},
                        "intentName":event["currentIntent"]["name"]
                    }   
                }   

    # If all the slots that are entered so far are valid, send back a delegate response, which tells Lex that it decides what to ask for next
    return {
                "dialogAction": {
                    "type": "Delegate",
                    "slots": slots
                } 
            }
    
    
# Main request/response handler
def lambda_handler(event, context):
    print("Incoming Event:")
    print(event)
    
    if event["invocationSource"]=="DialogCodeHook":
        validation_response = dialog(event)
        
    if event["invocationSource"]=="FulfillmentCodeHook":
        validation_response = fulfill(event)
    
    print("Outgoing Response:")
    print(validation_response)
    return validation_response