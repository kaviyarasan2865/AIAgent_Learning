from agents import analyze_and_optimize_site

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

# Define test personas
test_personas = [
    "busy professional seeking quick solutions",
    "detail-oriented researcher comparing options",
    "first-time visitor exploring the site"
]

def main():
    print("Starting Website Optimization Analysis...\n")
    
    try:
        results = analyze_and_optimize_site(test_html, test_personas)
        
        print("\n=== User Journey Analysis ===")
        for i, journey in enumerate(results["user_journeys"]):
            print(f"\nPersona {i+1}:")
            print(journey.get("output", "No output available"))
        
        print("\n=== Friction Points ===")
        if results["friction_points"]:
            print(results["friction_points"].get("output", "No friction points detected"))
        
        print("\n=== Benchmark Analysis ===")
        if results["benchmark_analysis"]:
            print(results["benchmark_analysis"].get("output", "No benchmark analysis available"))
        
        print("\n=== UX Recommendations ===")
        if results["ux_recommendations"]:
            print(results["ux_recommendations"].get("output", "No UX recommendations available"))
            
    except Exception as e:
        print(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()