import os

ext_dict = {}
lang_dict= {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".go": "Go",
    ".php": "PHP",
    ".swift": "Swift",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "Sass (SCSS)",
    ".xml": "XML",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
}

def main():
    get_lines()
    print_dict()

def get_lines(code_dir=None, dir=None):
    if code_dir is None:
        code_dir = os.path.dirname(__file__)
    if dir is None:
        dir = os.listdir(code_dir)
    for item in dir:
        
        #sets item path
        item_path = os.path.join(code_dir, item)
        
        #checks if item is a file and in the dict
        if os.path.isfile(item_path):
            #opens the file to read the contents
            try:
                with open(item_path, encoding="utf-8") as file:
                    line_count = len(file.readlines())
            except UnicodeDecodeError:
                try:
                    with open(item_path, encoding="latin-1") as file:  # fallback encoding
                        line_count = len(file.readlines())
                except Exception as e:
                    print(f"Skipping {item_path}: {e}")
                    continue
            except Exception as e:
                print(f"Skipping {item_path}: {e}")
                continue
            #gets the file extension    
            file_ext =  os.path.splitext(item)[1]
            
            #builds the dict and counts the code
            if file_ext in ext_dict and file_ext in lang_dict:
                ext_dict[file_ext] += line_count
            elif file_ext not in ext_dict and file_ext in lang_dict:
                ext_dict[file_ext] = line_count
                
        elif os.path.isdir(item_path):
            get_lines(item_path, os.listdir(item_path))
            
        else:
            raise Exception("Unrecognized content")
    
    return ext_dict
    
def print_dict():
    #removes the length of this script from the total count
    with open(os.path.abspath(__file__)) as counter_file:
        line_count = len(counter_file.readlines())
        ext_dict[".py"] -= line_count
    
    #creates a key for Total    
    total_lines = 0
    most_code = float("-inf")
    primary_ext = ""
    
    for key, value in ext_dict.items():
        total_lines += value
        if value > most_code:
            most_code = value
            primary_ext = key
            
    print()
    print("-" * 45)
    print(f"{'Extension':<12} | {'Lines':>7} | {'Percent of code':>17}")
    print("-" * 45)        
            
    for key, value in ext_dict.items():
        if key != "Total" and value != 0:
            percent = round(100*value / total_lines, 2)
            print(f"{key:<12} | {value:>7} | {percent:>16.2f}%")
            
    print("-" * 45)
    print(f"{'Total lines:':25}{total_lines:>17}")    
    
    if most_code == 0:
        print(f"{'No code found!':>30}")
    else:
        print(f"{'Primary language:':25}{lang_dict[primary_ext]:>17}")
    print("-" * 45)

main()
