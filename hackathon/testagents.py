from agents import reflection_agent

# Example HTML code to test
test_html = """
<div class="container">
    <h1>Welcome to Our Store</h1>
    <p>Check out our amazing products!</p>
    <button>Buy Now</button>
    <button>Learn More</button>
    <button>Contact Us</button>
</div>
"""

def main():
    print("Starting UX Analysis and Improvement Process...")
    
    # Use the agent to analyze and improve the HTML
    result = reflection_agent.invoke({
        "input": f"""
1. First, analyze this HTML code for UX improvements:
{test_html}

2. After getting the analysis, update the HTML code with the suggested improvements.

3. Return the improved HTML code.
"""
    })
    
    print("\nAgent Process Result:")
    print(result["output"])

if __name__ == "__main__":
    main()