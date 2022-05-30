# Models 
the core compenent in this package is the `models` field it can be used to store and track the payment.

# Classes
## AbstractPayment
the most top level abstract class it contains all the necessary data to produce a payment request

to use this class you need to **extend** it.
### Fileds
- **invoice_number:** `str` required used as primary key
- **amount:** `float` required 
- **comment:** `str` required
- **discount:** `float` required 
- **mode:** `enum` required 
- **status:** `enum` required initial value `progress`

**Metadata**

- **created_date:** `date` autofield
- **updated_date:** `date` autofield
- **payment_date:** `date` used when payment `status` chaged to `paid`

### Variables
- **back_url:** when payment done chargily service will redirect user to this link, if u don't want to use this field you can overide `generate_back_url` 
- **webhook_url:** when payment process terminate chargily service will send payment result to this link, if u don't want to use this field you can overide `generate_webhook_url` 

### Methods
- **get_payment_data:** return `dict` with all data required to make a pymanet request
- **generate_webhook_url** return a full url to the website page that hander payment confirmation it use `webhook_url` variable
- **generate_back_url** return a full url to the payment status when payment is done
- **get_client_email** return client email **NEED TO BE IMPLEMENTED**
- **get_client** return client username **NEED TO BE IMPLEMENTED**
- **make_payment** send request payment to website and return url response. if there is an error the payment status will set to `failed`.
- **payment_failed** set payment `status` to `failed`
- **payment_confirm** set payment `status` to `paid`
- **payment_canceled** set payment `status` to `canceled`

## AuthPayment
this is an abstract class that extend from `AbstractPayment`, it can used for authenticated payment which mean the user who created this payment has an account and logged in.

you can use this type of payment in **ecommerce**, **invoice payment** anything who required for the user to be loggedin

### Fields
- **client:** `ForeignKey` required 
- **client_email:** `str` required
### Methods
- **get_client_email:** return a value of `client_email`.
- **get_client** return a value of `client`.


## AnonymPayment
same as `AuthPayment` extend `AbstractPayment`

you can use this type fo payment in payments that not required user to be loggedin like **sponsoring**

### Fields
- **client:** `str` required 
- **client_email:** `str` required
### Methods
- **get_client_email:** return a value of `client_email`.
- **get_client** return a value of `client`.


## FakePaymentMixin
this class can be used with one of the above class it override `make_payment` methode, this will readirect the payment process to a fake payment page. You can use it for `devlopment`