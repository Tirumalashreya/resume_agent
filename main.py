# main.py
import os
import traceback
from dotenv import load_dotenv 
load_dotenv()

# Import functions and classes from the utils module
from utils.llm_config import setup_llm, llm, test_llm_simple
from utils.input_handlers import ResumeInputHandler
from utils.resume_processor import simple_resume_optimization, SimpleFallback
from utils.file_manager import save_output_to_file

def main():
    """Main function to run the resume optimization system."""
    print("🚀 RESUME OPTIMIZATION SYSTEM 🚀")
    print("=" * 50)

    # Step 1: Setup LLM
    # The setup_llm function initializes the global 'llm' variable
    # defined in llm_config.py
    setup_llm()

    # Step 2: Get user inputs for resume and job description
    try:
        print("\nStep 1: Provide your resume")
        resume_text = ResumeInputHandler.get_resume_input()

        print("\nStep 2: Provide the job description")
        job_description = ResumeInputHandler.get_job_description_input()

        print("\n🔄 Processing your resume...")

    except Exception as e:
        print(f"❌ Error getting inputs: {e}")
        traceback.print_exc()
        return

    result = "" # Initialize result variable

    # Step 3: Perform resume optimization
    # Check if LLM is functional and proceed with AI-powered optimization or fallback
    if llm and test_llm_simple():
        print("\n🚀 LLM is available, proceeding with AI-powered optimization...")
        
        try:
            # Extract skills using the simple fallback method, as the original code
            # used it even before the direct LLM call. This provides structured skills
            # for the LLM prompt.
            skills = SimpleFallback.extract_skills_simple(resume_text)
            skills_text = (
                f"Technical: {', '.join(skills['technical'])}\n"
                f"Soft: {', '.join(skills['soft'])}\n"
                f"Domain: {', '.join(skills['domain'])}"
            )
            
            # Construct the prompt for the LLM to generate the optimized resume
            prompt = (
                f"You are an expert resume writer. Create a highly ATS-friendly resume. "
                f"Utilize the following information to tailor the resume specifically for the job description:\n\n"
                f"--- ORIGINAL RESUME CONTENT ---\n{resume_text}\n\n"
                f"--- EXTRACTED SKILLS ---\n{skills_text}\n\n"
                f"--- JOB DESCRIPTION ---\n{job_description}\n\n"
                f"Focus on:\n"
                f"- Incorporating keywords from the job description naturally\n"
                f"- Quantifying achievements wherever possible\n"
                f"- Using clear, standard section headers\n"
                f"- Ensuring ATS-friendly formatting\n"
                f"Provide only the complete, well-formatted resume text."
            )
            
            # Invoke the LLM to get the optimized resume content
            response = llm.invoke(prompt)
            # Extract the content from the LLM's response object
            result = response.content if hasattr(response, 'content') else str(response)
            
            print("\n" + "=" * 50)
            print("✅ AI-POWERED OPTIMIZATION COMPLETED!")
            print("=" * 50)
            print(result)
            
        except Exception as e:
            print(f"❌ AI-powered optimization failed: {e}")
            print("🔄 Falling back to enhanced processing (non-LLM mode)...")
            # If LLM optimization fails, fall back to the simple rule-based optimization
            result = simple_resume_optimization(resume_text, job_description)
            
            print("\n" + "=" * 50)
            print("✅ RESUME OPTIMIZATION COMPLETED (Enhanced Mode)")
            print("=" * 50)  
            print(result)
    else:
        # If no LLM is available or LLM test fails, use the enhanced fallback mode
        print("🔄 LLM not available or test failed. Using enhanced processing mode...")
        result = simple_resume_optimization(resume_text, job_description)

        print("\n" + "=" * 50)
        print("✅ RESUME OPTIMIZATION COMPLETED (Enhanced Mode)")
        print("=" * 50)
        print(result)

    # Step 4: Offer to save the results to a file
    try:
        save_choice = input("\nDo you want to save the results to a file? (y/n): ").strip().lower()
        if save_choice in ['y', 'yes']:
            filename = save_output_to_file(str(result))
            if filename:
                print(f"✅ Results saved to: {filename}")
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    main() # Call the main function when the script is executed
