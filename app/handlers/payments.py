# -*- coding: utf-8 -*-
import os
import tornado
from app.handlers import base
import paypal
from paypal import PayPalInterface
from paypal import PayPalConfig
from app.model.user import UserPaymentDetails
from app.model.coupons import Coupon
from mongoengine.queryset import DoesNotExist
from datetime import datetime 

#######GLOBALS#######
env = "ITENV" in os.environ and os.environ["ITENV"] or "dev"
if env=="prod":
	RETURN_URL = 'http://www.intheory.co.uk/payment/do'
	CANCEL_URL = "http://www.intheory.co.uk/payment"	
else:
	RETURN_URL = 'http://localhost:8888/payment/do'
	CANCEL_URL = "http://localhost:8888/payment"	

#####GLOBALS############
PAYPAL_API_USERNAME = "zahid_api1.intheory.co.uk"
PAYPAL_API_PASSWORD = "UZQZC8RD228TZEU4"
PAYPAL_API_SIGNATURE = "AA6FKP55XSbL3HvSeGi8V-Fb.Yv8A47KsUXj1CQw531s.vd-HCMVUsrL",
PRODUCT_PRICE = 9.99

#####UTILITIES##########
#TODO: Create a factory?
def get_paypal_interface():
	'''
	Returns a paypal interface handle
	'''
	CONFIG = PayPalConfig(API_USERNAME = PAYPAL_API_USERNAME,
                        API_PASSWORD = PAYPAL_API_PASSWORD,
                        API_SIGNATURE = PAYPAL_API_SIGNATURE,
                        API_ENVIRONMENT="production",
                        DEBUG_LEVEL=0)

	return PayPalInterface(config=CONFIG)

class ViewPaymentPageHandler(base.BaseHandler):
    '''
    Renders the payment page.    
    '''
    @tornado.web.authenticated
    def on_get(self):
    	try:	   
    		if not self.current_user.has_paid:    
	        	self.base_render("payments/payment.html")
	        else:
	        	self.base_render("payments/thankyou.html")
        except Exception, e:
	    	self.log.warning("Error while rendering payment page: " + str(e))

class DoPaymentHandler(base.BaseHandler):
	'''
	This hanlder will make us rich! ... not.
	'''
	@tornado.web.authenticated
	def on_get(self):
		try:
			token = self.get_argument("token", None)
			pid = self.get_argument("PayerID", None)

			ppi = get_paypal_interface()
			response = ppi.do_express_checkout_payment(token=token,
	        								payerid=pid,
	        								PAYMENTREQUEST_0_PAYMENTACTION='Sale',
	        								PAYMENTREQUEST_0_CURRENCYCODE='GBP',
	        								PAYMENTREQUEST_0_AMT=self.current_user.price,
	        								PAYMENTREQUEST_0_DESC= 'Intheory Web App - ' + '£' + str(self.current_user.price) + ' - Full Access')
			
			if response['ACK'] == "Success":
				transaction_id = response['PAYMENTINFO_0_TRANSACTIONID']
				receipt_id = response['PAYMENTINFO_0_RECEIPTID']

				self.current_user.record_payment(transaction_id, receipt_id)
				self.log.info("User with id "+ str(self.current_user.id) + "has paid. The transaction id is " + transaction_id)
				self.base_render("payments/thankyou.html")
			else:
				self.base_render("payments/paymenterror.html")
				self.log.error("Error while completing payment: ACK != Success")
		except Exception, e:
			self.log.warning("Error while completing payment: " + str(e))

#Seller:350042585
#Buyer: 350053375

class RedeemCouponHandler(base.BaseHandler):
	'''
	Redeems a coupon and calculates the new price 
	'''
	@tornado.web.authenticated
	def on_get(self):
		code = self.get_argument("code", None)
		try:
			c = Coupon.objects(code=code, redeemed=False, expiration_date__gte=datetime.now()).get()
			discount = PRODUCT_PRICE * float(c.discount)/100
			new_price = "{0:.2f}".format(PRODUCT_PRICE - discount)
			success = True
			return (new_price,success)
		except DoesNotExist:
			success = False
			return (PRODUCT_PRICE, success)

	def on_success(self, new_price, success):
		self.xhr_response.update({"new_price":new_price})
		self.xhr_response.update({"success":success})
		self.write(self.xhr_response)

class RedirectToPayPalHandler(base.BaseHandler):
    '''
    Redirects user to the Paypal page
    '''
    def on_get(self):
        try:
            #Calculate price
            code = self.get_argument("code", None)
            try:
                c = Coupon.objects(code=code, redeemed=False, expiration_date__gte=datetime.now()).get()
                discount = PRODUCT_PRICE * float(c.discount)/100
                price = PRODUCT_PRICE - discount
                c.redeemed = True
                c.save()
            except DoesNotExist:
                price = PRODUCT_PRICE

            if  price == 0:
            	redir_url = "/dashboard"
                self.current_user.record_payment("Free voucher transaction", "Free voucher transaction")
                self.current_user.price = str("{0:.2f}".format(price))
                self.current_user.save()
                self.log.info("User with id "+ str(self.current_user.id) + "has paid. The transaction id is " + "Free voucher transaction")
            else:
	            ppi = get_paypal_interface()
	            email = self.current_user and self.current_user.email or ""
	            self.current_user.price = str("{0:.2f}".format(price))
	            self.current_user.save()
	            setexp_response = ppi.set_express_checkout( PAYMENTREQUEST_0_AMT=str("{0:.2f}".format(price)), 
															PAYMENTREQUEST_0_CURRENCYCODE='GBP',
															returnurl=RETURN_URL, 
															cancelurl=CANCEL_URL, 
															PAYMENTREQUEST_0_PAYMENTACTION='Order',
															email=email,
					        								PAYMENTREQUEST_0_DESC= 'Intheory Web App - ' + '£' + str("{0:.2f}".format(price)) + ' - Full Access',
															landingpage="Billing")

	            token = setexp_response.token
	            getexp_response = ppi.get_express_checkout_details(token=token)
	               
	            # Redirect client to this URL for approval.
	            redir_url = ppi.generate_express_checkout_redirect_url(token)

            return (redir_url,)
        except Exception, e:
            self.log.warning("Error while redirecting user with id " + str(self.current_user.id) + " to PayPal: " + str(e))

    def on_success(self, redirect_url):
        self.xhr_response.update({"redirect_url":redirect_url})
        self.write(self.xhr_response)
