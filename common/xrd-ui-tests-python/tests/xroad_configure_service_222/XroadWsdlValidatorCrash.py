# coding=utf-8
import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import wsdl_validator_errors
from view_models import ss_system_parameters


class XroadWsdlValidatorCrash(unittest.TestCase):
    def test_xroad_wsdl_validator_crash(self):
        main = MainController(self)

        ssh_host = main.config.get('ss1.ssh_host')
        ssh_user = main.config.get('ss1.ssh_user')
        ssh_pass = main.config.get('ss1.ssh_pass')

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        client_id = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        client_name = main.config.get('ss1.client_name')

        wsdl_warning_url = main.config.get('wsdl.remote_path').format(
            main.config.get('wsdl.service_wsdl_warning_filename'))
        wsdl_validator_wrapper_path = ss_system_parameters.WSDL_VALIDATOR_WRAPPER_LOCATION

        test_wsdl_validator_crash = wsdl_validator_errors.test_wsdl_validator_crash(case=main,
                                                                                    ssh_host=ssh_host,
                                                                                    ssh_username=ssh_user,
                                                                                    ssh_password=ssh_pass,
                                                                                    wsdl_url=wsdl_warning_url,
                                                                                    ss_host=ss_host,
                                                                                    ss_user=ss_user,
                                                                                    ss_pass=ss_pass,
                                                                                    client_id=client_id,
                                                                                    client_name=client_name,
                                                                                    wsdl_validator_wrapper_path=wsdl_validator_wrapper_path)

        try:
            '''SERVICE_44 step 1c Testing wsdl validation, when wsdl validator is executed with wrong argument'''
            main.log('SERVICE_44 step 1c Testing wsdl validation, when wsdl validator is executed with wrong argument')
            test_wsdl_validator_crash()
        except:
            main.log('Test failed')
            assert False
        finally:
            main.log('Restoring wsdl wrapper')
            wsdl_validator_errors.restore_wsdl_validator_wrapper(case=main, ssh_host=ssh_host, ssh_username=ssh_user,
                                                                 ssh_password=ssh_pass,
                                                                 wsdl_validator_wrapper_path=wsdl_validator_wrapper_path)
            main.tearDown()
