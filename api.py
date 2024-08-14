import streamlit as st
import anthropic

# Use the API key directly in the code
API_KEY = st.secrets["claud_api_key"]

def get_meal_plan_from_ai(fasting_level, pre_meal_level, post_meal_level, dietary_preference):
    try:
        # Initialize the Anthropic client with the API key
        client = anthropic.Anthropic(api_key=API_KEY)
        
        # Construct the prompt for Claude AI
        prompt = (
            f"A patient with the following details needs a personalized meal plan:\n"
            f"- Fasting sugar level: {fasting_level} mg/dL\n"
            f"- Pre-meal sugar level: {pre_meal_level} mg/dL\n"
            f"- Post-meal sugar level: {post_meal_level} mg/dL\n"
            f"- Dietary preference: {dietary_preference}\n\n"
            "Please provide a personalized meal plan that considers these factors."
        )

        # Send the prompt to Claude AI
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0.5,  # Adjust temperature for response creativity or focus
            system="You are a nutrition expert providing meal plans based on blood sugar levels and dietary preferences.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract text content from the response
        if response and hasattr(response, 'content') and isinstance(response.content, list):
            # Join all text blocks into a single string
            meal_plan = "\n".join(block.text for block in response.content if hasattr(block, 'text'))
            return meal_plan
        else:
            return 'No content found in the response.'
    
    except Exception as e:
        # Handle specific API errors
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("Personalized Meal Plan for Diabetic Patients by Ibn Adam")

    st.write("""
    This app helps diabetic patients receive personalized meal plans based on their blood sugar levels and dietary preferences.
    """)

    # Sidebar inputs
    st.sidebar.header("Input Your Information")

    fasting_level = st.sidebar.number_input("Enter your fasting sugar level (mg/dL):", min_value=0)
    pre_meal_level = st.sidebar.number_input("Enter your pre-meal sugar level (mg/dL):", min_value=0)
    post_meal_level = st.sidebar.number_input("Enter your post-meal sugar level (mg/dL):", min_value=0)

    dietary_preference = st.sidebar.selectbox(
        "Select your dietary preference:",
        ("No preference", "Vegetarian", "Vegan")
    )

    # Button to generate meal plan
    if st.sidebar.button("Generate Meal Plan"):
        # Get the meal plan from Claude AI
        meal_plan = get_meal_plan_from_ai(fasting_level, pre_meal_level, post_meal_level, dietary_preference)
        
        if meal_plan:
            # Display the personalized meal plan
            st.write("### Your Personalized Meal Plan")
            st.write(meal_plan)
        else:
            st.error("Failed to generate meal plan. Please check your API key and credits.")

if __name__ == "__main__":
    main()
