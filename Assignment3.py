import time as t
import itertools
import re

kb = {}


# Classes

class Predicate:
    def __init__(self, name, args, negative=False):
        self.name = name
        self.args = args
        self.negative = negative
    
    def __str__(self):
        return f"{str(self.negative)+self.name + str(len(self.args))}"
    
    def __eq__(self, other):
        if isinstance(other, Predicate):
            return self.name == other.name and self.args == other.args and self.negative == other.negative
        return False

    def get_key(self):
        string = ""
        string+=str(self.name)
        for arg in self.args:
            string += arg
        return string

    def __hash__(self):
        return (hash(str(self.get_key())))

class Sentence:
    def __init__(self, predicates,noofpredicates):
        self.predicates = predicates
        self.noofpredicates = noofpredicates
    
    def __str__(self):
        return f"{'|'.join(str(predicate) for predicate in self.predicates)}"

    def __eq__(self, other):
        if isinstance(other, Sentence):
            return self.predicates == other.predicates
        return False
    
    def get_key(self):
        string = ""
        for p in self.predicates:
            string += str(p.get_key())
            string += "|"
        return string

    def __hash__(self):
        return hash(self.get_key())
    
# Main
def main():
    with open('input.txt', 'r') as f:
        extracted_data = f.readlines()

    data = [x.strip() for x in extracted_data]
    
    #  Two or more args will be separated by commas

    queries = data[0]
    n = int(data[1])

    # queries
    queries = [x.replace(' ','') for x in queries.split('),')]
    
    # sentences
    sentences = [x.replace(' ','') for x in data[2:]]

    # convert sentences to cnf and add to kb
    cnf_sentences = []
    for sentence in sentences:
        cnf_sentence = to_cnf(sentence)
        cnf_sentences.append(cnf_sentence)
        # makeKB(sentence)    

    # Standardize variables
    standardized_cnf_sentences = standardize(cnf_sentences)

    for sentence in standardized_cnf_sentences:
        makeKB(sentence)    


    # Resolution for queries 
    for query in queries:
        query = to_cnf(query)
        query = negate(query)
        makeKB(query)
        querys = changeQuerytoSentence(query)
        return resolution(querys,0)

# Convert to CNF
def distribute_or_over_and(sentence):
    disjuncts = sentence.split("|")
    conjuncts = []

    for disjunct in disjuncts:
        literals = disjunct.split("&")
        conjuncts.append(literals)


    product = itertools.product(*conjuncts)

    result = []
    for conjunct in product:
        result.append("|".join(conjunct))

    return "&".join(result)

def negate(sentence):
    if sentence[0]=='~':
        return sentence[1:]
    elif '&' in sentence:
        sub_exprs = [negate(e) for e in sentence.split('&')]
        return '|'.join(sub_exprs)
    elif '|' in sentence:
        sub_exprs = [negate(e) for e in sentence.split('|')]
        return '&'.join(sub_exprs)
    else:
        return '~' + sentence

def to_cnf(sentence):
    
    # 1. Eliminate ⇒, replacing α ⇒ β with ¬α ∨ β.
    # 2. Move ¬ inwards: ¬(α ∧ β) ≡ ¬α ∨ ¬β, ¬(α ∨ β) ≡ ¬α ∧ ¬β,  ¬¬α ≡ α
    # 3. (α ∧ β) ∨ γ ≡ (α ∨ γ) ∧ (β ∨ γ)
    
    idx = sentence.find('=>')
    if idx != -1:
        
        premise = negate(sentence[:idx]) 
        conclusion = sentence[idx+2:]
        sentence = premise + '|' + conclusion

        
    cnf_sentence = distribute_or_over_and(sentence)
    return cnf_sentence

# Convert to KB

def changeQuerytoSentence(cnf_sentence):
    conjuncts = cnf_sentence.split("&") 

    for conjunct in conjuncts:
        disjuncts = conjunct.split("|")
        sz = len(disjuncts)
        predicates = []

        for disjunct in disjuncts:
            p = makePredicates(disjunct,conjunct)
            predicates.append(p)

        s = Sentence(predicates,sz)
    
    return s

def makeKB(cnf_sentence):
    conjuncts = cnf_sentence.split("&") 

    for conjunct in conjuncts:
        disjuncts = conjunct.split("|")
        sz = len(disjuncts)
        predicates = []

        for disjunct in disjuncts:
            p = makePredicates(disjunct,conjunct)
            # p = str(p)
            predicates.append(p)

        s = Sentence(predicates,sz)

        for p in predicates:
            strv = str(p)
            if strv not in kb:
                kb[strv] = []

            kb[strv].append(s)        

def makePredicates(sentence,conjunct):
    args=[]
    bracSt = sentence.find('(')
    bracEnd = sentence.find(')')
    arguments= sentence[bracSt+1:bracEnd]
    commaInd = arguments.find(",")
    while(commaInd!=-1):
        args.append(arguments[:commaInd])
        arguments = arguments[commaInd+1:]
        commaInd=arguments.find(",")
    args.append(arguments)
    if(sentence[0]=="~"):
        isNeg = 1
        pred = sentence[1:bracSt]
    else:
        isNeg=0
        pred = sentence[:bracSt]
    
    p = Predicate(pred,args,isNeg)
    return p

