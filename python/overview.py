import re

class Overview():

    def __init__(self, filepath):
        self.filepath = filepath
        self.overview_dict = None
        self.number_of_lines = 0

        # TODO find a way to remove this
        self.class_overview()


    def class_and_method_names(self, line_number):
        for obj_name, obj in self.class_overview().items():
            if obj['start'] <= line_number <= obj['end']:
                if obj['type'] == 'function':
                    return (None, obj_name)
                elif obj['type'] == 'class':
                    for method_name, method_obj in obj['functions'].items():
                        if method_obj['start'] <= line_number <= method_obj['end']:
                            return (obj_name, method_name)

        return (None, None)


    def match_methods(self, class_name, method_pattern):
        def matches(pattern, method_name):
            return re.compile(pattern).search(method_name) is not None

        found_method_lines = []

        if class_name in  self.overview_dict.keys():
            class_items = self.overview_dict[class_name]['functions'].items()
            found_method_lines = [method_line['end'] for method_name, method_line in class_items if matches(method_pattern, method_name) ]

        return sorted(found_method_lines, reverse=True)

    def class_overview(self):
        if self.overview_dict is not None:
            return self.overview_dict

        overview_dict = {}
        current_class_name = None
        search_function = re.compile("def (.*)\(.*\):")
        search_class = re.compile("class (.*)\(.*\):")
        indent_search = re.compile("^([\s]*)def")
        current_object = None

        first_indent_text = None

        f = open(self.filepath)
        lines = f.readlines()
        f.close()

        for i, line in enumerate(lines):
            if line.startswith("class"):
                class_name = search_class.search(line).group(1)
                overview_dict[class_name] = {'type': 'class', 'functions':{}, 'start': i + 1}

                if current_class_name != None:
                    overview_dict[current_class_name]['end'] = i

                if current_object is not None:
                    current_object['end'] = i
                    current_object = None

                current_class_name = class_name

            if line.strip().startswith("def"):
                function_name = search_function.search(line).group(1)

                if current_class_name != None and first_indent_text is None:
                    first_indent_text = indent_search.search(line).group(1)

                if line.startswith(f'{first_indent_text}def'): # is method
                    if current_object is not None:
                        current_object['end'] = i

                    current_object = {'start': i + 1 }
                    overview_dict[current_class_name]['functions'][function_name] = current_object

                elif line.startswith(f'def') : #is function
                    if current_object is not None:
                        current_object['end'] = i

                    if current_class_name is not None: 
                        overview_dict[current_class_name]['end'] = i

                    current_object = { 'type': 'function', 'start': i + 1}
                    current_class_name = None
                    overview_dict[function_name] = current_object

        if current_class_name != None:
            overview_dict[current_class_name]['end'] = len(lines)

        if current_object is not None:
            current_object['end'] = len(lines)


        self.number_of_lines = len(lines)
        self.overview_dict = overview_dict

        return overview_dict

