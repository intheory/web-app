from app.handlers import base
from paypal import PayPalInterface
from paypal import PayPalConfig
import os

#######GLOBALS#######
env = "ITENV" in os.environ and os.environ["ITENV"] or "dev"
if env=="prod":
	RETURN_URL = 'http://www.intheory.co.uk/payment/do'
	CANCEL_URL = "http://www.intheory.co.uk/payment"	
else:
	RETURN_URL = 'http://localhost:8888/payment/do'
	CANCEL_URL = "http://localhost:8888/payment"	

#####GLOBALS############
PAYPAL_API_USERNAME = "george_1350042703_biz_api1.intheory.co.uk"
PAYPAL_API_PASSWORD = "1350042729"
PAYPAL_API_SIGNATURE = "AQU0e5vuZCvSg-XJploSa.sGUDlpAJe3NGstI3cCC5XSh5CVK89vvFpa",

#####UTILITIES##########
#TODO: Create a factory?
def get_paypal_interface():
	'''
	Returns a paypal interface handle
	'''
	CONFIG = PayPalConfig(API_USERNAME = PAYPAL_API_USERNAME,
                        API_PASSWORD = PAYPAL_API_PASSWORD,
                        API_SIGNATURE = PAYPAL_API_SIGNATURE,
                        DEBUG_LEVEL=0)

	return PayPalInterface(config=CONFIG)

class ViewPaymentPageHandler(base.BaseHandler):
    '''
    Renders the payment page.    
    '''

    def on_get(self):
    	try:
	        ppi = get_paypal_interface()
	        setexp_response = ppi.set_express_checkout( PAYMENTREQUEST_0_AMT='10.00', 
														PAYMENTINFO_0_CURRENCYCODE="GBP",
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
        except Exception:
	    	self.log.warning("Error while rendering payment page: " + str(e))

class DoPaymentHandler(base.BaseHandler):
	'''
	This hanlder will make us rich! ... not.
	'''
	def on_get(self):
		try:
			token = self.get_argument("token", None)
			pid = self.get_argument("PayerID", None)

			ppi = get_paypal_interface()
			response = ppi.do_express_checkout_payment(token=token,
	        								payerid=pid,
	        								paymentaction='Sale',
	        								PAYMENTINFO_0_CURRENCYCODE="GBP",
	        								PAYMENTREQUEST_0_AMT='10.00')
			
			if response['ACK'] == "Success":
				self.redirect("/") 
			else:
				self.log.error("Erro while completing payment: ACK != Success")

		except Exception, e:
			self.log.warning("Error while completing payment: " + str(e))


#Seller:350042585
#Buyer: 350053375
