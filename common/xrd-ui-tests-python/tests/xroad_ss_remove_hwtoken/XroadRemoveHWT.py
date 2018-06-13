import unittest
from main.maincontroller import MainController
import os, time
from helpers import ssh_client


class XroadRemoveHWT(unittest.TestCase):
    """
    RIA URL: None
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_removehwt(self):
        main = MainController(self)
        main.test_number = 'XroadRemoveHWT'
        main.test_name = self.__class__.__name__


        main.log('Clear environment from docker')

        os.system('sudo docker stop cssim410_test')
        os.system('sudo docker rm --force cssim410_test')

        ss_ssh_host = main.config.get('hwtoken.ssh_host')
        ss_ssh_user = main.config.get('hwtoken.ssh_user')
        ss_ssh_pass = main.config.get('hwtoken.ssh_pass')
        '''Open connection'''
        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        '''Remove hardware token'''
        sshclient.exec_command('sudo apt-get remove -y xroad-addon-hwtokens', sudo=True)
        
        '''Restart xroad-signer service'''
        sshclient.exec_command('service xroad-signer restart', sudo=True)

        '''Wait for signer restart'''
        time.sleep(60)