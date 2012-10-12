from app.handlers import base
from paypal import PayPalInterface
from paypal import PayPalConfig

#######GLOBALS#######
RETURN_URL = 'http://www.intheory.co.uk/payment/do'
CANCEL_URL = "http://www.intheory.co.uk/payment"

class ViewPaymentPageHandler(base.BaseHandler):
    '''
    Renders the payment page.    
    '''

    def on_get(self):
    	try:
	    	CONFIG = PayPalConfig(API_USERNAME = self.settings['paypal-api-username'],
									API_PASSWORD = self.settings['paypal-api-password'],
									API_SIGNATURE = self.settings['paypal-api-signature'],
									DEBUG_LEVEL=0)

	        ppi = PayPalInterface(config=CONFIG)
	    	
	        setexp_response = ppi.set_express_checkout(amt='10.00', 
														returnurl=RETURN_URL, 
														cancelurl=CANCEL_URL, 
														paymentaction='Order', 
														email="giorgosera@gmail.com",
														landingpage="Billing")

	        token = setexp_response.token
	        getexp_response = ppi.get_express_checkout_details(token=token)
	        
	        # Redirect client to this URL for approval.
	        redir_url = ppi.generate_express_checkout_redirect_url(token)
	        self.base_render("payment.html", redir_url=redir_url)
	        do_express_checkout_payment()
        except Exception:
	    	print e

class DoPaymentHandler(base.BaseHandler):
	'''
	This hanlder will make us rich!
	'''
	def on_get(self):
		print self.get_argument("token", None)
		print self.get_argument("token", None)

#Seller:350042585
#Buyer: 350053375