def makeNegative(query):
    newq = ""
    querys = str(query)
    if(querys[0]=='1'):
        newq = '0'+querys[1:]
    else:
        newq = '1'+querys[1:]
    return newq

# Standardization

def get_const_value(variable_count):
    start = 2306 + variable_count
    constant = ""
    while start >= 26:
        constant = chr(97 + start % 26) + constant
        start //= 26
    return constant

def standardize(statements):
    variable_count = 0
    modified_cnf_statement = []
    for statement in statements:
        variables = {}
        r = re.compile('\([a-zA-Z,]+\)')
        args = r.findall(statement)
        args = (",".join(map(lambda x: x[1:-1], args))).split(",")
        args = list(set(filter(lambda x: x[0].islower(), args)))
        for arg in args:
            variables[arg] = get_const_value(variable_count)
            variable_count += 1
        
        predicate_list = []
        for predicate in statement.split("|"):
            parts = predicate.split("(")
            args = map(lambda x: variables[x] if x in variables else x, parts[1][:-1].split(","))
            predicate_list.append(parts[0] + "(" + ",".join(args) + ")")
        modified_cnf_statement.append("|".join(predicate_list))
    return modified_cnf_statement

# Resolution

def find(values, i):
    if i != values[i]:
        values[i] = find(values, values[i])
    return values[i]

def unify(p1, p2):
    values = {}
    for i in range(len(p1)):
        values[p1[i]] = p1[i]
        values[p2[i]] = p2[i]
        
    for i in range(len(p1)):
        arg1, arg2 = find(values, p1[i]), find(values, p2[i])
        if arg1[0].islower() and arg2[0].isupper():
            values[arg1] = arg2
        elif arg1[0].isupper() and arg2[0].islower():
            values[arg2] = arg1
        elif arg1[0].islower() and arg2[0].islower():
            values[arg2] = arg1
        elif arg1[0].isupper() and arg2[0].isupper():
            if arg1 != arg2:
                return 0, values

    return 1,values

def resolve(q,p,query,statement,height):
    flag, values = unify(q.args, p.args)
    if flag == 0:
        return False
    
    for i in range(len(p.args)):
        val1, val2 = find(values, q.args[i]), find(values, p.args[i])
        if val1 != val2:
            return False

    
    local_predicates = []
    
    for predicate in query.predicates:
        for i in range(len(predicate.args)):
            predicate.args[i] = find(values, predicate.args[i]) if predicate.args[i] in values else predicate.args[i]

        new_pred = Predicate(predicate.name,predicate.args,predicate.negative)
        local_predicates.append(new_pred)

    for predicate in statement.predicates:
        for i in range(len(predicate.args)):
            predicate.args[i] = find(values, predicate.args[i]) if predicate.args[i] in values else predicate.args[i]

        new_pred = Predicate(predicate.name,predicate.args,predicate.negative)
        local_predicates.append(new_pred)
        
    to_remove = []
    for i in range(len(local_predicates)):
        for j in range(i+1,len(local_predicates)):
            if local_predicates[i].get_key()==local_predicates[j].get_key() and local_predicates[i].negative!=local_predicates[j].negative:
                to_remove.append(local_predicates[j])
                to_remove.append(local_predicates[i])
            if local_predicates[i].get_key()==local_predicates[j].get_key() and local_predicates[i].negative==local_predicates[j].negative:
                to_remove.append(local_predicates[i])

    for m in to_remove:
        if m in local_predicates:
            local_predicates.remove(m) 

    
    if len(local_predicates) == 0:
        return True
    
    new_sentence = Sentence(local_predicates,len(local_predicates))
    # print("New Query: ", new_sentence)
    
    return resolution(new_sentence,height+1)
    

def resolution(query, height):
    if query == "":
        return True
    
    if height>(len(kb)*100):
        return False

    for q in query.predicates:
        qneg = makeNegative(q)

        if qneg[0]=='1' and (qneg in kb):
            statements = kb[qneg]
            for statement in statements:
                for p in statement.predicates:
                    if p.name == q.name and p.negative != q.negative:
                        if all(argument[0].isupper() for argument in q.args) and all(argument[0].isupper() for argument in p.args) and (q.args != p.args):
                            continue
                        if resolve(q, p, query, statement,height):
                            return True

        elif qneg[0]=='0' and (qneg in kb):
            statements = kb[qneg]
            for statement in statements:
                for p in statement.predicates:
                    if p.name == q.name and p.negative != q.negative:
                        if resolve(q, p, query, statement,height):
                            return True
    return False


if __name__=='__main__':
    # read the file-----------
    # st = t.process_time()
    answer = main()
    if answer:
        with open('output.txt','w') as f:
            f.write("TRUE")
            f.close()
    else:
        with open('output.txt','w') as f:
            f.write("FALSE")
            f.close()
    # end = t.process_time()
    # print("time ",end-st)