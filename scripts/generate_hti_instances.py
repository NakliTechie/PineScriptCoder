#!/usr/bin/env python3
"""
Script to generate HTI screener instances 1-10
"""

import os
import re

def generate_hti_instances():
    """Generate HTI screener instances 1-10"""
    base_dir = "/Users/chiragpatnaik/Pinescript/screeners/hti_screener/final"
    
    # Read the base template (instance 1)
    with open(f"{base_dir}/hti_1.pine", "r") as f:
        template = f.read()
    
    # Generate instances 2-10
    for i in range(2, 11):
        # Replace indicator name
        instance_content = re.sub(
            r"indicator\('HTI - 1'", 
            f"indicator('HTI - {i}'", 
            template
        )
        
        # Replace screen number
        instance_content = re.sub(
            r"scr_numb = input\.int\(1,", 
            f"scr_numb = input.int({i},", 
            instance_content
        )
        
        # Write the instance file
        filename = f"hti_{i}.pine"
        with open(f"{base_dir}/{filename}", "w") as f:
            f.write(instance_content)
        
        print(f"Generated {filename}")

if __name__ == "__main__":
    generate_hti_instances()
    print("All HTI screener instances generated successfully!")