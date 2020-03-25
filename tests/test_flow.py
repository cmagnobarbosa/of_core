"""Tests for high-level Flow of OpenFlow 1.0 and 1.3."""
import unittest

from kytos.core.switch import Switch
from napps.kytos.of_core.v0x01.flow import Flow as Flow01
from napps.kytos.of_core.v0x04.flow import Flow as Flow04


class TestFlow(unittest.TestCase):
    """Test OF flow abstraction."""

    def test_flow_mod(self):
        """Convert a dict to flow and vice-versa."""
        switch = Switch('dpid')
        expected = {
            'id': '1ce5d08a46496fcb856cb603a5bfa00f',
            'switch': switch.id,
            'table_id': 1,
            'match': {
                'dl_src': '11:22:33:44:55:66'
            },
            'priority': 2,
            'idle_timeout': 3,
            'hard_timeout': 4,
            'cookie': 5,
            'actions': [
                {'action_type': 'set_vlan',
                 'vlan_id': 6}],
            'stats': {}}
        for flow_class in Flow01, Flow04:
            with self.subTest(flow_class=flow_class):
                flow = flow_class.from_dict(expected, switch)
                actual = flow.as_dict()
                self.assertDictEqual(expected, actual)
