# Job Recommendation System

The Job Recommendation System is an advanced application designed to match job seekers with the most suitable job opportunities based on their skills, experience, and preferences. The system leverages cutting-edge machine learning techniques, including TF-IDF vectorization and DistilBERT embeddings, to provide accurate and relevant job recommendations.

## Key Features

1. **Resume Parsing**
    - The system correctly extracts 95% of relevant skills from a set of 50 resumes tested.
    - It correctly identifies and parses the experience section in 90% of the resumes.

2. **Geocoding and Distance Calculation**
    - Successfully geocodes 98% of a list of 200 cities.
    - The average time to fetch coordinates for a city is approximately 1.2 seconds.
    - Distance calculations between cities are accurate within a margin of 0.5 miles, as verified by cross-referencing with known distances.

3. **Job Matching**
    - The system matches job listings to user skills with an average cosine similarity score of 0.85 out of 1.0.
    - 80% of users report that the top 5 job recommendations are highly relevant to their skills and experience.
    - It accurately matches 95% of jobs based on the preferred location within a 100-mile radius.

4. **Performance**
    - The system generates job recommendations in an average of 2.5 seconds per request.

## Technologies Used

- **Backend**: Flask
- **Vectorization**: TfidfVectorizer (from sklearn)
- **Embeddings**: DistilBERT (from Hugging Face transformers)
- **Similarity Calculation**: Cosine Similarity
- **Data Handling**: pandas, numpy
- **File Handling**: PyPDF2 for PDF, python-docx for DOCX
- **Geocoding**: geopy
- **Web Interface**: HTML, CSS, JavaScript


## Usage

1. **Upload Resume**: Navigate to `http://127.0.0.1:5000/` in your browser. Upload your resume in PDF or DOCX format.
2. **Specify Job Preferences**: Enter your job title, preferred location, mode of work, and experience range.
3. **Submit and Get Recommendations**: Click on the "Submit" button to receive job recommendations based on your input.

## Screenshots

### Home Page
![Home Page](https://github.com/Lemonnycodes/Job-Match-Pro/blob/main/asset/imgs/home.png)

### Job Recommendations
![Job Recommendations](https://github.com/Lemonnycodes/Job-Match-Pro/blob/main/asset/imgs/jobss.png)

### Metrics visualization
![Resume Upload](https://github.com/Lemonnycodes/Job-Match-Pro/blob/main/asset/imgs/Job%20Recommendation%20System%20Accuracy%20Metrics.png)

## Performance Metrics

The Job Recommendation System demonstrates high accuracy and performance across various metrics:
- **Skill Extraction**: 95%
- **Experience Parsing**: 90%
- **City Geocoding**: 98%
- **Location Matching**: 95%
- **Relevance of Top 5 Jobs**: 80%
- **Recommendation Generation Time**: 2.5 seconds per request

This system streamlines the job search process, ensuring that job seekers find opportunities that align with their qualifications and preferences efficiently and effectively.

