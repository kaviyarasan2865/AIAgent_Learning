from dotenv import load_dotenv
from agents import run_bug_fixer
import os
from pprint import pprint

load_dotenv()

def main():
    # Example input data
    input_data = {
        "html": """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sample Page</title>
        </head>
        <body>
            <div style="width: 300px;">
                Lorem ipsum dolor sit amet
            </div>
            <img src="#" alt="">
            <button onclick="handleClick()">Click me</button>
        </body>
        </html>
        """,
        "css": """
        .header {
            position: absolute;
            width: 500px;
            z-index: 999;
        }
        """,
        "javascript": """
        function handleClick() {
            const element = document.getElementById('missing-id');
            element.style.display = 'none';
        }
        """
    }
    
    # Run the bug fixer
    result = run_bug_fixer(input_data)
    
    # Print the results
    print("\nBug Fixer Results:")
    print("=================")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    
    # Terminal approval flow
    if result.get("status") == "pending" and "dashboard" in result:
        dashboard = result["dashboard"]
        print("\nApproval Dashboard:")
        print("==================")
        if "diff_views" in dashboard:
            for idx, diff in enumerate(dashboard["diff_views"], 1):
                print(f"\nChange #{idx} [{diff['type']}]:")
                print(f"Explanation: {diff.get('explanation', '')}")
                print("--- BEFORE ---")
                print(diff.get("before", ""))
                print("--- AFTER ----")
                print(diff.get("after", ""))
        # Prompt for approval
        user_input = input("\nApprove all changes? (y/n): ").strip().lower()
        if user_input == "y":
            print("\nAll changes approved and applied!")
            # Here you could call a function to actually apply changes if needed
        else:
            print("\nNo changes were applied. Exiting.")
    elif "changes" in result:
        print("\nProposed Changes:")
        print("================")
        for change_type, changes in result["changes"].items():
            print(f"\n{change_type.upper()}:")
            for change in changes:
                print(f"- {change.get('description', '')}")

if __name__ == "__main__":
    main()
