# CNSH Runtime — L1+L2 Syntax + Parser
from .command import CNSHCommand, Domain
from .parser  import parse, parse_safe, CNSHParser
from .router  import dispatch
