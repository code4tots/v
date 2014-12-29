import unittest, curses, v

try:
  from unittest import mock
except ImportError:
  import mock

@mock.patch('curses.curs_set')
class TextDisplayTestCase(unittest.TestCase):

  def setUp(self):
    self.mock_stdscr = mock.Mock(spec=['getmaxyx', 'addstr', 'addch'])

  def test_convert_coordinates(self, *ignored_mocks):
    text = ('hello\n'
            'world!\n')

    display = v.TextDisplay(None)
    display.insert(text)

    self.assertEqual(
        (0, 0),
        display.convert_coordinates(0))

    self.assertEqual(
        (1, 0),
        display.convert_coordinates(6))

    self.assertEqual(
        (1, 1),
        display.convert_coordinates(7))

if __name__ == '__main__':
  unittest.main()
