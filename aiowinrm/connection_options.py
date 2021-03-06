import asyncio
import aiohttp
import re

from aiowinrm.sec import AuthEnum
from aiowinrm.errors import AIOWinRMException
from aiowinrm.sec.utils import set_kerb_pwd
from aiowinrm.sec.windows_session import \
    HAVE_NTLM, \
    HAVE_KERBEROS, \
    KERB_ENCRYPTION_AVAILABLE, \
    NTLM_ENCRYPTION_AVAILABLE
from aiowinrm.utils import check_url, get_url_info


IP4_RE = re.compile(r'([01]?[0-9]?[0-9]|2[0-4][0-9]|2[5][0-5])\.{4}')


class ConnectionOptions(object):

    def __init__(self,
                 winrm_url,
                 username,
                 password,
                 auth_method,
                 realm=None,
                 verify_ssl=True,
                 default_to_ssl=True,
                 connector=None,
                 loop=None,
                 allow_plain_text=False,
                 server_certificate_hash=None,
                 ca_trust_path=None,
                 cert_pem=None,
                 cert_key_pem=None,
                 read_timeout_sec=None,
                 kerberos_delegation=False,
                 kerberos_hostname_override=None,
                 message_encryption='auto',
                 credssp_disable_tlsv1_2=False,
                 send_cbt=True,
                 keytab=None,
                 ad_server=None):

        self.loop = asyncio.get_event_loop() if loop is None else loop
        self._connector = connector
        self.url = check_url(winrm_url, default_to_ssl)

        # prevent accidental plain text usage
        if 'https://' not in self.url \
                and not allow_plain_text \
                and auth_method == AuthEnum.Basic:
            raise AIOWinRMException('Usage of HTTP + Basic Auth is insecure and discouraged')

        if isinstance(auth_method, AuthEnum):
            auth_method = auth_method.value
        if auth_method == AuthEnum.Kerberos.value and not realm:
            raise AIOWinRMException(f'realm is required for {auth_method}')

        # pick an auth method if auto
        if auth_method == 'auto':
            host, scheme, port, path = get_url_info(winrm_url)
            if not IP4_RE.match(host) and realm and HAVE_KERBEROS and KERB_ENCRYPTION_AVAILABLE:
                auth_method = 'kerberos'
            elif scheme == 'https':
                auth_method = 'ntlm' if HAVE_NTLM else 'basic'
            elif HAVE_NTLM and NTLM_ENCRYPTION_AVAILABLE:
                auth_method = 'ntlm'
            elif allow_plain_text:
                auth_method = 'basic'
            else:
                raise AIOWinRMException('Could not find a suitable auth_method')

        # creds
        self.realm = realm
        self.username = username
        self.password = password
        self.ad_server = ad_server

        # sec
        self.verify_ssl = verify_ssl
        self.server_certificate_hash = server_certificate_hash
        self.auth_method = auth_method
        self.ca_trust_path = ca_trust_path
        self.cert_pem = cert_pem
        self.cert_key_pem = cert_key_pem
        self.read_timeout_sec = read_timeout_sec
        self.kerberos_delegation = kerberos_delegation
        self.kerberos_hostname_override = kerberos_hostname_override
        self.message_encryption = message_encryption
        self.credssp_disable_tlsv1_2 = credssp_disable_tlsv1_2
        self.send_cbt = send_cbt
        self.keytab = keytab

    def get_kerb_ticket(self, generate_kerb_conf=False):
        set_kerb_pwd(username=self.username,
                     password=self.password,
                     realm=self.realm,
                     ad_server=self.ad_server,
                     generate_kerb_conf=generate_kerb_conf)

    @property
    def connector(self):
        if self._connector is None:
            return aiohttp.TCPConnector(loop=self.loop,
                                        verify_ssl=self.verify_ssl,
                                        force_close=False)
