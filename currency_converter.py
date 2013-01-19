from CurrencyService_client import *
import sys

def getXchangeRate(fromCcy="USD", toCcy="JPY", verbose=False):
    loc = CurrencyServiceLocator()
    if verbose: # set tracefile to standard output
        port = loc.getBasicHttpBinding_ICurrencyService(tracefile=sys.stdout)
    else:
        port = loc.getBasicHttpBinding_ICurrencyService()

    # instantiate request object
    request = ICurrencyService_GetConversionRate_InputMessage()

    # set FromCurrency attribute of the request object
    fromCur = request.new_FromCurrency(fromCcy)
    request.set_element_FromCurrency(fromCur)

    # set ToCurrency attribute of the request object
    toCur = request.new_ToCurrency(toCcy)
    request.set_element_ToCurrency(toCur)

    kwargs = {}

    try:
        # send request
        response = port.GetConversionRate(request, **kwargs)
    except Exception as e:
        print e
    else:
        output = "Conversion Rate: %.2f" % (response.GetConversionRateResult.Rate)
        print output

if __name__ == '__main__':
    getXchangeRate('USD','INR')
