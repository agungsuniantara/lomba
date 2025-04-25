import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import os
import numpy as np
import math

class NutritionApp:
    def __init__(self, window):
        # ------ BASIC APPLICATION SETTINGS ------
        self.window = window
        self.window.title("Nutrition App")
        self.window.geometry("1000x750")
        
        # Set application color theme
        self.style = ttk.Style()
        
        # Prepare calorie intake data
        self.calorie_data = {}
        
        # Read calorie data from file if exists
        self.filename = "calorie_data.json"
        self.read_calorie_data()
        
        # ------ APPLICATION HEADER SECTION ------
        self.title_frame = ttk.Frame(self.window, padding=10)
        self.title_frame.pack(fill=X, pady=(10, 5))
        
        self.app_title = ttk.Label(
            self.title_frame, 
            text="NUTRITION TRACKER",
            font=('Helvetica', 22, 'bold'),
            bootstyle=PRIMARY
        )
        self.app_title.pack()
        
        self.subtitle = ttk.Label(
            self.title_frame,
            text="Track your daily nutritional needs",
            font=('Helvetica', 12),
            bootstyle=SECONDARY
        )
        self.subtitle.pack(pady=5)
        
        # ------ CREATE NAVIGATION TABS ------
        self.main_tab = ttk.Notebook(self.window, bootstyle=INFO)
        self.main_tab.pack(expand=True, fill=BOTH, padx=15, pady=10)
        
        # Tab 1: Macronutrient Tracker
        self.macro_tab = ttk.Frame(self.main_tab, padding=10)
        self.main_tab.add(self.macro_tab, text="Macronutrient Tracker")
        
        # Tab 2: Daily Calorie Intake
        self.calorie_tab = ttk.Frame(self.main_tab, padding=10)
        self.main_tab.add(self.calorie_tab, text="Daily Calorie Intake")
        
        # Prepare content for both tabs
        self.create_macronutrient_tab()
        self.create_calorie_tab()
        
        # ------ FOOTER SECTION ------
        self.footer_frame = ttk.Frame(self.window, padding=5)
        self.footer_frame.pack(side=BOTTOM, fill=X)
        
        self.footer_text = ttk.Label(
            self.footer_frame,
            text=f"© {datetime.now().year} Nutrition App - v2.1",
            font=('Helvetica', 8),
            bootstyle=SECONDARY
        )
        self.footer_text.pack(side=BOTTOM, fill=X, pady=5)

    # ------ FUNCTIONS FOR MACRONUTRIENT TAB ------
    def create_macronutrient_tab(self):
        # Main container for macronutrient tab
        self.macro_frame = ttk.Frame(self.macro_tab, padding=10)
        self.macro_frame.pack(expand=True, fill=BOTH)
        
        # Configure column and row sizes
        self.macro_frame.columnconfigure(0, weight=1)
        self.macro_frame.columnconfigure(1, weight=1)
        self.macro_frame.rowconfigure(1, weight=1)
        
        # ------ MACRONUTRIENT INPUT SECTION ------
        self.macro_input_frame = ttk.Labelframe(
            self.macro_frame, 
            text="Macronutrient Input",
            padding=15,
            bootstyle=INFO
        )
        self.macro_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # Carbohydrate input
        ttk.Label(
            self.macro_input_frame, 
            text="Carbohydrates (g):",
            bootstyle=INFO
        ).grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        self.carb_input = ttk.Entry(self.macro_input_frame, width=15)
        self.carb_input.grid(row=0, column=1, padx=5, pady=10, sticky='w')
        
        # Protein input
        ttk.Label(
            self.macro_input_frame, 
            text="Protein (g):",
            bootstyle=INFO
        ).grid(row=1, column=0, padx=5, pady=10, sticky='w')
        
        self.protein_input = ttk.Entry(self.macro_input_frame, width=15)
        self.protein_input.grid(row=1, column=1, padx=5, pady=10, sticky='w')
        
        # Fat input
        ttk.Label(
            self.macro_input_frame, 
            text="Fat (g):",
            bootstyle=INFO
        ).grid(row=2, column=0, padx=5, pady=10, sticky='w')
        
        self.fat_input = ttk.Entry(self.macro_input_frame, width=15)
        self.fat_input.grid(row=2, column=1, padx=5, pady=10, sticky='w')
        
        # Calculate button
        self.calculate_macro_btn = ttk.Button(
            self.macro_input_frame, 
            text="Calculate Macronutrients", 
            command=self.calculate_macros,
            bootstyle=SUCCESS
        )
        self.calculate_macro_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=15, sticky='ew')
        
        # ------ MACRONUTRIENT DIAGRAM SECTION ------
        self.macro_diagram_frame = ttk.Labelframe(
            self.macro_frame, 
            text="Macronutrient Visualization",
            padding=15,
            bootstyle=PRIMARY
        )
        self.macro_diagram_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        # Prepare pie chart
        self.macro_figure = Figure(figsize=(5, 4), dpi=100)
        self.macro_plot = self.macro_figure.add_subplot(111)
        self.macro_canvas = FigureCanvasTkAgg(self.macro_figure, self.macro_diagram_frame)
        self.macro_canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Initial empty pie chart
        self.macro_plot.pie([1], labels=['Enter data'], colors=['#f5f5f5'])
        self.macro_plot.set_title('Macronutrient Distribution')
        self.macro_canvas.draw()
        
        # ------ MACRONUTRIENT ANALYSIS RESULTS SECTION ------
        self.macro_results_frame = ttk.Labelframe(
            self.macro_frame, 
            text="Macronutrient Analysis Results",
            padding=15,
            bootstyle=SUCCESS
        )
        self.macro_results_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        # Analysis results label
        self.macro_results_label = ttk.Label(
            self.macro_results_frame, 
            text="Enter macronutrient data to see analysis", 
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        self.macro_results_label.pack(fill=X, pady=5)
        
        self.macro_details_label = ttk.Label(
            self.macro_results_frame, 
            text="", 
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        self.macro_details_label.pack(fill=X, pady=5)

    # ------ FUNCTIONS FOR CALORIE TAB ------
    def create_calorie_tab(self):
        # Main container for calorie tab
        self.calorie_frame = ttk.Frame(self.calorie_tab, padding=10)
        self.calorie_frame.pack(expand=True, fill=BOTH)
        
        # Configure column and row sizes
        self.calorie_frame.columnconfigure(0, weight=1)
        self.calorie_frame.columnconfigure(1, weight=1)
        self.calorie_frame.rowconfigure(1, weight=1)
        
        # ------ CALORIE INPUT SECTION ------
        self.calorie_input_frame = ttk.Labelframe(
            self.calorie_frame, 
            text="Calorie Intake Input",
            padding=15,
            bootstyle=INFO
        )
        self.calorie_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        # Age input
        ttk.Label(
            self.calorie_input_frame, 
            text="Age:",
            bootstyle=INFO
        ).grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        self.age_input = ttk.Entry(self.calorie_input_frame, width=15)
        self.age_input.grid(row=0, column=1, padx=5, pady=10, sticky='w')

        # Gender input
        ttk.Label(
            self.calorie_input_frame, 
            text="Gender:",
            bootstyle=INFO
        ).grid(row=1, column=0, padx=5, pady=10, sticky='w')
        
        self.gender_var = tk.StringVar(value='')
        self.gender_combo = ttk.Combobox(
            self.calorie_input_frame, 
            textvariable=self.gender_var, 
            width=15, 
            values=('Male', 'Female'),
            state="readonly"
        )
        self.gender_combo.grid(row=1, column=1, padx=5, pady=10, sticky='w')
        
        # Activity level input
        ttk.Label(
            self.calorie_input_frame, 
            text="Activity Level:",
            bootstyle=INFO
        ).grid(row=2, column=0, padx=5, pady=10, sticky='w')
        
        self.activity_var = tk.StringVar(value='')
        self.activity_combo = ttk.Combobox(
            self.calorie_input_frame, 
            textvariable=self.activity_var, 
            width=15,
            values=('Sedentary', 'Light', 'Moderate', 'Active'),
            state="readonly"
        )
        self.activity_combo.grid(row=2, column=1, padx=5, pady=10, sticky='w')
        
        # Today's calorie input
        ttk.Label(
            self.calorie_input_frame, 
            text="Today's Calories:",
            bootstyle=INFO
        ).grid(row=3, column=0, padx=5, pady=10, sticky='w')
        
        self.today_calorie_input = ttk.Entry(self.calorie_input_frame, width=15)
        self.today_calorie_input.grid(row=3, column=1, padx=5, pady=10, sticky='w')
        
        # Check calorie button
        self.check_calorie_btn = ttk.Button(
            self.calorie_input_frame, 
            text="Check Calorie Intake", 
            command=self.check_calories,
            bootstyle=SUCCESS
        )
        self.check_calorie_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=15, sticky='ew')
        
        # ------ CALORIE DIAGRAM SECTION ------
        self.calorie_diagram_frame = ttk.Labelframe(
            self.calorie_frame, 
            text="Weekly Calorie Intake Visualization",
            padding=15,
            bootstyle=PRIMARY
        )
        self.calorie_diagram_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        # Prepare bar chart
        self.calorie_figure = Figure(figsize=(5, 4), dpi=100)
        self.calorie_plot = self.calorie_figure.add_subplot(111)
        self.calorie_canvas = FigureCanvasTkAgg(self.calorie_figure, self.calorie_diagram_frame)
        self.calorie_canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # ------ CALORIE ANALYSIS RESULTS SECTION ------
        self.calorie_results_frame = ttk.Labelframe(
            self.calorie_frame, 
            text="Calorie Analysis Results",
            padding=15,
            bootstyle=SUCCESS
        )
        self.calorie_results_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        # Calorie analysis results label
        self.calorie_results_label = ttk.Label(
            self.calorie_results_frame, 
            text="Enter data to see calorie analysis", 
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        self.calorie_results_label.pack(fill=X, pady=5)
        
        self.calorie_details_label = ttk.Label(
            self.calorie_results_frame, 
            text="", 
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        self.calorie_details_label.pack(fill=X, pady=5)
        
        # Display initial bar chart
        self.update_bar_chart()
        
    # ------ FUNCTIONS TO CALCULATE MACRONUTRIENTS ------
    def calculate_macros(self):
        """Calculate and display macronutrient distribution"""
        try:
            # Get user input values
            carbs = float(self.carb_input.get())
            protein = float(self.protein_input.get())
            fat = float(self.fat_input.get())
            
            # Convert to calories
            # 1g carbohydrate = 4 calories
            # 1g protein = 4 calories
            # 1g fat = 9 calories
            carb_calories = carbs * 4  
            protein_calories = protein * 4
            fat_calories = fat * 9
            
            total_calories = carb_calories + protein_calories + fat_calories
            
            # Calculate percentages
            if total_calories > 0:
                carb_percent = (carb_calories / total_calories) * 100
                protein_percent = (protein_calories / total_calories) * 100
                fat_percent = (fat_calories / total_calories) * 100
            else:
                carb_percent = protein_percent = fat_percent = 0
            
            # Update pie chart
            self.macro_plot.clear()
            values = [carb_percent, protein_percent, fat_percent]
            labels = [f'Carbs\n({carb_percent:.1f}%)', 
                     f'Protein\n({protein_percent:.1f}%)', 
                     f'Fat\n({fat_percent:.1f}%)']
            colors = ['#3498db', '#2ecc71', '#e74c3c']  # Blue, Green, Red
            explode = (0.05, 0.05, 0.05)
            
            self.macro_plot.pie(values, labels=labels, autopct='%1.1f%%', 
                             startangle=90, explode=explode, colors=colors, shadow=True)
            self.macro_plot.set_title('Macronutrient Distribution')
            self.macro_figure.tight_layout()
            self.macro_canvas.draw()
            
            # Check balance against recommended values
            # Recommendation: 50% carbs, 20% protein, 30% fat
            carb_diff = abs(carb_percent - 50)
            protein_diff = abs(protein_percent - 20)
            fat_diff = abs(fat_percent - 30)
            
            avg_diff = (carb_diff + protein_diff + fat_diff) / 3
            
            # Determine status based on average difference
            if avg_diff <= 5:
                status = "very close to"
                self.macro_results_label.configure(bootstyle=SUCCESS)
            elif avg_diff <= 10:
                status = "close to"
                self.macro_results_label.configure(bootstyle=INFO)
            elif avg_diff <= 15:
                status = "somewhat different from"
                self.macro_results_label.configure(bootstyle=WARNING)
            else:
                status = "very different from"
                self.macro_results_label.configure(bootstyle=DANGER)
            
            # Format result message
            message = f"Your macronutrient balance is {status} the recommended intake."
            details = f"Your breakdown: {carb_percent:.0f}% Carbs, {protein_percent:.0f}% Protein, {fat_percent:.0f}% Fat."
            
            # Update result labels
            self.macro_results_label.config(text=message)
            self.macro_details_label.config(text=details)
            
        except ValueError:
            # Show error if input is not numeric
            messagebox.showerror("Error", "Please enter valid numeric values.")
    
    # ------ FUNCTIONS TO READ CALORIE DATA FROM FILE ------
    def read_calorie_data(self):
        """Read calorie history data from file"""
        # Default data for last 7 days
        today = datetime.now()
        for i in range(7):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            self.calorie_data[date] = 0
        
        # Default values if file doesn't exist
        self.recommended_calories = 0
        self.min_calories = 0
        self.max_calories = 0
        
        # Try to read file if exists
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    
                    # Ensure data exists for last 7 days
                    for i in range(7):
                        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                        if date not in data:
                            data[date] = 0
                    
                    # Only keep last 7 days data
                    dates_to_keep = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
                    self.calorie_data = {k: data[k] for k in dates_to_keep if k in data}
                    
                    # Read user profile if exists
                    if 'user_profile' in data:
                        self.user_profile = data['user_profile']
                    else:
                        self.user_profile = {}
                        
                    # Read recommended calories if exists
                    if 'recommended_calories' in data:
                        self.recommended_calories = data['recommended_calories']
                        self.min_calories = data['min_calories']
                        self.max_calories = data['max_calories']
            except Exception as e:
                print(f"Error reading data: {e}")
                self.user_profile = {}
        else:
            self.user_profile = {}
        
    # ------ FUNCTIONS TO SAVE CALORIE DATA TO FILE ------
    def save_calorie_data(self):
        """Save calorie history data to file"""
        data = {
            **self.calorie_data,
            'user_profile': self.user_profile,
            'recommended_calories': self.recommended_calories,
            'min_calories': self.min_calories,
            'max_calories': self.max_calories
        }
        try:
            with open(self.filename, 'w') as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Error saving data: {e}")
            messagebox.showerror("Error", f"Failed to save data: {e}")
    
    # ------ FUNCTIONS TO CHECK DAILY CALORIE INTAKE ------
    def check_calories(self):
        """Check daily calorie intake"""
        try:
            # Get user input values
            age = int(self.age_input.get())
            gender = self.gender_var.get()
            activity = self.activity_var.get().lower()
            today_calories = float(self.today_calorie_input.get())
            
            # Default weight and height based on gender
            if gender.lower() == 'male':
                weight = 70  # kg
                height = 170  # cm
            else:  # female
                weight = 60  # kg
                height = 160  # cm
            
            # Save to user profile
            self.user_profile = {
                'age': age,
                'gender': gender,
                'activity': activity
            }
            
            # Calculate BMR using Mifflin-St Jeor equation
            if gender.lower() == 'male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:  # female
                bmr = 10 * weight + 6.25 * height - 5 * age - 161
            
            # Activity multipliers
            activity_factors = {
                'sedentary': 1.2,  # Little to no exercise
                'light': 1.375,    # Light exercise 1-3 days/week
                'moderate': 1.55,  # Moderate exercise 3-5 days/week
                'active': 1.725,    # Hard exercise 6-7 days/week
            }
            
            # Calculate recommended daily calories
            recommended_calories = bmr * activity_factors.get(activity, 1.2)
            
            # Update recommended calories value
            self.recommended_calories = recommended_calories
            
            # Set range (±10% of recommendation)
            self.min_calories = math.ceil(recommended_calories * 0.97 / 100) * 100
            self.max_calories = math.ceil(recommended_calories * 1.05 / 100) * 100
            
            # Save today's calories
            today = datetime.now().strftime("%Y-%m-%d")
            self.calorie_data[today] = today_calories
            
            # Save data to file
            self.save_calorie_data()
            
            # Update bar chart
            self.update_bar_chart()
            
            # Determine status message based on calorie intake
            if today_calories < self.min_calories:
                if self.min_calories - today_calories <= 200:
                    status = f"slightly below (under the recommended range of {self.min_calories:.0f}-{self.max_calories:.0f} kcal)"
                    self.calorie_results_label.configure(bootstyle=WARNING)
                else:
                    status = f"low (under the recommended range of {self.min_calories:.0f}-{self.max_calories:.0f} kcal)"
                    self.calorie_results_label.configure(bootstyle=DANGER)
            elif today_calories > self.max_calories:
                if today_calories - self.max_calories <= 200:
                    status = f"slightly above the recommended range ({self.min_calories:.0f}-{self.max_calories:.0f} kcal for your profile)"
                    self.calorie_results_label.configure(bootstyle=WARNING)
                else:
                    status = f"above the recommended range ({self.min_calories:.0f}-{self.max_calories:.0f} kcal for your profile)"
                    self.calorie_results_label.configure(bootstyle=DANGER)
            else:
                status = f"within the recommended range ({self.min_calories:.0f}-{self.max_calories:.0f} kcal for your profile)"
                self.calorie_results_label.configure(bootstyle=SUCCESS)
            
            # Update result label
            message = f"Your calorie intake is {status}."
            self.calorie_results_label.config(text=message)
            
        except ValueError:
            # Show error if input is not numeric
            messagebox.showerror("Error", "Please enter valid numeric values.")
    
    # ------ FUNCTIONS TO UPDATE BAR CHART ------
    def update_bar_chart(self):
        """Update bar chart with latest calorie data"""
        self.calorie_plot.clear()
        
        # Get last 7 days as day names with dates
        today = datetime.now()
        dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        x_labels = [d.strftime("%m/%d") for d in dates]
        date_keys = [d.strftime("%Y-%m-%d") for d in dates]
        
        # Get calorie values
        calories = [self.calorie_data.get(date, 0) for date in date_keys]
        
        # Create bar chart
        x = np.arange(len(x_labels))
        bars = self.calorie_plot.bar(x, calories, width=0.6)
        
        # Color bars based on calorie range
        for i, bar in enumerate(bars):
            cal = calories[i]
            if cal == 0:
                bar.set_color('#cccccc')  # Gray for empty data
            elif cal < self.min_calories and self.min_calories > 0:
                bar.set_color('#ff9f1a')  # Orange for low calories
            elif cal > self.max_calories and self.max_calories > 0:
                bar.set_color('#e74c3c')  # Red for high calories
            else:
                bar.set_color('#2ecc71')  # Green for good calories
                
            # Add value labels on top of bars
            height = bar.get_height()
            if height > 0:
                self.calorie_plot.text(bar.get_x() + bar.get_width()/2., height + 50,
                                    f"{height:.0f}", ha='center', va='bottom')
        
        # Set y-axis limits
        highest_calories = max(max(calories) if calories else 0, self.max_calories * 1.2) 
        if highest_calories <= 0:
            highest_calories = 3000  # Default value if no data
        self.calorie_plot.set_ylim(0, highest_calories * 1.2)
        
        # Add recommended range lines
        if self.recommended_calories > 0:
            self.calorie_plot.axhline(y=self.recommended_calories, color='green', linestyle='-', linewidth=2, label=f'Recommended: {self.recommended_calories:.0f} kcal')
            self.calorie_plot.axhline(y=self.min_calories, color='orange', linestyle='--', linewidth=1, label=f'Min: {self.min_calories:.0f} kcal')  
            self.calorie_plot.axhline(y=self.max_calories, color='red', linestyle='--', linewidth=1, label=f'Max: {self.max_calories:.0f} kcal')
            
            # Add colored area for recommended range
            self.calorie_plot.axhspan(self.min_calories, self.max_calories, alpha=0.1, color='green')
        
        # Set x-axis labels
        self.calorie_plot.set_xticks(x)
        self.calorie_plot.set_xticklabels(x_labels, rotation=45)
        
        # Add labels and title
        self.calorie_plot.set_xlabel("Date")
        self.calorie_plot.set_ylabel("Calories")
        self.calorie_plot.set_title('Last 7 Days Calorie Intake')
        
        # Add legend if there are recommended calories
        if self.recommended_calories > 0:
            self.calorie_plot.legend(loc='lower left', fontsize='small')
        
        # Update display
        self.calorie_figure.tight_layout()
        self.calorie_canvas.draw()
    
    # ------ FUNCTION WHEN CLOSING APPLICATION ------
    def on_close(self):
        # Save data before closing application
        self.save_calorie_data()
        self.window.destroy()

# ------ MAIN PROGRAM ------
if __name__ == "__main__":
    # Create application window with 'litera' theme
    window = ttk.Window(themename="litera")
    
    # Run application
    app = NutritionApp(window)
    
    # Set function to run when closing application
    window.protocol("WM_DELETE_WINDOW", app.on_close)
    
    # Run main application loop
    window.mainloop()