# Views 
this module implement views or 'endpoint'.
## Classes
### PaymentConfirmationView
A class can be used to recive payment confirmation 
#### Paramters 
- **required_body_options** required paramter in recived response if the there is a missing field the response will be ignored
- **manager** an delgater who make response confirmation 
- **model** A `PaymentModel` who implement `AbstractPayment`

#### Methods
- **post** revcive post request, validate request and make confirmation
- **validate_signature** check if the signature if it is correct
- **get_args** extract all args from request
- **validate_args** validate args and check `required_body_options`.
- **confirmation** if the request is valide this method is responsable for extract payment `status` and submit the result
- **get_object** return payment object using `invoice_number`

### CreatePaymentView
a View that responsable for creating a new payments extends `CreateView`    
#### Paramaters
- **payment_create_faild_url** if create payment is failed the view will redirect user to this url 
#### Methods
- **form_valid** if the form that sumbited from user is valide the this method will be called. 
- **create_object** method responsable for creating a new payment object
- **payment_create_faild** called when some error happen, it redirect to `payment_create_failed_url**

### PaymentObjectStatusView
a View responsable to show payment status extends `DetailView`

### PaymentObjectDoneView
a View responsable to show status of  **finished payment** 

### FakePaymentView
a View used for **Devlopment**, this view mimic **chargily service**.