'''
Call the following RestfulAPI to deploy ModuleConfig.xml file to gateway:
1. Get token
    Request type: POST
    URL: https://us-s1.anylink.io:8443/user/getToken
    Parameters: JSON
    {
        "tenantEname": "nvisualai",
        "name": "admin",
        "password": "your_password_here"
    }
    Response:
    {
        "status":"100",
        "data":"dc91c34b-6a11-437a-ab8e-fa6fdc3e547b"
    }
    status:
        100: successful
        103: invalid parameter
        107: tenant name not exist
        109: unknown username
        115: this user is locked
        116: error password
        111:other errors
    msg:	Detail error message
    data:	Token

2. Deploy config file
    POST
    URL: https://us-s1.anylink.io:8443/v2/remoteAgent/sendAnylinkXML
    JSON parameters:
        {
            token: "data from /user/getToken response",
            filetype: "config_xml",
            serialNumber: 1801702,
            content: "<agent>...</agent>"
        }
    Response:
    {
        "status":"100",
        "data":"1534311799247"
    }
3. After config file deployment, poll the following interface to get deployment result, call once every 1 second.
   Stop polling when the status in Response is one of the following values:
        100: successful,
        102: Timeout
        103: parameter error,
        104: invalid token
        122: AnyLink box is waiting to register.
        123: Registration failed
        125: Get status failed because AnyLink box is offline.
        126: Registering
        111: For some other errors, refer to the "msg" value.
    GET
    URL: https://us-s1.anylink.io:8443/agent/register
    JSON parameters:
        {
            token: "your_token_here"
            serialNumber: "config_xml",
            serialNumber: 1801702,
            registerID: "data from /v2/remoteAgent/sendAnylinkXML response"
        }
    Response:
    {
        "status": "100"
    }
'''

import requests
import time
import json
import logging
from typing import Optional, Dict, Any

