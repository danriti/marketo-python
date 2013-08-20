
import unittest

import marketo
import marketo.auth


class ResponseMock(object):
    """ A mock object of a SOAP response.
    """
    def __init__(self):
        # Example soap response that allows for an insertion of an attribute
        # value for the lead record "LastName" attribute.
        self.SOAP_RESPONSE = u"""<?xml version="1.0" encoding="UTF-8"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns1="http://www.marketo.com/mktows/">
        <SOAP-ENV:Body>
          <ns1:successSyncLead>
            <result>
              <leadId>1234567</leadId>
              <syncStatus>
                <leadId>1234567</leadId>
                <status>UPDATED</status>
                <error xsi:nil="true"/>
              </syncStatus>
              <leadRecord>
                <Id>1234567</Id>
                <Email>someone@example.com</Email>
                <ForeignSysPersonId xsi:nil="true"/>
                <ForeignSysType xsi:nil="true"/>
                <leadAttributeList>
                  <attribute>
                    <attrName>Account_ID__c</attrName>
                    <attrType>string</attrType>
                    <attrValue>0000000000abcde</attrValue>
                  </attribute>
                  <attribute>
                    <attrName>LastName</attrName>
                    <attrType>string</attrType>
                    <attrValue>%s</attrValue>
                  </attribute>
                </leadAttributeList>
              </leadRecord>
            </result>
          </ns1:successSyncLead>
        </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>"""

        self.text = None


class ResponseAscii(ResponseMock):
    """ A mock object that implements a SOAP response containing all ASCII
        characters.
    """
    def __init__(self):
        super(ResponseAscii, self).__init__()
        ASCII_STR = u"Moller"
        self.text = self.SOAP_RESPONSE % (ASCII_STR)


class ResponseUnicode(ResponseMock):
    """ A mock object that implements a SOAP response containing mostly ASCII
        characters and a single Unicode character.
    """
    def __init__(self):
        super(ResponseUnicode, self).__init__()
        UNICODE_STR = u"M%cller" % unichr(244)
        self.text = self.SOAP_RESPONSE % (UNICODE_STR)


class MarketoBasicTests(unittest.TestCase):

    def test_auth(self):
        # From Marketo example"
        user_id = "bigcorp1_461839624B16E06BA2D663"
        encryption_key = "899756834129871744AAEE88DDCC77CDEEDEC1AAAD66"
        timestamp = "2010-04-09T14:04:54-07:00"
        signature = "ffbff4d4bef354807481e66dc7540f7890523a87"
        self.assertTrue(marketo.auth.sign(timestamp + user_id, encryption_key) == signature)

    def test_unwrap_ascii(self):
        """ Test the unwrap method with an an response containing all ASCII. """
        res = ResponseAscii()
        lead_record = marketo.wrapper.sync_lead.unwrap(res)
        self.assertIsInstance(lead_record, marketo.wrapper.lead_record.LeadRecord)

    def test_unwrap_unicode(self):
        """ Test the unwrap method with an response containing Unicode. """
        res = ResponseUnicode()
        lead_record = marketo.wrapper.sync_lead.unwrap(res)
        self.assertIsInstance(lead_record, marketo.wrapper.lead_record.LeadRecord)

if __name__ == '__main__':
    unittest.main()
