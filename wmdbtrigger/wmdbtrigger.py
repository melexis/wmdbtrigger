"""
Wmdbtrigger - Send an event when a wafermap is added / updated to the wmdb

It sends events with the following format:

	Event { type: << event type,  one of [ NEW_WAFERMAP_IN_WMDB, UPDATED_WAFERMAP_IN_WMDB, DELETED_WAFERMAP_IN_WMDB ]
		from: << fully qualified hostname of the sender >>
		date: << timestamp in utf-8 format >>
		attributes: { hostname: << hostname of the wmdb where the event originated >>
			      port: << port of the wmdb file service >>
			      path: << string containing the path of the wafermap >> }}

To a topic event
"""
import stomp
import sys

class EventType:
  NEW_WAFERMAP_IN_WMDB='NEW_WAFERMAP_IN_WMDB'
  UPDATED_WAFERMAP_IN_WMDB='UPDATED_WAFERMAP_IN_WMDB'
  DELETED_WAFERMAP_IN_WMDB='DELETED_WAFERMAP_IN_WMDB'

class Wmdb:

  def __init__(self, hostname, port):
    self.hostname = hostname
    self.port = port

  def __repr__(self):
    return "Wmdb {hostname: %(hostname)s port: %(port)s}" % {'hostname': self.hostname, 'port': self.port}

class Event:

  def __init__(self, eventtype, sender, date, wmdb, wafermaptype, path):
    self.eventtype = eventtype
    self.sender = sender
    self.date = date
    self.wmdb = wmdb 
    self.wafermaptype = wafermaptype
    self.path = path

  def __repr__(self):
    return "Event {type: %(type)s from: %(from)s date: %(date)s wmdb: %(wmdb)s wafermaptype: %(wafermaptype)s %(path)s}" % {
        'type': self.eventtype,
        'from': self.sender,
        'date': self.date,
        'wmdb': self.wmdb,
        'wafermaptype': self.wafermaptype,
        'path': self.path}

def event_to_xml(event):
  """Convert an event to xml

     First import datetime to be able to work with dates
     >>> from datetime import datetime
     
     Given an event
     >>> timestamp = datetime(2012, 12, 7, 8, 56)
     >>> e = Event(EventType.NEW_WAFERMAP_IN_WMDB, 'sda.sensors.elex.be', timestamp, 
     ...   Wmdb('sda.sensors.elex.be', 6913), 'catmap', '/mnt/categorymaps/WC_A12345_1.th01')

     When the event is sent to event_to_xml then we get the event in xml format.
     >>> xml = event_to_xml(e)
  
     Clean the xml so we have a chance to compare it.
     >>> lines = map(lambda s: s.strip(), xml.split("\\n"))
     >>> '\\n'.join(lines)
     '<?xml version="1.0"?>\\n<event type="NEW_WAFERMAP_IN_WMDB" from="sda.sensors.elex.be" date="2012-12-07T08:56:00">\\n<attribute key="hostname" value="sda.sensors.elex.be" />\\n<attribute key="port" value="6913" />\\n<attribute key="path" value="/mnt/categorymaps/WC_A12345_1.th01" />\\n<attribute key="wafermaptype" value="catmap" />\\n</event>'
  """
  return """<?xml version="1.0"?>
     <event type="%(type)s" from="%(from)s" date="%(timestamp)s">
       <attribute key="hostname" value="%(hostname)s" />
       <attribute key="port" value="%(port)s" />
       <attribute key="path" value="%(path)s" />
       <attribute key="wafermaptype" value="%(wafermaptype)s" />
     </event>""" % {'type': event.eventtype,
                    'timestamp': event.date.isoformat(),
                    'from': event.sender,
                    'wafermaptype': event.wafermaptype,
                    'hostname': event.wmdb.hostname,
                    'port': event.wmdb.port,
                    'path': event.path}

def trigger(event, hostnames):
  """Send trigger to the queueservers on the hostnames

     Parameters
       event     - the event to send to the stomp server
       hostnames - list of lists of tuples with hostname and port of the queueserver. Hostnames, with failover, are grouped in the inner list.

     Example:  trigger(event, [[("ewaf-test.colo.elex.be", 61613)], [("esb-a-test.sensors.elex.be", 61501), ("esb-b-test.sensors.elex.be", 61501)]])

     This will send the trigger to "ewaf-test.colo.elex.be" and also to either "esb-a-test.sensors.elex.be" or "esb-b-test.sensors.elex.be" depending on which one is listening to the defined portnumber.

     Returns None"""

  def _send_trigger(event, hosts):
      c = stomp.Connection(hosts)
      try:
        c.start()
        c.connect()
        c.send(event_to_xml(event), destination='/topic/VirtualTopic.event')
      finally:
        c.stop()

  for hosts in hostnames:
    _send_trigger(event, hosts)

def test():
  import doctest
  doctest.testmod()

def usage():
  return """%s
  test - run the unit tests
"""

def main():
  if len(sys.argv) == 2 and 'test' == sys.argv[1]:
    print 'running tests'
    test()
  else:
    usage()

if __name__ == '__main__':
  main()
