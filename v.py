"""A simple text editor with complete disregard for performance."""
import curses, time

class TextDisplay(object):
  def __init__(self, stdscr):
    self.stdscr = stdscr
    self.text = ''
    self.display_row = 0
    self.display_col = 0
    curses.curs_set(0)
    self.cursors = [0]

  @property
  def height(self):
    return self.stdscr.getmaxyx()[0]

  @property
  def width(self):
    return self.stdscr.getmaxyx()[1]

  def convert_coordinates(self, location):
    row = self.text[:location].count('\n')
    col = location - self.text.rfind('\n', 0, location) - 1
    return row, col

  def within_display_bounds(self, row, col):
    return (row - self.display_row in range(self.height) and
            col - self.display_col in range(self.width))

  def render(self):
    lines = self.extract_lines()
    self.render_lines(lines)
    self.render_cursors(lines)

  def extract_lines(self):
    return [line[self.display_col:self.width+self.display_col]
            for line in self.text.split('\n')[self.display_row:self.height]]

  def render_lines(self, lines):
    for line_number, line in enumerate(lines):
      self.stdscr.addstr(line_number, 0, line)

  def render_cursors(self, lines):
    for cursor in self.cursors:
      row, col = self.convert_coordinates(cursor)
      if self.within_display_bounds(row, col):
        relative_row = row - self.display_row
        relative_col = col - self.display_col
        ch = lines[relative_row][relative_col:relative_col+1] or ' '
        self.stdscr.addch(relative_row, relative_col, ch,
                          curses.A_BLINK | curses.A_REVERSE)

  def refresh(self):
    self.render()
    self.stdscr.refresh()

  def raw_insert(self, string, location):
    self.text = self.text[:location] + string + self.text[location:]

  def insert_at(self, string, location):
    self.cursors = [cursor if cursor < location else cursor + len(string)
                    for cursor in self.cursors]
    self.raw_insert(string, location)

  def insert(self, string):
    for cursor in self.cursors:
      self.insert_at(string, cursor)

def main(stdscr):
  display = TextDisplay(stdscr)
  display.insert("Hello world!\n\nSecond line!\n")
  display.insert("hi there! ")
  display.insert("Didn't see you there.\n")
  display.refresh()
  time.sleep(3)

if __name__ == '__main__':
  curses.wrapper(main)
