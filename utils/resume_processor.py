# utils/resume_processor.py
from typing import Dict, List
import re

class SimpleFallback:
    """
    Provides simple, rule-based (keyword-based) functions for resume processing.
    These functions act as a fallback or a pre-processing step for LLM-based solutions.
    """

    @staticmethod
    def extract_skills_simple(resume_text: str) -> Dict[str, List[str]]:
        """
        Extracts skills from the resume text based on predefined keyword lists.
        Categorizes skills into 'technical', 'soft', and 'domain'.
        """
        # Define lists of common keywords for different skill categories
        technical_keywords = [
            'python', 'javascript', 'java', 'c++', 'react', 'node.js', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'html', 'css', 'typescript', 'express',
            'postgresql', 'mongodb', 'redis', 'linux', 'bash', 'jenkins', 'github',
            'vue', 'angular', 'flask', 'django', 'spring', 'mysql', 'oracle',
            'azure', 'gcp', 'terraform', 'ansible', 'jest', 'cypress', 'junit',
            'rest', 'api', 'graphql', 'microservices', 'devops', 'ci/cd', 'machine learning',
            'data analysis', 'deep learning', 'nlp', 'pytorch', 'tensorflow', 'scikit-learn',
            'pandas', 'numpy', 'spark', 'hadoop', 'tableau', 'power bi', 'excel', 'gcp'
        ]

        soft_keywords = [
            'leadership', 'communication', 'teamwork', 'problem-solving', 'analytical',
            'creative', 'adaptable', 'collaborative', 'detail-oriented', 'organized',
            'mentoring', 'training', 'presentation', 'negotiation', 'time management',
            'motivated', 'passionate', 'learning', 'critical thinking', 'interpersonal',
            'conflict resolution', 'emotional intelligence', 'proactive'
        ]

        domain_keywords = [
            'agile', 'scrum', 'kanban', 'ci/cd', 'devops', 'testing', 'debugging',
            'optimization', 'architecture', 'design patterns', 'api', 'microservices',
            'cloud computing', 'security', 'automation', 'monitoring', 'logging',
            'performance tuning', 'full-stack', 'web development', 'responsive', 'ui', 'ux',
            'project management', 'product management', 'business analysis', 'data modeling',
            'system design', 'requirements gathering'
        ]

        resume_lower = resume_text.lower() # Convert resume text to lowercase for case-insensitive matching

        # Find skills by checking if keywords exist in the resume text
        found_technical = sorted(list(set([skill for skill in technical_keywords if skill.lower() in resume_lower])))
        found_soft = sorted(list(set([skill for skill in soft_keywords if skill.lower() in resume_lower])))
        found_domain = sorted(list(set([skill for skill in domain_keywords if skill.lower() in resume_lower])))

        return {
            "technical": found_technical,
            "soft": found_soft,
            "domain": found_domain
        }

    @staticmethod
    def create_optimized_resume(resume_text: str, job_description: str = "") -> str:
        """
        Creates a basic ATS-friendly resume format by extracting and structuring
        information from the raw resume text. This is a rule-based approach.
        It also attempts to incorporate job-specific keywords.
        """
        lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
        name_line = lines[0] if lines else "Your Name" # Assume first non-empty line is the name

        # Extract contact information using regular expressions
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

        email_match = re.search(email_pattern, resume_text)
        phone_match = re.search(phone_pattern, resume_text)

        contact_info = []
        if email_match:
            contact_info.append(f"Email: {email_match.group()}")
        if phone_match:
            contact_info.append(f"Phone: {phone_match.group()}")

        # Extract skills using the simple keyword extraction method
        skills = SimpleFallback.extract_skills_simple(resume_text)

        # Attempt to extract common resume sections based on keywords
        experience_section = ""
        education_section = ""
        
        text_lower = resume_text.lower()
        
        # Heuristic to find and extract the "Experience" section
        if "experience:" in text_lower or "professional experience" in text_lower:
            exp_start_idx = -1
            if "experience:" in text_lower:
                exp_start_idx = text_lower.find("experience:")
            elif "professional experience" in text_lower:
                exp_start_idx = text_lower.find("professional experience")

            if exp_start_idx != -1:
                # Find the end of the experience section by looking for subsequent major sections
                exp_end_idx = len(resume_text)
                for section_header in ["education:", "skills:", "projects:", "awards:"]:
                    found_idx = text_lower.find(section_header, exp_start_idx + len("experience:"))
                    if found_idx != -1 and found_idx < exp_end_idx:
                        exp_end_idx = found_idx
                experience_section = resume_text[exp_start_idx:exp_end_idx].strip()
                # Remove the header itself from the extracted section
                experience_section = re.sub(r'(?i)experience:|professional experience', '', experience_section, count=1).strip()


        # Heuristic to find and extract the "Education" section
        if "education:" in text_lower:
            edu_start_idx = text_lower.find("education:")
            edu_end_idx = len(resume_text)
            for section_header in ["skills:", "projects:", "awards:"]:
                found_idx = text_lower.find(section_header, edu_start_idx + len("education:"))
                if found_idx != -1 and found_idx < edu_end_idx:
                    edu_end_idx = found_idx
            education_section = resume_text[edu_start_idx:edu_end_idx].strip()
            education_section = re.sub(r'(?i)education:', '', education_section, count=1).strip()


        # Identify job keywords that appear in the resume and the job description
        job_keywords = []
        if job_description:
            job_lower = job_description.lower()
            all_skills_combined = skills['technical'] + skills['domain'] # Combine relevant skill types
            job_keywords = [keyword for keyword in all_skills_combined if keyword.lower() in job_lower]

        # Generate the structured, ATS-friendly resume
        optimized_resume = f"""
{name_line}
{', '.join(contact_info)}

PROFESSIONAL SUMMARY
Experienced professional with a strong background in software development and project delivery.
Adept at leveraging modern technologies to build scalable and efficient solutions.
{f"Key skills aligned with target role: {', '.join(job_keywords[:5])}" if job_keywords else "Committed to continuous learning and achieving impactful results."}

TECHNICAL SKILLS
• Programming Languages: {', '.join([s.title() for s in skills['technical'][:6]]) if skills['technical'] else 'Not specified'}
• Frameworks & Tools: {', '.join([s.title() for s in skills['technical'][6:12]]) if len(skills['technical']) > 6 else 'Not specified'}
• Databases & Cloud: {', '.join([s.upper() if s.upper() in ['SQL', 'AWS', 'GCP'] else s.title() for s in skills['technical'][12:18]]) if len(skills['technical']) > 12 else 'Not specified'}
• Development Practices: {', '.join([s.title() for s in skills['domain'][:6]]) if skills['domain'] else 'Not specified'}

PROFESSIONAL EXPERIENCE
{experience_section if experience_section else '''
Software Developer | Tech Solutions Inc. | 20XX - Present
• Developed and maintained full-stack web applications, improving user engagement by X%.
• Implemented robust backend APIs, supporting high-traffic user interactions.
• Collaborated with cross-functional teams to define, design, and ship new features.
• Participated in code reviews, ensuring high code quality and adherence to best practices.
'''}

EDUCATION
{education_section if education_section else 'B.S. in Computer Science | University Name | 20XX'}

CORE COMPETENCIES
• {', '.join([s.title() for s in (skills['soft'] + skills['domain'])[:8]]) if (skills['soft'] + skills['domain']) else 'Problem Solving • Adaptability • Teamwork • Innovation'}

=== ATS OPTIMIZATION FEATURES ===
✓ Standard section headers for ATS parsing
✓ Keyword optimization based on job requirements
✓ Quantified achievements and metrics (where provided or templated)
✓ Clean, professional formatting
✓ Relevant technical skills prominently displayed
✓ Action-oriented bullet points
        """
        return optimized_resume.strip()

