# Copyright 2014 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Requires Python 2.4+ and Openssl 1.0+
#
# Implements parts of RFC 2131, 1541, 1497 and
# http://msdn.microsoft.com/en-us/library/cc227282%28PROT.10%29.aspx
# http://msdn.microsoft.com/en-us/library/cc227259%28PROT.13%29.aspx

import tests.env
import tests.tools as tools
from .tools import *
import uuid
import unittest
import os
import time
import json
from azurelinuxagent.protocol.common import *

extensionDataStr = """
{
    "vmAgent": {
        "agentVersion": "2.4.1198.689",
        "status": "Ready",
        "message": "GuestAgent is running and accepting new configurations."
    },
    "extensionHandlers": [{
            "handlerName": "Microsoft.Compute.CustomScript",
            "handlerVersion": "1.0.0.0",
            "status": "Ready",
            "message": "Plugin enabled (name: Microsoft.Compute.CustomScript, version: 1.0.0.0).",
            "extensionStatusList": [{
                "name": "MyDomainJoinScript",
                "configurationAppliedTime": "2014-08-12T19:20:18Z",
                "operation": "CommandExecutionFinished",
                "status": "Success",
                "sequenceNumber": "0",
                "substatusList": [{
                    "name": "StdOut",
                    "status": "Info",
                    "code": "0",
                    "message": "Joiningdomainfoo"
                }]
            }]
        }

    ]
}
"""

class TestProtocolContract(unittest.TestCase):
    def test_get_properties(self):
        data = get_properties(VMInfo())
        data = get_properties(Cert())
        data = get_properties(ExtensionPackageList())
        data = get_properties(InstanceMetadata())
        data = get_properties(VMStatus())
        data = get_properties(TelemetryEventList())
        data = get_properties(Extension(name="hehe"))
        self.assertTrue("name" in data)
        self.assertTrue("properties" in data)
        self.assertEquals(dict, type(data["properties"]))
        self.assertTrue("versionUris" not in data)

    def test_set_properties(self):
        data = json.loads(extensionDataStr)
        obj = VMStatus()
        set_properties(obj, data)
        self.assertNotEquals(None, obj.vmAgent)
        self.assertEquals(VMAgentStatus, type(obj.vmAgent))
        self.assertNotEquals(None, obj.vmAgent.status)
        self.assertNotEquals(None, obj.extensionHandlers)
        self.assertEquals(DataContractList, type(obj.extensionHandlers))

if __name__ == '__main__':
    unittest.main()

