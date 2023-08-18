"""
Used this to process a messy data file of weather data. 
The code is messy due to the inconsitency of the weather data file, so I suggest to not use this.
"""

def fix_spacing(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines[1:]:
        cleaned_line = line.replace('\t\t\t', ' 0 ')
        elements = cleaned_line.split()
        unique_elements = []
        for i in range(len(elements) - 1):
            if (elements[i+1] != elements[i] or elements[i] == '0' or elements[i] == '0.0') or float(elements[i]) > 2:
                unique_elements.append(elements[i])
        
        cleaned_line = ' '.join(unique_elements)
        cleaned_lines.append(cleaned_line)

    with open(output_file, 'w') as f:
        f.write('\n'.join(cleaned_lines))

def tabs_to_space(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        elements = line.split()
        cleaned_line = ' '.join(elements)
        cleaned_lines.append(cleaned_line)

    with open(output_file, 'w') as f:
        f.write('\n'.join(cleaned_lines))

if __name__ == '__main__':
    input_file = r'C:\Users\dnh18\OneDrive - NIST\Documents\JadenHe\UMD_NIST_link_09-23-41_24-07-2023.txt'
    output_file = r'C:\Users\dnh18\OneDrive - NIST\Documents\JadenHe\weather_data#2.txt'
    tabs_to_space(input_file, output_file)
