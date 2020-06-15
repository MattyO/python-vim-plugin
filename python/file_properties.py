import itertools
import re

def get_indents(file_name):
    def recursive_sub(indents, accum=''):
        if len(indents) == 0:
            return []
        indent = indents.pop(0)
        next_indent = indent[len(accum):]
        return [next_indent] + recursive_sub(indents, accum + next_indent)

    indent_search = re.compile("^([\s]*)[a-zA-Z]*")
    search_results = []
    with open(file_name, 'r') as f:
        for line in f:
            result = indent_search.search(line)
            if result is not None: 
                search_results.append(indent_search.search(line).group(1))

    results_list = [ key for key, group in itertools.groupby(search_results) ]
    results_list = set(filter(lambda l: l != "\n" and l != '', results_list))
    results_list = sorted(results_list)
    return recursive_sub(results_list)
