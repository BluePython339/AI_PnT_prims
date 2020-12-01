"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Class for the implementation of the variable elimination algorithm.

"""
import pandas as pd
import itertools as it

class VariableElimination():

    def __init__(self, network):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.

        """
        self.network = network
        self.nodes = {}



    def classify_nodes(self):
        childs = []
        root = []
        leaf = []
        middle = []
        for i in self.network.parents.keys():
            childs += self.network.parents[i]##

        #print(childs)
        for i in self.network.parents.keys():
            if len(self.network.parents[i]) == 0:
                root.append(i)
            elif i not in childs:
                leaf.append(i)
            else:
                middle.append(i)
        return leaf+root+middle  

    def reduce_observed(self):
        for probs in self.network.probabilities.keys():
            self.network.probabilities[probs] = self.reduce_observed_single(self.network.probabilities[probs])

    def reduce_observed_single(self, df):            
        for i in self.observed:
            try:
                df = df[df[i] == self.observed[i]]
            except:
                pass
        return df


    def create_factors(self):
        factors = []
        for i in self.network.parents:
            factors.append(([i, *self.network.parents.get(i)],self.network.probabilities[i]))
        return factors

    def multiply_2(self, obj1, obj2):
        df1 = obj1[1]
        df2 = obj2[1]
        #size = (len(df1.columns) if len(df1.columns) > len(df2.columns) else len(df2.columns))
        #td = [[*i, 0] for i in it.product(["False", "True"], repeat=(len(obj1[0]) if len(obj1[0]) > len(obj2[0]) else len(obj2[0])))]
        #res = pd.DataFrame(td, columns=obj1[0]+["prob"] if len(obj1[0]) > len(obj2[0]) else obj2[0]+["prob"] )
        #res = self.reduce_observed_single(res)
        shared = list(set(obj1[0]).intersection(obj2[0]))
        large, it_l , small, it_s = (obj1[1], obj1[0] , obj2[1], obj2[0]) if len(obj1[0]) >= len(obj2[0]) else (obj2[1], obj2[0] , obj1[1], obj1[0]) 
        res = large.copy(deep=True)
        for index, row in large.iterrows():
            qdata = []
            for i in shared:
                qdata.append([i, row[i]])
            val1 = small.query(self.construct_query(qdata)).iloc[0]['prob']
            val2 = row['prob']
            new = val1*val2
            #print("{} * {} = {}".format(val1, val2, new))
            res.at[index, 'prob'] = new
        return [it_l, res]
                
    def construct_query(self, data):
        a = ""
        for i in data:
            a += '{} == "{}" & '.format(*i)
        a = a[:-2]
        return a
        
    def multiply_factors(self, multipliers):

        while len(multipliers) >= 2:
            #print(len(multipliers))
            obj1 = multipliers.pop(0)
            obj2 = multipliers.pop(0)
            res = self.multiply_2(obj1, obj2)
            multipliers.insert(0,res)
        return multipliers[0]

    def eliminate_var(self, obj, var):
        df = obj[1]
        obj[0].remove(var)
        try:
            obj[0].remove("prob")
        except:
            pass
        remainders = obj[0]
        remainders.append('prob')
        td = [[*i, 0.0] for i in it.product(["False", "True"], repeat=len(remainders)-1)]
        new_f = pd.DataFrame(td, columns=remainders )
        new_f = self.reduce_observed_single(new_f)
        remainders.remove("prob")
        for index, row in new_f.iterrows():
            qdata = []
            for i in remainders:
                qdata.append([i, row[i]])
            #print(self.construct_query(qdata))
            val = df.query(self.construct_query(qdata))['prob'].sum()
            new_f.at[index, 'prob'] = val
        return [remainders, new_f]

    def reduce_factors(self, factors, ordering):
        for obj in ordering:
            adjusters = []
            for i in factors:
                if obj in i[0]:
                    adjusters.append(i)
            for i in factors:
                if obj in i[0]:
                    factors.remove(i)
                    print(len(factors))
            if len(adjusters) > 1:
                #print("HERE")
                adjusters = [self.multiply_factors(adjusters)]

            factors.append(self.eliminate_var(adjusters[0], obj))
            for i in factors:
                print(i[0])
            print('_________END OF ROUND {}___________'.format(obj))
        for i in factors:
            print("____________________")
            print(i[0])
            print(i[1])
            print("____________________")
        #print(factors)


    def run(self, query, observed, elim_order):
        self.observed = observed
        self.reduce_observed()
        ordering = self.classify_nodes()
        ordering.remove(query)
        print(ordering)
        #print(ordering)
        factors = self.create_factors()
        #print(factors[0])
        #print(factors)
        self.reduce_factors(factors, ordering)

        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables

        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run

        Output: A variable holding the probability distribution
                for the query variable

        """
