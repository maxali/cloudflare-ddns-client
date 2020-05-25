import os
import logging
import azure.functions as func
from .cloudflareddns import update_dns

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ipaddr = read_param(req, 'ipaddr')
    domain = os.environ["DOMAIN"]
    token = os.environ["CLOUDFLARE_TOKEN"]

    if ipaddr and domain and token:
        auth = {'Authorization': 'Bearer {token}'.format(token=token)}
        update_dns(domain, auth, ipaddr)
        return func.HttpResponse(f"IP is {ipaddr}!")
    else:
        return func.HttpResponse(
             "ipaddr param, DOMAIN and CLOUDFLARE_TOKEN environments are required",
             status_code=400
        )


def read_param(req: func.HttpRequest, param):
    param_value = req.params.get(param)
    if not param_value:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            param_value = req_body.get(param)

    return param_value