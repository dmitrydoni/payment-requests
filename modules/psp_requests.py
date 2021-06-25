import constants
import utils
import json
import hashlib
import urllib
import requests


def get_deposit_request_params(payload_file):
    """
    Return payload with deposit request params
    """

    # Read deposit request payload JSON object as dict
    with open(payload_file, 'r') as dpf:
        deposit_payload = json.load(dpf)

    # Remove old signature, if any
    if 'signed' in deposit_payload:
        del deposit_payload['signed']

    # Get incremented transaction code
    txcode = utils.get_tx_code()
    deposit_payload.update(
        {
            'txcode': txcode
        }
    )

    # Prepare URL query string
    query_string = urllib.parse.urlencode(deposit_payload)
    print(f"\nQuery string: {query_string}\n")

    # Add signature to payload
    query_string_key_appended = query_string + constants.API_KEY
    signed = calc_signature(msg=query_string_key_appended.encode('utf-8'))
    deposit_payload.update(
        {
            'signed': signed
        }
    )
    print(f"Payload with signature:\n{json.dumps(deposit_payload, indent=4)}\n")

    # Persist updated payload to JSON file
    with open(payload_file, 'w') as dpf:
        json.dump(deposit_payload, dpf, indent=4)

    return deposit_payload


def get_status_request_params(payload_file):
    """
    Return payload with status request params
    """

    # Read deposit request payload JSON object as dict
    with open(constants.DEPOSIT_PAYLOAD, 'r') as dpf:
        deposit_payload = json.load(dpf)

    # Read status request payload JSON object as dict
    with open(payload_file, 'r') as spf:
        status_payload = json.load(spf)

    # Remove old signature, if any
    if 'signed' in status_payload:
        del status_payload['signed']

    # Set params from deposit request payload
    amount = deposit_payload['amount']
    currency = deposit_payload['currency']
    customer = deposit_payload['customer']
    merchant = deposit_payload['merchant']
    txcode = deposit_payload['txcode']
    status_payload.update(
        {
            'amount': amount,
            'currency': currency,
            'customer': customer,
            'merchant': merchant,
            'txcode': txcode,
        }
    )

    # Prepare URL query string
    query_string = urllib.parse.urlencode(status_payload)
    print(f"\nQuery string: {query_string}\n")

    # Add signature to payload
    query_string_key_appended = query_string + constants.API_KEY
    signed = calc_signature(msg=query_string_key_appended.encode('utf-8'))
    status_payload.update(
        {
            'signed': signed
        }
    )
    print(f"Payload with signature:\n{json.dumps(status_payload, indent=4)}\n")

    # Persist updated payload to JSON file
    with open(payload_file, 'w') as spf:
        json.dump(status_payload, spf, indent=4)

    return status_payload


def get_withdrawal_request_params(payload_file):
    """
    Return payload with withdrawal request params
    """

    # Read withdrawal request payload JSON object as dict
    with open(payload_file, 'r') as wpf:
        withdrawal_payload = json.load(wpf)

    # Remove old signature, if any
    if 'signed' in withdrawal_payload:
        del withdrawal_payload['signed']

    # Get incremented transaction code
    txcode = utils.get_tx_code()
    withdrawal_payload.update(
        {
            'txcode': txcode
        }
    )

    # Prepare URL query string
    query_string = urllib.parse.urlencode(withdrawal_payload)
    print(f"\nQuery string: {query_string}\n")

    # Add signature to payload
    query_string_key_appended = query_string + constants.API_KEY
    signed = calc_signature(msg=query_string_key_appended.encode('utf-8'))
    withdrawal_payload.update(
        {
            'signed': signed
        }
    )
    print(f"Payload with signature:\n{json.dumps(withdrawal_payload, indent=4)}\n")

    # Persist updated payload to JSON file
    with open(payload_file, 'w') as wpf:
        json.dump(withdrawal_payload, wpf, indent=4)

    return withdrawal_payload


def calc_signature(msg):
    """
    Return signature calculated using the SHA512 hash function
    """

    signature = hashlib.sha512(msg).hexdigest()

    return signature


def send_request(url, payload):
    """
    Send a request to payment provider's API
    """

    response = requests.get(url, params=payload)

    print(f"Status code: {response.status_code}\n"
          f"Headers: {response.headers}\n"
          f"Content: {response.content}")

    return response


def make_request(request_type):
    """
    Make a request to payment provider's API
    Supported request types: payin, status, payout
    """

    assert request_type in constants.REQUEST_TYPES, \
        "Request type should be one of: 'payin', 'status', 'payout'."

    if request_type == 'payin':
        deposit_request_payload = get_deposit_request_params(
            payload_file=constants.DEPOSIT_PAYLOAD
        )

        # Generate URL to navigate to the provider's payment form
        response = constants.PAYMENT_GATEWAY + '?' + urllib.parse.urlencode(deposit_request_payload)
        print(f"Payment Form URL:\n{response}")

    else:
        if request_type == 'status':
            status_request_payload = get_status_request_params(
                payload_file=constants.STATUS_PAYLOAD
            )
            response = send_request(
                url=constants.STATUS_GATEWAY,
                payload=status_request_payload
            )
        if request_type == 'payout':
            withdrawal_request_payload = get_withdrawal_request_params(
                payload_file=constants.WITHDRAWAL_PAYLOAD
            )
            response = send_request(
                url=constants.WITHDRAWAL_GATEWAY,
                payload=withdrawal_request_payload
            )

        # Save provider's response to a file
        with open('../output/' + request_type + '_response.json', 'w') as rf:
            json.dump(response.json(), rf, indent=4)

    return response


make_request(request_type='payin')  # 'payin', 'status', 'payout'
