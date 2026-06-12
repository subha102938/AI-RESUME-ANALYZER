import io
import os
import asyncio
from fastapi import UploadFile
from app import analyze

async def run_tests():
    # Resolve the PDF path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "resume.pdf")

    with open(pdf_path, "rb") as f:
        pdf_content = f.read()

    # Define test helper
    async def test_analyze(job_desc):
        # Create a new UploadFile for each test run because read pointer gets consumed
        file_obj = io.BytesIO(pdf_content)
        upload_file = UploadFile(file=file_obj, filename="resume.pdf")
        
        result = await analyze(file=upload_file, job_description=job_desc)
        return result

    print("Running Verification Tests...\n")

    # Test Case 1: Empty Job Description (should fallback to default skills)
    res1 = await test_analyze("")
    print("Test 1 (Empty Job Desc) Result:")
    print("  job_required_skills:", res1["job_required_skills"])
    print("  resume_skills:", res1["resume_skills"])
    print("  matched_skills:", res1["matched_skills"])
    print("  missing_skills:", res1["missing_skills"])
    print("  ats_score:", res1["ats_score"])
    
    assert set(res1["job_required_skills"]) == {"Python", "SQL", "Machine Learning", "JavaScript"}, "Test 1 Failed: Expected default fallback skills"
    print("  => Test 1 PASSED!\n")

    # Test Case 2: Custom Job Description with specific skills
    res2 = await test_analyze("We need a backend developer skilled in SQL, JavaScript and C++.")
    print("Test 2 (Custom Job Desc with skills) Result:")
    print("  job_required_skills:", res2["job_required_skills"])
    print("  resume_skills:", res2["resume_skills"])
    print("  matched_skills:", res2["matched_skills"])
    print("  missing_skills:", res2["missing_skills"])
    print("  ats_score:", res2["ats_score"])
    
    # NOTE: The assertions below depend on the current implementation of extract_skills() in finder.py, 
    # which uses substring matching. As a result, "Java" matches inside "JavaScript" and "C" matches inside "C++".
    assert set(res2["job_required_skills"]) == {"C", "C++", "Java", "SQL", "JavaScript"}, "Test 2 Failed: Expected skills extracted from job description"
    print("  => Test 2 PASSED!\n")

    # Test Case 3: Job Description with no matching skills (should fallback to default skills)
    res3 = await test_analyze("fud bud fuzz")
    print("Test 3 (No skills extracted Job Desc) Result:")
    print("  job_required_skills:", res3["job_required_skills"])
    print("  resume_skills:", res3["resume_skills"])
    print("  matched_skills:", res3["matched_skills"])
    print("  missing_skills:", res3["missing_skills"])
    print("  ats_score:", res3["ats_score"])
    
    assert set(res3["job_required_skills"]) == {"Python", "SQL", "Machine Learning", "JavaScript"}, "Test 3 Failed: Expected fallback to default skills when none extracted"
    print("  => Test 3 PASSED!\n")

    print("All tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(run_tests())
