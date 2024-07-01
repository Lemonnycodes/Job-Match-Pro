#Count Vectorizer Model
from http.client import HTTPException
from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
import re
import logging
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
from werkzeug.exceptions import HTTPException


app = Flask(__name__)

job_skills = {
    'Software Developer': [
        'Python', 'JavaScript', 'Java', 'C#', 'Go', 'TypeScript', 'Scala', 'Ruby', 'PHP',
        'Black Box Testing', 'Agile Testing', 'DevOps Practices', 'API Design', 'Microservices',
        'Spring Boot', 'Django', 'React', 'Angular', 'Vue.js', 'Cloud Services', 'AWS Lambda',
        'Containerization', 'Kubernetes', 'Docker', 'CI/CD', 'Git', 'SQL', 'NoSQL', 'GraphQL','AJAX','SDLC'
    ],
    'Microsoft CRM Developer': [
        'Javascript', 'C#', 'Microsoft Dynamics 365', 'ASP .NET', 'Canvas', 'Power BI',
        'PowerApps', 'Azure', 'SQL Server', 'Integration Services', 'Automated Testing', 'Custom Workflow Creation'
    ],
    'Database Developer': [
        'SQL Server', 'Microsoft Access', 'Oracle', 'MySQL', 'PostgreSQL', 'NoSQL Databases',
        'Database Design', 'Performance Tuning', 'ETL Processes', 'Data Warehousing', 'MongoDB', 'Cassandra'
    ],
    'Graphic Designer': [
        'Photoshop', 'Adobe Suite', 'Illustrator', 'InDesign', 'Sketch', 'Figma',
        'User Interface Design', 'Animation', 'Print Design', 'Web Design', 'Typography', 'Color Theory'
    ],
    'Systems Analyst': [
        'SQL', 'Networking', 'Linux', 'Cloud Computing', 'ERP Systems', 'System Architecture',
        'Data Analysis', 'Project Management', 'Information Security', 'Troubleshooting', 'SAP', 'Oracle Applications'
    ],
    'Product Manager': [
        'Project Management', 'Marketing', 'Public Speaking', 'SEO/SEM', 'Business Analysis',
        'Product Lifecycle Management', 'Market Research', 'User Experience Design', 'Data-Driven Decision Making', 'Agile Methodologies'
    ],
    'Sales Associate': [
        'Sales Techniques', 'Customer Service', 'E-commerce', 'CRM', 'Negotiation',
        'Salesforce', 'Lead Generation', 'Market Analysis', 'Product Presentation', 'Client Relationship Management'
    ],
    'Marketing Specialist': [
        'Digital Marketing', 'SEO/SEM', 'Content Creation', 'Social Media', 'Google Analytics',
        'Email Marketing', 'AdWords', 'Facebook Ads', 'Marketing Strategy', 'Brand Management', 'Campaign Management'
    ],
    'Data Scientist': [
        'Machine Learning', 'Data Analysis', 'Python', 'R', 'Statistical Analysis',
        'Deep Learning', 'TensorFlow', 'Keras', 'Data Mining', 'Big Data Technologies', 'Hadoop', 'Spark','Matplotlib', 'NumPy', 'Pandas', 'Seaborn', 'Scikit-learn', 'Jupyter Notebook', 'NLTK' ,
        'MS Visio', 'MS Excel', 'MS FrontPage',' MS Word'
   
    ],
    'Network Administrator': [
        'Networking', 'Cybersecurity', 'Linux', 'Cloud Computing', 'Docker',
        'Windows Server', 'Network Security', 'Cisco Systems', 'Firewall Management', 'VPN', 'Remote Support'
    ],
    'UX Designer': [
        'UI/UX Design', 'Sketch', 'Photoshop', 'InVision', 'User Research',
        'Prototype Design', 'User Testing', 'Interaction Design', 'Accessibility Design', 'Responsive Design','REST','SOAP','XML','JSON'
    ],
    'Technical Writer': [
        'Technical Documentation', 'Editing', 'Research', 'Content Management Systems', 'Proofreading',
        'API Documentation', 'User Manuals', 'Online Help Systems', 'Markdown', 'Technical Diagrams'
    ],
    'Cloud Solutions Architect': [
        'Cloud Computing', 'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes',
        'Cloud Security', 'Cloud Migration', 'Hybrid Cloud', 'Serverless Architectures', 'Cloud Storage Solutions'
    ],
    'Cybersecurity Analyst': [
        'Cybersecurity', 'Ethical Hacking', 'Network Security', 'Cryptography', 'Firewalls',
        'Intrusion Detection', 'Malware Analysis', 'Risk Assessment', 'Security Audits', 'Compliance'
    ],
    'Blockchain Developer': [
        'Blockchain', 'Solidity', 'Ethereum', 'Cryptocurrency', 'Smart Contracts',
        'DApp Development', 'Truffle Framework', 'Hyperledger', 'Blockchain Architecture', 'Token Economics'
    ],
    'AI Research Scientist': [
        'Machine Learning', 'Deep Learning', 'TensorFlow', 'Python', 'AI Ethics',
        'Natural Language Processing', 'Computer Vision', 'Reinforcement Learning', 'AI Model Optimization', 'AI Applications'
    ],
    'Mobile App Developer': [
        'Mobile Development', 'Swift', 'Kotlin', 'React Native', 'Firebase',
        'iOS Development', 'Android Development', 'Mobile UI/UX Design', 'Cross-Platform Development', 'App Store Optimization'
    ],
    'DevOps Engineer': [
        'CI/CD', 'Scripting', 'Linux', 'Docker', 'Kubernetes',
        'Automation Tools', 'Jenkins', 'Ansible', 'Cloud Deployment', 'Monitoring and Logging', 'Security Best Practices'
    ],
    'Corporate Lawyer': [
        'Contract Law', 'Corporate Governance', 'M&A', 'Compliance', 'Litigation',
        'Intellectual Property', 'Labor Law', 'Securities Regulation', 'Corporate Finance Law', 'Dispute Resolution'
    ],
    'Environmental Scientist': [
        'Environmental Analysis', 'Sustainability', 'GIS', 'Ecology', 'Pollution Control',
        'Environmental Policy', 'Conservation Strategies', 'Waste Management', 'Water Quality Assessment', 'Environmental Impact Analysis'
    ],
    'Human Resources Manager': [
        'Employee Relations', 'Benefits Administration', 'Recruitment', 'Compliance', 'Training',
        'Performance Management', 'HR Policies', 'Workforce Planning', 'Employee Engagement', 'Diversity and Inclusion'
    ],
    'Public Health Official': [
        'Epidemiology', 'Biostatistics', 'Health Education', 'Public Policy', 'Community Health',
        'Disease Prevention', 'Public Health Surveillance', 'Global Health Issues', 'Health Promotion Programs', 'Emergency Response'
    ],
    'Biomedical Engineer': [
        'Biomechanics', 'Biomaterials', 'Medical Imaging', 'Tissue Engineering', 'Biomedical Devices',
        'Medical Instrumentation', 'Regenerative Medicine', 'Clinical Engineering', 'Biomolecular Engineering', 'Healthcare Technologies'
    ],
    '3D Animator': [
        '3D Modeling', 'Animation', 'Texturing', 'Rigging', 'Motion Capture',
        'Character Animation', 'Visual Effects', '3D Rendering', 'Animation Software', 'Storyboarding'
    ],
    'Real Estate Agent': [
        'Property Management', 'Sales', 'Real Estate Economics', 'Customer Service', 'Negotiation',
        'Real Estate Marketing', 'Property Appraisal', 'Market Analysis', 'Leasing Agreements', 'Property Law'
    ],
    'Fintech Analyst': [
        'Financial Modeling', 'Blockchain', 'Python', 'Machine Learning', 'Regulatory Knowledge',
        'Quantitative Analysis', 'Risk Management', 'Financial Markets', 'Cryptocurrency Analysis', 'Payment Systems'
    ],
    'Web Developer': [
        'HTML', 'CSS', 'JavaScript', 'PHP', 'Ruby on Rails','flask'
        'React.js', 'Angular', 'Node.js', 'Web Performance Optimization', 'Security Practices'
    ],
    'Video Game Designer': [
        'Game Mechanics', 'Storytelling', 'Programming', 'Graphic Design', 'User Interface Design',
        'Game Development Engines', 'Level Design', 'Game Testing', 'Player Psychology', 'Interactive Storytelling'
    ],
    'Logistics Coordinator': [
        'Supply Chain Management', 'Logistics Planning', 'Warehouse Operations', 'Inventory Management', 'Shipping',
        'Freight Management', 'Logistics Software', 'Supply Chain Optimization', 'Distribution Strategies', 'Import/Export Compliance'
    ],
    'Foreign Language Translator': [
        'Language Proficiency', 'Translation', 'Localization', 'Interpreting', 'Cultural Awareness',
        'Simultaneous Translation', 'Technical Translation', 'Document Translation', 'Multilingual Communication', 'Language Services'
    ],
    'SEO Consultant': [
        'SEO', 'Google Analytics', 'Content Marketing', 'Keyword Research', 'Webmaster Tools',
        'Link Building', 'SEO Strategy', 'Content Optimization', 'Search Engine Algorithms', 'Local SEO'
    ],
    'Data Security Analyst': [
        'Information Security', 'Network Security', 'Vulnerability Assessment', 'Encryption', 'Firewalls',
        'Penetration Testing', 'Security Operations', 'Incident Response', 'Data Privacy', 'Compliance Standards',
        'MS Visio', 'MS Excel', 'MS FrontPage',' MS Word'
    ],
    'Software Tester': [
        'Test Automation', 'Manual Testing', 'Performance Testing', 'Security Testing', 'Quality Assurance',
        'Selenium', 'Test Planning', 'Bug Tracking', 'Regression Testing', 'Test Scripts', 'Black Box Testing (Advanced)', 'Agile Testing (Experienced)', 'Retesting & Regression Testing'
    ],
    'Data Engineer': [
        'Data Integration', 'Data Warehousing', 'Big Data Technologies', 'Data Modeling', 'ETL Development',
        'SQL', 'Python', 'Apache Spark', 'Data Pipeline Construction', 'Real-time Data Processing',
        'MS Visio', 'MS Excel', 'MS FrontPage',' MS Word'
    ],
    'Data Analyst': [
        'Python', 'R', 'SQL', 'Tableau', 'Power BI', 'Excel', 
        'Pandas', 'NumPy', 'Statistical Analysis', 'Data Visualization', 'Machine Learning',
        'MS Visio', 'MS Excel', 'MS FrontPage',' MS Word'
    ],
    'Programmer Analyst': [
        'Java', 'C++', 'SQL', 'Python', 'System Analysis', 'Debugging','DBMS',
        'Code Optimization', 'Database Management', 'Software Development Lifecycle', 'Agile Methodologies'
    ],
    'Salesforce Developer': [
        'Apex', 'Visualforce', 'Salesforce Object Query Language (SOQL)', 'Lightning Components',
        'Salesforce APIs', 'CRM', 'Integration Patterns', 'Workflow Automation', 'Custom UI Development', 'Platform Development'
    ],
    'SAP Consultant': [
        'SAP ERP', 'SAP Business Suite', 'ABAP', 'NetWeaver', 'SAP HANA', 'SAP Fiori',
        'Business Process Knowledge', 'Data Migration', 'SAP Modules Specific Knowledge (like FI, MM, SD)', 'Project Management'
    ],
    
    'Cloud Engineer': [
        'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 
        'Cloud Security', 'DevOps', 'CI/CD Pipelines', 'Server Management', 'Scripting'
    ],
    'Project Manager': [
        'Project Planning', 'Risk Management', 'Agile Scrum Master', 'Stakeholder Management', 
        'Budgeting', 'MS Project', 'Team Leadership', 'Performance Tracking', 'Resource Allocation', 'Communication Skills'
    ],
    'Quality Assurance Engineer': [
        'Test Automation', 'Selenium WebDriver', 'Quality Control Procedures', 'Bug Tracking Tools', 
        'JIRA', 'Regression Testing', 'Performance Testing', 'Test Plan Development', 'CI/CD', 'Security Testing'
    ],
    'Machine Learning Engineer': [
        'Python', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Data Modeling', 
        'Neural Networks', 'Deep Learning', 'NLP', 'Computer Vision', 'AI Algorithm Development'
    ],
    'DevOps Specialist': [
        'Jenkins', 'Ansible', 'Docker', 'Kubernetes', 'Terraform', 
        'Scripting (Bash/Python)', 'Linux', 'CI/CD Pipelines', 'Cloud Services', 'Monitoring Tools (Prometheus/Grafana)'
    ],
    'User Experience Designer': [
        'Sketch', 'InVision', 'User Research', 'Personas', 'Wireframing', 
        'Prototyping', 'Usability Testing', 'Interaction Design', 'Information Architecture', 'Visual Design'
    ],
    'Network Engineer': [
        'Routing and Switching', 'Firewalls', 'Cisco Systems', 'Juniper', 'Network Security',
        'WAN/LAN', 'VoIP', 'MPLS', 'Network Management Tools', 'Troubleshooting'
    ],
    'Business Analyst': [
        'Requirement Gathering', 'Data Analysis', 'Business Process Modeling', 'Stakeholder Analysis',
        'UML', 'SQL', 'Power BI', 'Tableau', 'SDLC', 'Agile Methodologies','Microsoft Office Suite (Word, PowerPoint, Excel)', 'Access', 'SQL', 'Tableau', 'Python', 'MS Power BI', 'KNIME','Hadoop',
'PySpark', 'Agile', 'Google Analytics', 'R programming language', 'Microsoft AZURE', 'generative AI', 'data analytics'
    ]
}

