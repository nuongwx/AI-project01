import itertools
class Fact:
   def __init__(self, op='', args=[], negated=False):
      self.op = op      
      self.args = args           
      self.negated = negated   

   def __repr__(self):
      return '{}({})'.format(self.op, ', '.join(self.args))

   def __lt__(self, rhs):
      if self.op != rhs.op:
         return self.op < rhs.op
      if self.negated != rhs.negated:
         return self.negated < rhs.negated
      return self.args < rhs.args

   def __eq__(self, rhs):
      if self.op != rhs.op:
         return False
      if self.negated != rhs.negated:
         return False
      return self.args == rhs.args

   def __hash__(self):
      return hash(str(self))
   
   def copy(self):
      return Fact(self.op, self.args.copy(), self.negated)

   def negate(self):
      self.negated = 1 - self.negated

   def get_args(self):
      return self.args

   def get_op(self):
      return self.op

   @staticmethod
   
   def get_fact(fact_line):
      
      fact_line = fact_line.strip().rstrip('.').replace(' ', '')
      sep_index = fact_line.index('(')
      # Op and args are separated by '('
      op = fact_line[:sep_index]
      args = fact_line[sep_index + 1 : -1].split(',')
      return Fact(op, args)
   
class Substitution:
   def __init__(self):
      self.mappings = dict()

   def __repr__(self):
      return ', '.join('{} = {}'.format(key, value) for key, value in self.mappings.items())

   def __eq__(self, rhs):
      return self.mappings == rhs.mappings
   
   def __hash__(self):
      return hash(frozenset(self.mappings.items()))
   # Check if substitution is empty
   def empty(self):
      return len(self.mappings) == 0
   # Check if var is in mappings
   def contains(self, var):
      return var in self.mappings
   # Get the value of var in mappings
   def substitute_of(self, var):
      return self.mappings[var]
   # Substitute var with x in mappings
   def substitute(self, fact):
      for idx, arg in enumerate(fact.args):
         if self.contains(arg):
            fact.args[idx] = self.substitute_of(arg)
   # Add var = x to mappings
   def add(self, var, x):
      self.mappings[var] = x 

class Rule:
   def __init__(self, conclusion=Fact(), premises=[]):
      self.conclusion = conclusion      
      self.premises = premises          
      self.ops = self.get_ops()           

      self.premises.sort()
      self.dup_predicate = self.duplicate_predicate()

   def __repr__(self):
      return '{} => {}'.format(' & '.join([str(cond) for cond in self.premises]), str(self.conclusion))
   
   def copy(self):
      return Rule(self.conclusion.copy(), self.premises.copy())
   # Get number of premises
   def number_of_premises(self):
      return len(self.premises)
   # Get all operators in premises
   def get_ops(self):
      ops = set()
      for premise in self.premises:
         ops.add(premise.op)
      return ops
   # Check if a fact can be used as a premise
   def maybe_helpful(self, fact_op):
      return fact_op in self.ops
   # Check if any fact pi in new_facts is unified with a premise in rule
   def maybe_triggered(self, new_facts):
      for new_fact in new_facts:
         for premise in self.premises:
            if unify(new_fact, premise, Substitution()):
               return True
      return False
   # Check if there are duplicate predicates in premises
   def duplicate_predicate(self):
      num_premises = self.number_of_premises()
      for i in range(num_premises - 1):
         if self.premises[i].op == self.premises[i + 1].op:
            return True
      return False

   @staticmethod
   def get_rule(rule_str):       
      # Example: daughter(Person, Parent) :- female(Person), parent(Parent, Person).
      rule_str = rule_str.strip().rstrip('.').replace(' ', '')
      sep_index = rule_str.find(':-')

      # Get conclusion (lhs) and premises (rhs) seperated by ':-'
      conclusion = Fact.get_fact(rule_str[: sep_index])
      premises = []
      list_fact_str = rule_str[sep_index + 2:].split('),')
      # Add ')' to the last fact
      for idx, fact_line in enumerate(list_fact_str):
         if idx != len(list_fact_str) - 1:
            fact_line += ')'
         fact = Fact.get_fact(fact_line)
         premises.append(fact)

      return Rule(conclusion, premises)
   
class KB:
   def __init__(self):
      self.facts = set()
      self.rules = []
   # Add fact to knowledge base
   def add_fact(self, fact):
      self.facts.add(fact)
   # Add rule to knowledge base
   def add_rule(self, rule):
      self.rules.append(rule)
   # Query alpha
   def query(self, alpha):
      return forward_chaining(self, alpha)
   # Get potential facts to be used as premises
   def get_potential_facts(self, rule):
      facts = []
      for fact in self.facts:
         if rule.maybe_helpful(fact.op):
            facts.append(fact)
      return facts

   @staticmethod
   # Learn facts and rules from knowledge base
   def learn(kb, string_list):
      # Read knowledge base line by line
      while string_list:
         sent_string, string_list = next_line(string_list)
         sent_type = classify(sent_string)
         if sent_type == 'fact':
            fact = Fact.get_fact(sent_string)
            kb.add_fact(fact)
         elif sent_type == 'rule':
            rule = Rule.get_rule(sent_string)
            kb.add_rule(rule)

