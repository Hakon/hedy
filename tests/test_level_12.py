
import hedy
import textwrap
from parameterized import parameterized
from test_level_01 import HedyTester

class TestsLevel12(HedyTester):
  level = 12

  def test_if_with_indent(self):
    code = textwrap.dedent("""\
    naam = 'Hedy'
    if naam = Hedy
        print 'koekoek'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      max_level=16)

  def test_if_with_equals_sign(self):
    code = textwrap.dedent("""\
    naam is 'Hedy'
    if naam = Hedy
        print 'koekoek'""")

    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")

    self.multi_level_tester(
      code=code,
      expected=expected,
      expected_commands=['is', 'if', 'print'],
      max_level=16)

  # print tests
  def test_print_float(self):
    code = textwrap.dedent("""\
    pi is 3.14
    print pi""")
    expected = textwrap.dedent("""\
    pi = 3.14
    print(f'{pi}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  # issue #745
  def test_print_list_gives_type_error(self):
    code = textwrap.dedent("""\
    plaatsen is 'een stad', 'een  dorp', 'een strand'
    print plaatsen""")

    self.multi_level_tester(
      code=code,
      max_level=14,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_print_list_access(self):
    code = textwrap.dedent("""\
    animals is 'cat', 'dog', 'platypus'
    print animals at random""")

    expected = textwrap.dedent("""\
    animals = ['cat', 'dog', 'platypus']
    print(f'{random.choice(animals)}')""")

    self.multi_level_tester(
      code=code,
      max_level=14,
      expected=expected,
      expected_commands=['is', 'print', 'random']
    )

  # ask tests
  def test_ask_number_answer(self):
    code = textwrap.dedent("""\
    prijs is ask 'hoeveel?'
    gespaard is 7
    sparen is prijs - gespaard
    print 'hallo' sparen""")
    expected = textwrap.dedent("""\
    prijs = input(f'hoeveel?')
    try:
      prijs = int(prijs)
    except ValueError:
      try:
        prijs = float(prijs)
      except ValueError:
        pass
    gespaard = 7
    sparen = prijs - gespaard
    print(f'hallo{sparen}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_ask_with_list_var(self):
    code = textwrap.dedent("""\
      colors is 'orange', 'blue', 'green'
      favorite is ask 'Is your fav color' colors at 1""")

    expected = textwrap.dedent("""\
      colors = ['orange', 'blue', 'green']
      favorite = input(f'Is your fav color{colors[1-1]}')
      try:
        favorite = int(favorite)
      except ValueError:
        try:
          favorite = float(favorite)
        except ValueError:
          pass""")

    self.multi_level_tester(
      max_level=14,
      code=code,
      expected=expected
    )

  def test_ask_with_string_var(self):
    code = textwrap.dedent("""\
      color is 'orange'
      favorite is ask 'Is your fav color' color""")

    expected = textwrap.dedent("""\
      color = 'orange'
      favorite = input(f'Is your fav color{color}')
      try:
        favorite = int(favorite)
      except ValueError:
        try:
          favorite = float(favorite)
        except ValueError:
          pass""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  @parameterized.expand(['10', '10.0'])
  def test_ask_with_number_var(self, number):
    code = textwrap.dedent(f"""\
      number is {number}
      favorite is ask 'Is your fav number' number""")

    expected = textwrap.dedent(f"""\
      number = {number}
      favorite = input(f'Is your fav number{{number}}')
      try:
        favorite = int(favorite)
      except ValueError:
        try:
          favorite = float(favorite)
        except ValueError:
          pass""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  #list tests
  def test_ask_with_list_gives_type_error(self):
    code = textwrap.dedent("""\
      colors is 'orange', 'blue', 'green'
      favorite is ask 'Is your fav color' colors""")

    self.multi_level_tester(
      max_level=14,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_assign_random_value(self):
    code = textwrap.dedent("""\
    dieren is 'hond', 'kat', 'kangoeroe'
    dier is dieren at random
    print dier""")

    expected = textwrap.dedent("""\
    dieren = ['hond', 'kat', 'kangoeroe']
    dier = random.choice(dieren)
    print(f'{dier}')""")

    list = ['Hond', 'Kat', 'Kangoeroe']

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.result_in(list),
      max_level=15)

  def test_list_comma(self):
    code = textwrap.dedent("""\
    voorspellingen = 'je wordt rijk' , 'je wordt verliefd' , 'je glijdt uit over een bananenschil'
    print 'Ik pak mijn glazen bol erbij...'
    print 'Ik zie... Ik zie...'
    sleep 2
    print voorspellingen at random""")

    expected = textwrap.dedent("""\
    voorspellingen = ['je wordt rijk', 'je wordt verliefd', 'je glijdt uit over een bananenschil']
    print(f'Ik pak mijn glazen bol erbij...')
    print(f'Ik zie... Ik zie...')
    time.sleep(2)
    print(f'{random.choice(voorspellingen)}')""")

    list = ['je wordt rijk', 'je wordt verliefd', 'je glijdt uit over een bananenschil']

    self.multi_level_tester(
      code=code,
      expected=expected,
      extra_check_function=self.result_in(list),
      max_level=15)

  def test_if_in_list_with_string_var_gives_type_error(self):
    code = textwrap.dedent("""\
    items is 'red'
    if 'red' in items
        print 'found!'""")
    self.multi_level_tester(
      max_level=16,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_equality_with_list_gives_error(self):
    code = textwrap.dedent("""\
    color is 5, 6, 7
    if 1 is color
        print 'success!'""")
    self.multi_level_tester(
      max_level=15,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  def test_equality_with_incompatible_types_gives_error(self):
    code = textwrap.dedent("""\
    a is 'test'
    b is 15
    if a is b
      c is 1""")
    self.multi_level_tester(
      max_level=16,
      code=code,
      exception=hedy.exceptions.InvalidTypeCombinationException
    )

  # new calculations
  def test_int_addition_directly(self):
    code = textwrap.dedent("""\
            print 2 + 2""")
    expected = textwrap.dedent("""\
            print(f'{2 + 2}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_float_addition_directly(self):
    code = textwrap.dedent("""\
            print 2.5 + 2.5""")
    expected = textwrap.dedent("""\
            print(f'{2.5 + 2.5}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_float_addition_with_string(self):
    code = textwrap.dedent("""\
            print 'het antwoord is ' 2.5 + 2.5""")
    expected = textwrap.dedent("""\
            print(f'het antwoord is {2.5 + 2.5}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_float_addition_in_var(self):
    code = textwrap.dedent("""\
            antwoord is 2.5 + 2.5
            print antwoord
            """)
    expected = textwrap.dedent("""\
            antwoord = 2.5 + 2.5
            print(f'{antwoord}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_float_addition_with_var(self):
    code = textwrap.dedent("""\
            getal1 is 5
            getal2 is 4.3
            print 'dat is dan: ' getal1 + getal2
            """)
    expected = textwrap.dedent("""\
            getal1 = 5
            getal2 = 4.3
            print(f'dat is dan: {getal1 + getal2}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_store_calc_in_var(self):
    code = textwrap.dedent("""\
            a is 1
            b is 2
            c is a + b
            print c ' is 3'""")
    expected = textwrap.dedent("""\
            a = 1
            b = 2
            c = a + b
            print(f'{c} is 3')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_add_3_string_vars(self):
    code = textwrap.dedent("""\
            getal1 is '5'
            getal2 is '6'
            getal3 is '7'
            print 'dat is dan: ' getal1 + getal2 + getal3""")
    expected = textwrap.dedent("""\
            getal1 = '5'
            getal2 = '6'
            getal3 = '7'
            print(f'dat is dan: {getal1 + getal2 + getal3}')""")

    check_output = (lambda x: HedyTester.run_code(x) == 'dat is dan: 567')

    self.multi_level_tester(
      code=code,
      max_level=12,
      expected=expected,
      extra_check_function=check_output
    )

  def test_add_int_vars(self):
    code = textwrap.dedent("""\
            getal1 is 5
            getal2 is 6
            print 'dat is dan: ' getal1 + getal2""")
    expected = textwrap.dedent("""\
            getal1 = 5
            getal2 = 6
            print(f'dat is dan: {getal1 + getal2}')""")

    check_output = (lambda x: HedyTester.run_code(x) == 'dat is dan: 11')

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected,
      extra_check_function=check_output
    )

  def test_assign_string_with_quotes(self):
    code = textwrap.dedent("""\
            name is 'felienne'
            print name""")
    expected = textwrap.dedent("""\
            name = 'felienne'
            print(f'{name}')""")
    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_assign_string_with_quotes_and_string_value(self):
    code = textwrap.dedent("""\
            name is 'felienne'
            print 'hallo ' name""")
    expected = textwrap.dedent("""\
            name = 'felienne'
            print(f'hallo {name}')""")
    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_print_multiple_calcs(self):
    code = textwrap.dedent("""\
            name is 1 + 2 + 3
            print name""")

    expected = textwrap.dedent("""\
            name = 1 + 2 + 3
            print(f'{name}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_calc_string_and_int_gives_type_error(self):
    code = textwrap.dedent("""\
      x is 'test1'
      y is x + 1""")

    self.multi_level_tester(
      code=code,
      exception=hedy.exceptions.InvalidTypeCombinationException
    )

  def test_print_chained_assignments(self):
    code = textwrap.dedent("""\
            x is 1 + 2
            y is x + 3
            print y + 4""")

    expected = textwrap.dedent("""\
            x = 1 + 2
            y = x + 3
            print(f'{y + 4}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_assign_calc(self):
    code = textwrap.dedent("""\
            var is 5
            print var + 5""")

    expected = textwrap.dedent("""\
            var = 5
            print(f'{var + 5}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected
    )

  def test_calc_assign_equals(self):
    code = "nummer = 4 + 5"
    expected = "nummer = 4 + 5"
    self.multi_level_tester(
      code=code,
      expected=expected)

  # def test_access_variable_before_definition(self):
  #   code = textwrap.dedent("""\
  #           a is b
  #           b is 3
  #           print a""")
  #
  #   expected = textwrap.dedent("""\
  #           a = b
  #           b = 3
  #           print(f'{a}')""")
  #
  #   self.multi_level_tester(
  #     code=code,
  #     max_level=17,
  #     expected=expected,
  #     extra_check_function=self.is_not_turtle(),
  #     test_name=self.name()
  #   )

  def test_list_creation_with_spaces(self):
    code = textwrap.dedent("""\
    actions is 'clap your hands', 'stomp your feet', 'shout Hurray'
    for action in actions
        for i in range 1 to 2
            print 'if youre happy and you know it'
            print action
        print 'if youre happy and you know it and you really want to show it'
        print 'if youre happy and you know it'
        print action""")
    expected = textwrap.dedent("""\
    actions = ['clap your hands', 'stomp your feet', 'shout Hurray']
    for action in actions:
      step = 1 if int(1) < int(2) else -1
      for i in range(int(1), int(2) + step, step):
        print(f'if youre happy and you know it')
        print(f'{action}')
        time.sleep(0.1)
      print(f'if youre happy and you know it and you really want to show it')
      print(f'if youre happy and you know it')
      print(f'{action}')
      time.sleep(0.1)""")


    self.single_level_tester(code=code, expected=expected)

  def test_list_creation_with_numbers(self):
    code = textwrap.dedent("""\
    getallen is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    getal is getallen at random""")
    expected = textwrap.dedent("""\
    getallen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    getal = random.choice(getallen)""")


    self.single_level_tester(code=code, expected=expected)

  def test_if_quotes_in_condition(self):
    code = textwrap.dedent("""\
    naam is 'Hedy'
    if naam is 'Hedy'
        print 'koekoek'""")
    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')""")


    self.single_level_tester(code=code, expected=expected)

  def test_if_quotes_and_spaces_in_condition(self):
    code = textwrap.dedent("""\
    naam is 'Hedy is top'
    if naam is 'Hedy is top'
        print 'koekoek'""")
    expected = textwrap.dedent("""\
    naam = 'Hedy is top'
    if str(naam) == str('Hedy is top'):
      print(f'koekoek')""")


    self.single_level_tester(code=code, expected=expected)

  def test_if_else_quotes_in_condition(self):
    code = textwrap.dedent("""\
    naam is 'Hedy'
    if naam is 'Hedy'
        print 'koekoek'
    else
        print 'soepkip'""")
    expected = textwrap.dedent("""\
    naam = 'Hedy'
    if str(naam) == str('Hedy'):
      print(f'koekoek')
    else:
      print(f'soepkip')""")


    self.single_level_tester(code=code, expected=expected)

  def test_if_else_no_quotes_for_num_in_condition(self):
    code = textwrap.dedent("""\
    antwoord is ask 'Hoeveel is 10 plus 10?'
    if antwoord is 20
        print 'Goedzo!'
        print 'Het antwoord was inderdaad ' antwoord
    else
        print 'Foutje'
        print 'Het antwoord moest zijn ' antwoord""")

    expected = textwrap.dedent("""\
    antwoord = input(f'Hoeveel is 10 plus 10?')
    try:
      antwoord = int(antwoord)
    except ValueError:
      try:
        antwoord = float(antwoord)
      except ValueError:
        pass
    if str(antwoord) == str('20'):
      print(f'Goedzo!')
      print(f'Het antwoord was inderdaad {antwoord}')
    else:
      print(f'Foutje')
      print(f'Het antwoord moest zijn {antwoord}')""")



    self.single_level_tester(code=code, expected=expected)


  #add/remove tests
  def test_add_to_list(self):
    code = textwrap.dedent("""\
    color is ask 'what is your favorite color? '
    colors is 'green', 'red', 'blue'
    add color to colors
    print colors at random""")

    expected = textwrap.dedent("""\
    color = input(f'what is your favorite color? ')
    try:
      color = int(color)
    except ValueError:
      try:
        color = float(color)
      except ValueError:
        pass
    colors = ['green', 'red', 'blue']
    colors.append(color)
    print(f'{random.choice(colors)}')""")

    self.multi_level_tester(
      max_level=15,
      code=code,
      expected=expected
    )
  def test_remove_from_list(self):
    code = textwrap.dedent("""\
    colors is 'green', 'red', 'blue'
    color is ask 'what color to remove?'
    remove color from colors
    print colors at random""")

    expected = textwrap.dedent("""\
    colors = ['green', 'red', 'blue']
    color = input(f'what color to remove?')
    try:
      color = int(color)
    except ValueError:
      try:
        color = float(color)
      except ValueError:
        pass
    try:
        colors.remove(color)
    except:
       pass
    print(f'{random.choice(colors)}')""")


    self.multi_level_tester(
      max_level=15,
      code=code,
      expected=expected
    )

  # negative tests
  def test_assign_string_without_quotes(self):
    code = textwrap.dedent("""\
            name is felienne
            print name""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      exception=hedy.exceptions.UnquotedAssignTextException
    )
  
  def test_list_creation(self):
    code = textwrap.dedent("""\
    animals is 'duck', 'dog', 'penguin'""")
    expected = textwrap.dedent("""\
    animals = ['duck', 'dog', 'penguin']""")


    self.single_level_tester(code=code, expected=expected)

  def test_calc_chained_vars(self):
    code = textwrap.dedent("""\
      a is 5
      b is a + 1
      print a + b""")

    expected = textwrap.dedent("""\
      a = 5
      b = a + 1
      print(f'{a + b}')""")

    self.multi_level_tester(
      code=code,
      max_level=17,
      expected=expected,
      extra_check_function=lambda x: self.run_code(x) == "11"
    )