try:
    job_data = pd.read_json('jsoninput_jobdata.json')
    print("Job data successfully loaded:", job_data.head())
except Exception as e:
    print("Failed to load job data:", str(e))

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        resume = request.files['resume']
        location = request.form['location']
        experience = int(request.form['experience'])
        mode_of_work = request.form.get('modeOfWork', 'No Preference').lower()

        if not resume:
            return jsonify({'error': 'No resume file provided'}), 400

        resume_text = extract_text(resume.stream)
        skills = extract_skills(resume_text)

        vectorizer = CountVectorizer()

        default_skills = ['General Skills']
        skill_texts = [' '.join(job_skills.get(title, default_skills)) for title in job_data['Job Title']]
        job_matrix = vectorizer.fit_transform(skill_texts)
        
        user_skills_vec = vectorizer.transform([skills])
        similarity_scores = cosine_similarity(user_skills_vec, job_matrix)

        if len(similarity_scores[0]) != len(job_data):
            return jsonify({'error': 'Mismatch in data lengths'}), 500
        
        job_data['similarity_score'] = similarity_scores[0]
        job_data['adjusted_score'] = job_data.apply(
            lambda row: seniorityrole(row['Job Title'], experience, row['similarity_score']), axis=1
        )

        recommended_jobs = job_data[
            (job_data['Location'].str.contains(location, case=False) if location.lower() != 'anywhere' else True) &
            (job_data['Years of Experience'] <= experience) & 
            (job_data['Mode of Work'].str.lower() == mode_of_work if mode_of_work != 'no preference' else True) &
            (job_data['similarity_score'] > 0.1)
        ].sort_values(by='similarity_score', ascending=False)

        return jsonify(recommended_jobs.to_dict(orient='records'))
    except Exception as e:
        logging.exception("An error occurred: %s", e)
        return jsonify({'error': str(e)}), 500


def extract_skills(resume_text):
    print("Resume Content",resume_text)
    uniqueskills = list(set(skill.lower() for sublist in job_skills.values() for skill in sublist))
    vectorizer = CountVectorizer(vocabulary=uniqueskills, lowercase=True)  # Ensure lowercase matching
    vectorizer.fit(uniqueskills)
    skill_counts = vectorizer.transform([resume_text.lower()])
    print("skills count",skill_counts)
    skills_found = [skill for skill, count in zip(vectorizer.get_feature_names_out(), skill_counts.toarray()[0]) if count > 0]
    print("Skills found after matching:", skills_found)  
    return ' '.join(skills_found)


def seniorityrole(title, experience, base_score):
    senkeywords = ['Senior', 'Sr.', 'Manager', 'Executive', 'Lead']
    if any(keyword in title for keyword in senkeywords) and experience > 5:
        return base_score * 1.2
    return base_score

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method Not Allowed', 'message': str(error)}), 405

if __name__ == '__main__':
    app.run(debug=True)

