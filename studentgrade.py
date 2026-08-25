import pandas as pd
import matplotlib.pyplot as plt

def create_student_dataset() -> pd.DataFrame:
    """Initializes and returns a structured DataFrame with student mock data."""
    data = {
        "Serial Number": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Name": [
            "Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince", 
            "Ethan Hunt", "Fiona Gallagher", "George Clark", "Hannah Abbott", 
            "Ian Malcolm", "Julia Roberts"
        ],
        "Marks": [95, 82, 74, 58, 91, 65, 45, 88, 79, 62]
    }
    return pd.DataFrame(data)

def assign_grade(marks: float) -> str:
    """
    Assigns a letter grade based strictly on the specified thresholds:
    - 90 to 100: A Grade
    - 80 to <90: B Grade
    - 70 to <80: C Grade
    - 60 to <70: D Grade
    - Below 60: Fail
    """
    if 90 <= marks <= 100:
        return "A Grade"
    elif 80 <= marks < 90:
        return "B Grade"
    elif 70 <= marks < 80:
        return "C Grade"
    elif 60 <= marks < 70:
        return "D Grade"
    else:
        return "Fail"

def display_summary_table(df: pd.DataFrame) -> None:
    """Prints a clean, well-formatted tabular summary of the student grades."""
    print("=" * 60)
    print(f"{'STUDENT PERFORMANCE & GRADES SUMMARY':^60}")
    print("=" * 60)
    # Using to_string for a clean terminal table layout
    print(df.to_string(index=False))
    print("=" * 60 + "\n")

def plot_student_marks(df: pd.DataFrame) -> None:
    """Generates a professional line graph plotting student marks with a failure threshold line."""
    plt.figure(figsize=(11, 6))

    # Combine Serial Number and Name for clear X-axis labels
    x_labels = [f"{row['Serial Number']}. {row['Name']}" for _, row in df.iterrows()]
    
    # Plotting the line graph with markers
    plt.plot(
        x_labels, 
        df['Marks'], 
        marker='o', 
        linestyle='-', 
        color='#1f77b4', 
        linewidth=2, 
        markersize=8, 
        label='Student Marks'
    )

    # Drawing the prominent horizontal threshold line at Marks = 60
    plt.axhline(
        y=60, 
        color='#d62728', 
        linestyle='--', 
        linewidth=2, 
        label='Failure Level (60 Marks)'
    )

    # Chart Styling and Labels
    plt.title("Student Marks Distribution and Failure Threshold", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Students (Serial No. & Name)", fontsize=11, fontweight='semibold')
    plt.ylabel("Marks Scored (0 - 100)", fontsize=11, fontweight='semibold')
    plt.ylim(0, 105)
    plt.xticks(rotation=35, ha='right')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper right', frameon=True)
    
    # Optimize layout to prevent label clipping
    plt.tight_layout()
    plt.show()

def main() -> None:
    """Main execution pipeline."""
    # 1. Initialize Dataset
    df = create_student_dataset()

    # 2. Apply Grading Logic
    df['Grade'] = df['Marks'].apply(assign_grade)

    # 3. Print Tabular Output
    display_summary_table(df)

    # 4. Generate Visualization
    plot_student_marks(df)

if __name__ == "__main__":
    main()