def simple_resume_optimization(resume_text: str, job_description: str) -> str:
    """
    Performs an enhanced simple resume optimization using the SimpleFallback class.
    This function generates a skill analysis, an ATS-optimized resume,
    and a job matching analysis without relying on an LLM.
    """
    print("🔄 Running enhanced optimization (fallback mode)...")

    # Extract skills using the SimpleFallback method
    skills = SimpleFallback.extract_skills_simple(resume_text)
    # Create the optimized resume structure using SimpleFallback
    optimized = SimpleFallback.create_optimized_resume(resume_text, job_description)

    # Calculate job matching: find skills from the resume that are present in the job description
    all_skills_for_matching = skills['technical'] + skills['domain'] # Focus on technical and domain skills for matching
    job_matches = [skill for skill in all_skills_for_matching if skill.lower() in job_description.lower()]

    # Format the comprehensive result
    result = f"""
--- SKILL ANALYSIS ---
Technical Skills: {', '.join(skills['technical']) if skills['technical'] else 'None found'}
Soft Skills: {', '.join(skills['soft']) if skills['soft'] else 'None found'}
Domain Skills: {', '.join(skills['domain']) if skills['domain'] else 'None found'}

--- ATS-OPTIMIZED RESUME ---
{optimized}

--- JOB MATCHING ANALYSIS ---
Job Keywords Found in Resume: {len(job_matches)} matches detected
Matched Skills: {', '.join(job_matches) if job_matches else 'No direct skill matches found based on current keywords.'}

--- OPTIMIZATION RECOMMENDATIONS ---
✓ Structured with ATS-friendly formatting
✓ Incorporated relevant keywords from job description
✓ Quantified achievements where possible (ensure your original resume has these)
✓ Used action verbs and professional language
✓ Optimized for keyword scanning systems
✓ Clear section headers for ATS parsing
    """
    return result

