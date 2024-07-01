import pdfplumber
import docx
import re
import sys
import json

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
            else:
                print("Warning: No text found on one of the pages.")
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
    return text


def find_section(text, category):
    
    pattern = re.compile(rf'\b{category}s?\b[\s\S]*?(\n.+)+', re.IGNORECASE)
    matches = pattern.finditer(text)
    sections = []
    for match in matches:
        section_content = match.group(0).strip()
        # Adding debug output to see what is matched
        print(f"Matched section content:\n{section_content[:300]}")  
        
        
        if len(section_content.split()) > 5:  
            sections.append(section_content)

    return ' '.join(sections) if sections else "Section not found"



def main(resume_path):
    print(f"Processing resume: {resume_path}")
    if resume_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(resume_path)
    elif resume_path.lower().endswith('.docx'):
        text = extract_text_from_docx(resume_path)
    else:
        print("Unsupported file format")
        return

    # Extract sections
    skills_text = find_section(text, "Skill")
    experience_text = find_section(text, "Experience")

    print("Extracted Skills:", skills_text)
    print("Extracted Experience:", experience_text)
    # saving to a JSON file
    parsed_data = {
        "skills": skills_text,
        "experience": experience_text
    }

    # save path
    parsed_resume_path = "parsed_data.json"

    # Save the parsed data to a JSON file
    with open(parsed_resume_path, 'w') as json_file:
        json.dump(parsed_data, json_file, indent=4)

    print(f"Resume parsed and saved to {parsed_resume_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python resume_parser.py <path_to_resume>")
    else:
        main(sys.argv[1])
