import random

relations = [('Asda ', 'subsidiary', ' Image copyrightGetty ImagesSainsbury'), ('Asda ', 'follows', ' plans'), ('combination ', 'subclass of', ' supermarkets'), ('Coupe ', 'subsidiary', ' Sainsbury'), ('Coupe ', 'subsidiary', ' Asda'), ('Coupe ', 'subsidiary', ' brands and no stores'), ('Argos ', 'manufacturer', ' merger'), ('Tesco ', 'instance of', ' combined business'), ('Tesco ', 'instance of', ' market'), ('Rebecca Long-Bailey ', 'member of political party', ' Labour'), ('Rebecca Long-Bailey ', 'employer', ' BBC'), ('Rebecca Long-Bailey ', 'member of', ' shadow'), ('Vince Cable ', 'position held', ' Sir'), ('Sainsbury ', 'subsidiary', ' Asda'), ('Sainsbury ', 'subsidiary', ' Aldi'), ('Amazon ', 'parent astronomical body', ' horizon'), ('Sainsbury ', 'instance of', ' market share perspective'), ('Sainsbury ', 'instance of', ' certain extent'), ('Asda ', 'instance of', ' market share perspective'), ('Steve Dresser ', 'instance of', ' rapid rate'), ('Sainsbury ', 'subclass of', ' chains'), ('Sainsbury ', 'instance of', ' many ways'), ('Dresser ', 'subclass of', ' standard organic growth'), ('Sainsbury ', 'subsidiary', ' Asda'), ('BBC News ', 'owned by', ' BBC'), ('BBC News ', 'owned by', ' page'), ('BBC News ', 'instance of', ' version')]


def build_question_from_relation(relations):
    subject = {
        'question': '',
        'choices': [],
        'answer': 'A'
    }
    # build the complete set of all possible relations to choose
    choices_complete_set = set()
    for relation in relations:
        choices_complete_set.add(relation[1])

    for relation in relations:
        question = 'What is the possible relationship between {0} and {1} can you infer from the passage?'.format(
            relation[0], relation[2])

        relations_to_choose = list(choices_complete_set)
        choice_A = relation[1]
        relations_to_choose.remove(choice_A)
        choice_B = random.choice(relations_to_choose)
        relations_to_choose.remove(choice_B)
        choice_C = random.choice(relations_to_choose)
        relations_to_choose.remove(choice_C)
        choice_D = random.choice(relations_to_choose)
        relations_to_choose.remove(choice_D)


que = build_question_from_relation(relations)

print()
