import pprint

class Payload():
	def __init__(
		self,
		length,
		TTL,
		IPProtocol,
		srcPort,
		dstPort,
		flags
	):
		assert(isinstance(length, int))
		self.length = length

		assert(isinstance(TTL, int))
		self.TTL = TTL

		assert(isinstance(IPProtocol, int))
		self.IPProtocol = IPProtocol

		assert(isinstance(srcPort, int))
		self.srcPort = srcPort

		assert(isinstance(dstPort, int))
		self.dstPort = dstPort

		assert(isinstance(flags, bytes))
		self.flags = flags


	@staticmethod
	def fromPySharkCapture(packet):
		payload = Payload(
			int(packet.ip.len),
			int(packet.ip.ttl),
			int(packet.ip.proto),
			int(packet.tcp.srcport),
			int(packet.tcp.dstport),
			packet.tcp.flags.binary_value
		)

		return payload


	def toVector(self):
		res = [
			self.length		/ 65535.,
			self.TTL		/ 255.	,
			self.IPProtocol / 377.	, # As per RFC 790
			self.srcPort	/ 65535.,
			self.dstPort	/ 65535.
		]

		flagsList = [0.0] * 9
		pos = 0
		for byte in self.flags:
			for i in range(8):
				bit = (byte >> i) & 0x01
				flagsList[pos] = (float(bit))
				pos += 1

		res += flagsList[:9]

		return res
	
	@staticmethod
	def vectorSize():
		return 14



	def __str__(self):
		pp = pprint.PrettyPrinter(indent = 4)

		res  = "---------------------------\n"

		res += "Source Data:\n"
		res += "Length:           [%d]\n"	% self.length
		res += "TTL:              [%d]\n"	% self.TTL
		res += "IP Protocol:      [%d]\n"	% self.IPProtocol
		res += "Source Port:      [%d]\n"	% self.srcPort
		res += "Destination Port: [%d]\n"	% self.dstPort
		res += "Flags             [%s]\n"	% self.flags
		res += "\n"
		res += "Vector Data:\n"
		res += "%s\n"						% pp.pformat(self.toVector())

		res += "---------------------------"
		return res