# Parameters
TENANT_ENAME = "nvisualai"
USERNAME = "admin"
PASSWORD = "ycoBxFMtEPp@20"
SERIAL_NUMBER = 1801702
CONFIG_FILE_PATH = "C:\\Users\\AnyLink\\Desktop\\1801702.xml"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AnyLinkConfigDeployer:
    """AnyLink Config File Deployer"""
    
    def __init__(self, base_url: str = "https://us-s1.anylink.io:8443"):
        self.base_url = base_url
        self.token: Optional[str] = None
        
    def get_token(self, tenant_ename: str, username: str, password: str) -> bool:
        """
        Get authentication token
        
        Args:
            tenant_ename: Tenant English name
            username: Username
            password: Password
            
        Returns:
            bool: Whether token was obtained successfully
        """
        url = f"{self.base_url}/user/getToken"
        payload = {
            "tenantEname": tenant_ename,
            "name": username,
            "password": password
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            status = result.get("status")
            
            if status == "100":
                self.token = result.get("data")
                logger.info("Token obtained successfully")
                return True
            else:
                error_msg = self._get_error_message(status)
                logger.error(f"Failed to get token: {error_msg}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while requesting token: {e}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error occurred while parsing token response: {e}")
            return False
    
    def send_config_file(self, serial_number: int, config_content: str) -> Optional[str]:
        """
        Send config file to device
        
        Args:
            serial_number: Device serial number
            config_content: Config file content (XML format)
            
        Returns:
            Optional[str]: Register ID for subsequent status polling
        """
        if not self.token:
            logger.error("No valid token obtained, please call get_token method first")
            return None
            
        url = f"{self.base_url}/v2/remoteAgent/sendAnylinkXML"
        payload = {
            "token": self.token,
            "filetype": "config_xml",
            "serialNumber": serial_number,
            "content": config_content
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            status = result.get("status")
            
            if status == "100":
                register_id = result.get("data")
                logger.info(f"Config file sent successfully, register ID: {register_id}")
                return register_id
            else:
                logger.error(f"Failed to send config file, status code: {status}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while sending config file: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error occurred while parsing send response: {e}")
            return None
    
    def poll_deployment_status(self, serial_number: int, register_id: str, max_attempts: int = 300) -> bool:
        """
        Poll config file deployment status
        
        Args:
            serial_number: Device serial number
            register_id: Register ID
            max_attempts: Maximum polling attempts (default 300 times, i.e. 5 minutes)
            
        Returns:
            bool: Whether deployment was successful
        """
        if not self.token:
            logger.error("No valid token obtained")
            return False
            
        url = f"{self.base_url}/agent/register"
        params = {
            "token": self.token,
            "serialNumber": serial_number,
            "registerID": register_id
        }
        
        attempt = 0
        while attempt < max_attempts:
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                status = result.get("status")
                status_msg = self._get_register_error_message(status)
                
                if status == "100":
                    logger.info(f"Config file deployed successfully (status: {status} - {status_msg})")
                    return True
                elif status in ["102", "103", "104", "123", "111"]:
                    msg = result.get("msg", "")
                    logger.error(f"Config file deployment failed (status: {status} - {status_msg}). {msg}")
                    return False
                else:
                    # Continue polling for status 122, 125, 126 and other unknown status
                    attempt += 1
                    logger.info(f"Polling... attempt {attempt}, status: {status} - {status_msg}")
                    time.sleep(1)
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error occurred while polling status: {e}")
                attempt += 1
                time.sleep(1)
            except json.JSONDecodeError as e:
                logger.error(f"Error occurred while parsing polling response: {e}")
                attempt += 1
                time.sleep(1)
        
        logger.error(f"Polling timeout, attempted {max_attempts} times")
        return False
    
    def deploy_config(self, tenant_ename: str, username: str, password: str, 
                     serial_number: int, config_content: str) -> bool:
        """
        Complete config file deployment process
        
        Args:
            tenant_ename: Tenant English name
            username: Username
            password: Password
            serial_number: Device serial number
            config_content: Config file content
            
        Returns:
            bool: Whether deployment was successful
        """
        logger.info("Starting config file deployment process")
        
        # 1. Get token
        if not self.get_token(tenant_ename, username, password):
            return False
        
        # 2. Send config file
        register_id = self.send_config_file(serial_number, config_content)
        if not register_id:
            return False
        
        # 3. Poll deployment status
        return self.poll_deployment_status(serial_number, register_id)
    
    @staticmethod
    def _get_error_message(status: str) -> str:
        """Get error message corresponding to status code"""
        error_messages = {
            "103": "Invalid parameter",
            "107": "Tenant name does not exist",
            "109": "Unknown username",
            "115": "User is locked",
            "116": "Wrong password",
            "111": "Other error"
        }
        return error_messages.get(status, f"Unknown error status: {status}")
    
    @staticmethod
    def _get_register_error_message(status: str) -> str:
        """Get registration error message corresponding to status code"""
        error_messages = {
            "100": "Successful",
            "102": "Timeout",
            "103": "Parameter error",
            "104": "Invalid token",
            "122": "AnyLink box is waiting to register",
            "123": "Registration failed",
            "125": "Get status failed because AnyLink box is offline",
            "126": "Registering",
            "111": "For some other errors, refer to the msg value"
        }
        return error_messages.get(status, f"Unknown error status: {status}")


def load_config_file(file_path: str) -> Optional[str]:
    """
    Load config content from file
    
    Args:
        file_path: Config file path
        
    Returns:
        Optional[str]: Config file content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Config file not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error occurred while reading config file: {e}")
        return None


def main():
    """Main function"""
    # Create deployer instance
    deployer = AnyLinkConfigDeployer()
    
    # Load config file
    config_content = load_config_file(CONFIG_FILE_PATH)
    if not config_content:
        logger.error("Unable to load config file")
        return
    
    # Execute deployment
    success = deployer.deploy_config(
        tenant_ename=TENANT_ENAME,
        username=USERNAME,
        password=PASSWORD,
        serial_number=SERIAL_NUMBER,
        config_content=config_content
    )
    
    if success:
        logger.info("Config file deployment completed")
    else:
        logger.error("Config file deployment failed")


if __name__ == "__main__":
    main()
