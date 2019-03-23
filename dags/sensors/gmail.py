import email
import re

from airflow.sensors.base_sensor_operator import BaseSensorOperator

from dags.sensors.mail import mailbox


class GmailSensor(BaseSensorOperator):
    def poke(self, context):
        mail = mailbox()
        result, data = mail.search(None, 'SINCE "19-Mar-2019"')

        ids = data[0]
        id_list = ids.split()
        id_list.reverse()
        for id in id_list:
            result, data = mail.fetch(id, "(RFC822)")
            mail = email.message_from_bytes(data[0][1])
            try:
                digits = re.findall(r'\d+', mail._payload[0]._payload)
                code = next(x for x in digits if len(x) == 6)
                if code is not None:
                    self.xcom_push(context, key='code', value=code)
                    return True
            except StopIteration:
                continue
        return False
