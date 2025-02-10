import re

from rdflib import Literal


def create_query(request: str):
    if request.startswith("query:"):
        request = "PREFIX ecom: <http://example.org/ecommerce#> " + request[len("query:"):]
        return {'query': request, 'bind': None }
    # now we work on the transactions here
    intent_details = extract_email_and_transaction(request)
    if intent_details['transaction_types']:
        if intent_details['transaction_types'][0] == 'customer':
            print('its for customers')
            return create_customer_request(intent_details)
        return create_order_request(intent_details)
    else:
        print('No content observed')
    query = """
                PREFIX ecom: <http://example.org/ecommerce#>
                SELECT ?Name ?Email ?OrderStatus WHERE { ?customer a ecom:Customer ;
                ecom:email ?Email ; ecom:name ?Name ; ecom:placesOrder ?order .
                ?order a ecom:Order ; ecom:orderStatus ?OrderStatus . } LIMIT 10
                """
    print('just a fallback plan')
    return {'query': query, 'bind': None }
def create_customer_request(intent_details):
    if intent_details['emails']:
        if len(intent_details['emails']) > 0:
            email = intent_details['emails'][0]
            query = """
                    PREFIX ecom: <http://example.org/ecommerce#>
                    SELECT ?Name ?Email ?OrderStatus WHERE {
                        ?customer a ecom:Customer ; ecom:email ?Email ;
                        ecom:name ?Name ; ecom:placesOrder ?order .
                        ?order a ecom:Order ; ecom:orderStatus ?OrderStatus .
                    } LIMIT 6
                    """
            return {'query': query, 'bind': { 'Email': Literal(email)}}
    query = """
            PREFIX ecom: <http://example.org/ecommerce#>
            SELECT ?Name ?Email ?OrderStatus WHERE { ?customer a ecom:Customer ;
            ecom:email ?Email ; ecom:name ?Name ; ecom:placesOrder ?order .
            ?order a ecom:Order ; ecom:orderStatus ?OrderStatus . } LIMIT 10
            """
    return {'query': query, 'bind': None }
def create_order_request(intent_details):
    if intent_details['emails']:
        if len(intent_details['emails']) > 0:
            email = intent_details['emails'][0]
            query = """
                    PREFIX ecom: <http://example.org/ecommerce#>
                    SELECT ?Name ?Email  ?Cost ?OrderStatus WHERE {
                        ?customer a ecom:Customer ; ecom:email ?Email ;
                        ecom:name ?Name ; ecom:placesOrder ?order .
                        ?order a ecom:Order ; ecom:orderStatus ?OrderStatus ; ecom:cost ?Cost .
                    } LIMIT 6
                    """
            return {'query': query, 'bind': { 'Email': Literal(email)}}
    query = """
            PREFIX ecom: <http://example.org/ecommerce#>
            SELECT ?Name ?Email  ?Cost ?OrderStatus WHERE {
            ?customer a ecom:Customer ; ecom:email ?Email ;
            ecom:name ?Name ; ecom:placesOrder ?order .
            ?order a ecom:Order ; ecom:orderStatus ?OrderStatus ; ecom:cost ?Cost .
            } LIMIT 6
            """
    return {'query': query, 'bind': None }
def extract_email_and_transaction(text):
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    transaction_type_regex = r"(orders|order|customer|customers)"
    emails = re.findall(email_regex, text)
    transaction_types = re.findall(transaction_type_regex, text, re.IGNORECASE)  # Case-insensitive
    return { "emails": emails, "transaction_types": list(set(transaction_types)) }
