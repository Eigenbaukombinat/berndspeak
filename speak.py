import paho.mqtt.client as mqtt
import shlex
import logging
import os
import time
import tempfile

logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s '
                        '%(levelname)s %(message)s')
log = logging.getLogger(__name__)


mqtt_client = mqtt.Client()
mqtt_client.enable_logger(logger=log)
mqtt_client.connect('putin')
mqtt_client.subscribe('space/bernd/speak/chat')
mqtt_client.subscribe('space/bernd/speak/msg')
CMD_PSA = 'espeak -v mb-de4 -s 150 -a 100 -p 200 -f {} -w out.wav && play out.wav gain -3 reverb'
CMD = 'espeak -v mb-de4 -s 130 -a 100 -p 0 -f {}'

def run(tmpl, txt):
    idx, fn = tempfile.mkstemp()
    cmd = tmpl.format(fn)
    with open(fn, 'w') as tf:
        tf.write(txt)
    log.info("running cmd: {}".format(cmd))
    os.system(cmd)
    os.unlink(fn)


def mqtt_received(client, data, msg):
    text = msg.payload.decode('utf8')
    if msg.topic == 'space/bernd/speak/chat':
        splitted = text.split('#')
        if len(splitted) != 2:
            return
        name, speaktext = splitted
        run(CMD_PSA, "Nachricht aus dem tschätt von {}.".format(name))
    else:
        speaktext = text
    run(CMD, speaktext)

mqtt_client.on_message = mqtt_received
mqtt_client.loop_start()


while True:
    time.sleep(5)

