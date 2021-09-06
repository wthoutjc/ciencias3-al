



class Token:

   def __init__(self, token_type='UNKNOWN', value=None, string='', line=-1, col=-1):
      self.category = token_type
      self.position = line, col
      self.symbol = string
      self.value = value

   def __str__(self):
      return f'{self.position[0]:>3d} {self.symbol:^20} {self.category:<22} {self.value:^20}'

   def __repr__(self):
      return f'{self.position[0]:>3d} {self.symbol:^20} {self.category:<22} {self.value:^20}'