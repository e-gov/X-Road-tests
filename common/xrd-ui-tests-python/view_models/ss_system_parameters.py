GENERATE_INTERNAL_TLS_KEY_BUTTON_ID = 'generate_internal_ssl'
EXPORT_INTERNAL_TLS_CERT_BUTTON_ID = 'export_internal_ssl_cert'
INTERNAL_TLS_CERT_HASH_ID = 'internal_ssl_cert_hash'
SERVICE_TIMEOUT_VALUE = '60'
WSDL_VALIDATOR_CONF_LOCATION = '/etc/xroad/conf.d/local.ini'
WSDL_VALIDATOR_WRAPPER_LOCATION = '/usr/share/xroad/wsdlvalidator/bin/wsdlvalidator_wrapper.sh'
RELOAD_APP_COMMAND = 'service xroad-jetty reload'
GLOBAL_CONF_EXPIRATION_TIME_IN_SECONDS = 660
CERTIFICATE_DETAILS_BUTTON_ID = 'cert_details'
BACKUP_CONFIGURATION_BUTTON_ID = 'backup'
BACKUP_UPLOAD_BUTTON_ID = 'backup_upload'
BACKUP_DUMP_LOCATION = '/var/lib/xroad/dbdump.dat'
BACKUP_DUMP_DIR1 = '/etc/xroad/'
BACKUP_DUMP_DIR2 = '/etc/nginx/sites-enabled/'
BACKUP_DUMP_VER = 'security_XROAD_6.8_KS1/GOV/TS2OWNER/TS2'
BACKUP_CORRUPTION_FILE = '/etc/xroad/conf.d/deletethisfile.ini'
BACKUP_CORRUPTION_FILE2 = '/var/lib/xroad/backup/deletethisfile.tar'
DELETE = "//button[contains(.,'Delete')]"
RESTORE = "//button[contains(.,'Restore')]"
DOWNLOAD = "//button[contains(.,'Download')]"

RESTORE_DUMP_CLEARING_SHARED_MEMORY = 'CLEARING SHARED MEMORY'
RESTORE_DUMP_STOPPING_SERVICES = 'STOPPING ALL SERVICES EXCEPT JETTY'
RESTORE_DUMP_PRERESTORE = 'Creating pre-restore backup archive to /var/lib/xroad/conf_prerestore_backup.tar:'
RESTORE_DUMP_CREATION = 'Creating database dump to /var/lib/xroad/dbdump.dat'
UPLOAD_BACKUP_FAILED = 'Upload backup file failed'
UPLOAD_BACKUP_SUCCESSFUL = 'Upload backup file'
CONFIRM_POPUP = "//div[@class='ui-dialog-content ui-widget-content']"
BACKUP_FILE_NAME ='#backup_files tbody td'
BACKUP_FILE_NAME_ROW = '//td[@class=" sorting_1"]'
CONFIRMATION = '#confirm'
BACKUP_RESTORE_EMPTY = ('//table[@id="backup_files"]//tr[@class="odd"]//td[@class="dataTables_empty"]')
SS_UPDATE_CONFRIM = '//div[@id="confirm"]'
EMPTY_ZIP_FILE = 'test.zip'
INVALID_CHARACTER_FILE = '@.tar'
EMPTY_TAR_FILE = 'test.tar'
SELECT_CLIENT_POPUP_XPATH = '//div[@aria-describedby = "confirm"]'
SELECT_CLIENT_POPUP_OK_BTN_XPATH = SELECT_CLIENT_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="Confirm"]'