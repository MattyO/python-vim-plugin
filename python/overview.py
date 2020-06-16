import re

class Overview():

    def __init__(self, filepath):
        self.filepath = filepath
        overview_dict = None
        
    def has_method(self, class_name, method_pattern):
        if class_name not in  self.overview_dict.keys():
            return False

        for method_name in self.overview_dict[class_name]['functions'].keys():
            if re.compile(method_pattern).search(method_name) is not None:
                return True


        return False


    def class_overview(self):
        overview_dict = {}
        current_class_name = None
        search_function = re.compile("def (.*)\(.*\):")
        search_class = re.compile("class (.*)\(.*\):")
        indent_search = re.compile("^([\s]*)def")

        first_indent_text = None

        f = open(self.filepath)
        lines = f.readlines()
        f.close()

        for i, line in enumerate(lines):
            if line.startswith("class"):
                class_name = search_class.search(line).group(1)
                overview_dict[class_name] = {'type': 'class', 'functions':{}, 'line': i + 1}

                if current_class_name != None:
                    overview_dict[current_class_name]['end'] = i
                current_class_name = class_name

            if line.strip().startswith("def"):
                function_name = search_function.search(line).group(1)

                if current_class_name != None and first_indent_text is None:
                    first_indent_text = indent_search.search(line).group(1)

                if line.startswith(f'{first_indent_text}def'): # is method
                    overview_dict[current_class_name]['functions'][function_name]= i + 1

                elif line.startswith(f'def') : #is function
                    overview_dict[current_class_name]['end'] = i
                    current_class_name = None
                    overview_dict[function_name] = { 'type': 'function', 'line': i + 1}

        if current_class_name != None:
            overview_dict[current_class_name]['end'] = len(lines)


        self.overview_dict = overview_dict

        return overview_dict

