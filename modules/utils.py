import constants
import json


def get_tx_code():
    """
    Return incremented transaction code for the next operation
    """

    # Read deposit request payload JSON object as dict
    with open(constants.DEPOSIT_PAYLOAD, 'r') as dpf:
        deposit_payload = json.load(dpf)

    # Read withdrawal request payload JSON object as dict
    with open(constants.WITHDRAWAL_PAYLOAD, 'r') as wpf:
        withdrawal_payload = json.load(wpf)

    # Get latest transaction code and increment
    txcode = max(int(deposit_payload['txcode']),
                     int(withdrawal_payload['txcode']))
    txcode += 1

    return txcode