def is_variable(x):
   return isinstance(x, str) and x[0].isupper()

def is_compound(x):
   return isinstance(x, Fact)

def is_list(x):
   return isinstance(x, list)

# Unify two facts
def unify(x, y, theta):
   if theta is False:
      return False
   if x == y:   
      return theta
   if is_variable(x):
      return unify_var(x, y, theta)
   if is_variable(y):
      return unify_var(y, x, theta)
   if is_compound(x) and is_compound(y):
      return unify(x.get_args(), y.get_args(), unify(x.get_op(), y.get_op(), theta))
   if is_list(x) and is_list(y) and len(x) == len(y):
      return unify(x[1:], y[1:], unify(x[0], y[0], theta))
   return False
# Unify a variable and a compound
def unify_var(var, x, theta):
   # If var is a variable and x is a compound, check if var occurs in x
   if theta.contains(var):
      return unify(theta.substitute_of(var), x, theta)
   # If var is a variable and x is not a compound, check if var occurs in x
   if theta.contains(x):
      return unify(var, theta.substitute_of(x), theta)
   theta.add(var, x)
   return theta
# Classify a sentence
def classify(sent_string):
   sent_string = sent_string.strip()
   if not sent_string:
      return 'blank'
   if sent_string.startswith('/*') and sent_string.endswith('*/'):
      return 'comment'
   if ':-' in sent_string:
      return 'rule'
   return 'fact'

def next_line(inp_str):
   idx = 0
   nxt_string = inp_str[idx].strip()
   if nxt_string.startswith('/*'):          
      while not nxt_string.endswith('*/'):
         idx += 1
         nxt_string += inp_str[idx].strip()
   elif nxt_string:                        
      while not nxt_string.endswith('.'):
         idx += 1
         nxt_string += inp_str[idx].strip()

   return nxt_string, inp_str[idx + 1:]
# Check if two facts can be unified
def subst(facts_1, facts_2):          
   if len(facts_1) != len(facts_2):
      return False

   for f1, f2 in zip(facts_1, facts_2):
      if f1.get_op() != f2.get_op():
         return False

   return unify(facts_1, facts_2, Substitution())
# Forward chaining algorithm
def forward_chaining(kb, alpha):
   res = set()
   # Check if alpha is a fact
   for fact in kb.facts:
      phi = unify(fact, alpha, Substitution())
      if phi:
         if phi.empty():
            res.add('true')
            return res
         res.add(phi)

   last_generated_facts = kb.facts.copy()

   while True:
      new_facts = set()
      # Check if any rule is triggered
      for rule in kb.rules:
         if not rule.maybe_triggered(last_generated_facts):
            continue

         num_premises = rule.number_of_premises()
         # Get potential facts to be used as premises
         potential_facts = kb.get_potential_facts(rule)

         # Generate all possible combinations of premises
         if not rule.dup_predicate:        
            potential_premises = itertools.combinations(sorted(potential_facts), num_premises)
         else:
            # If there are duplicate predicates, we need to consider all permutations
            potential_premises = itertools.permutations(potential_facts, num_premises)
         # Check if any combination of premises can be used to infer the conclusion
         for tuple_premises in potential_premises:
            premises = [premise for premise in tuple_premises]
            theta = subst(rule.premises, premises)
            if not theta:
               continue
                        
            new_fact = rule.conclusion.copy()
            theta.substitute(new_fact)
            
            if new_fact not in new_facts and new_fact not in kb.facts:
               new_facts.add(new_fact)
               phi = unify(new_fact, alpha, Substitution())
               if phi:
                  if phi.empty():
                     kb.facts.update(new_facts)
                     res.add('true')
                     return res
                  res.add(phi)

      last_generated_facts = new_facts
      if not new_facts:
         if not res:
            res.add('false')
         return res
      kb.facts.update(new_facts)

def initialize_knowledge_base(kb, input):
   with open(input, 'r') as f_in:
      knowledge = f_in.readlines()
      KB.learn(kb, knowledge)

   print('Initialized knowledge from file {}.'.format(input))
   return kb

def get_result(kb, query_file, output_file):
   with open(query_file, 'r') as f_query:
      with open(output_file, 'w') as f_out:
         for query_str in f_query.readlines():
            query = Fact.get_fact(query_str)
            query_str = str(query) + '.'
            results = set(kb.query(query))
            results_str = ' ;\n'.join([str(i) for i in results]) + '.\n'
            f_out.write(query_str + '\n')
            f_out.write(results_str + '\n')

if __name__ == "__main__":
   print('Enter test case: ', end='')

   test_case = input().strip()

   query_file = 'test/' + test_case + '/query.pl'
   input_file = 'test/' + test_case + '/knowledge_base.pl'
   output_file = 'test/' + test_case + '/answers.txt'

   kb = KB()
   kb = initialize_knowledge_base(kb, input_file)
   
   print("Processing")
   get_result(kb, query_file, output_file)
   print('Results  are written to {}.'.format(output_file))
