from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load job listings from JSON file
def load_jobs():
    with open('static/jobs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)  # Load JSON
        if "jobs" not in data:
            raise KeyError("❌ JSON file must contain a 'jobs' key at the top level.")
        return data["jobs"]  # Return the list inside "jobs"

@app.route('/')
def home():
    jobs = load_jobs()
    print("Loaded jobs data:", jobs)  # Debugging
    print("Type of jobs:", type(jobs))  # Check data type (should be a list)
    
    departments = list(set(job['department'] for job in jobs))  # Extract unique departments
    return render_template('index.html', jobs=jobs, departments=departments)

@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    jobs = load_jobs()
    job = next((job for job in jobs if job['id'] == job_id), None)
    if job:
        return render_template('job_detail.html', job=job)
    return "Job not found", 404

@app.route('/search')
def search_jobs():
    query = request.args.get('query', '').lower()
    department = request.args.get('department', '')

    jobs = load_jobs()

    if query:
        jobs = [job for job in jobs if query in job['title'].lower() 
                or query in job['description'].lower()]

    if department:
        jobs = [job for job in jobs if job['department'] == department]

    departments = list(set(job['department'] for job in load_jobs()))  
    return render_template('index.html', jobs=jobs, departments=departments, 
                           selected_department=department, search_query=query)

if __name__ == '__main__':
    app.run(debug=True)
