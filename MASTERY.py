import openai
import tkinter as tk
import os
import json
from datetime import datetime, timedelta
from tkvideo import tkvideo

# OpenAI API key to allow for the usage of ChatGPT
openai.api_key = "" # User pastes their personal API key

class MASTERY:
    
    def __init__(self, root):
        
        # Initialisng
        self.root = root
        self.root.title('MASTERY')
        self.root.configure(bg="gray")
        self.root.iconphoto(True, tk.PhotoImage(file = "MASTERY_MEDIA/MASTERY_BOOK.png"))
        self.mnlogo = tk.PhotoImage(file = "MASTERY_MEDIA/MASTERY_TEXT.png")

        # File paths for storing data
        self.progress_file = "progress.txt"
        self.spaced_repetition_file = "spaced_repetition_schedule.txt"

        # Initialise progress file if not present
        self.initialise_progress()

        # Set up the main dashboard
        self.setup_dashboard()

    def initialise_progress(self):
        
        # Check if the progress file exists, if not then create it
        if not os.path.exists(self.progress_file):
        
            with open(self.progress_file, "w") as file:
        
                json.dump({"total_quizzes": 0, "total_score": 0, "activities": {}, "quiz_history": []}, file)
        
        if not os.path.exists(self.spaced_repetition_file):
        
            with open(self.spaced_repetition_file, "w") as file:
        
                json.dump({}, file)

    def load_progress(self):
        
        # Load progress data from the file
        with open(self.progress_file, "r") as file:
        
            return json.load(file)

    def save_progress(self, progress_data):

        # Save updated progress data to the file
        with open(self.progress_file, "w") as file:

            json.dump(progress_data, file)

    def load_spaced_repetition(self):
        
        # Load spaced repetition schedule from the file
        with open(self.spaced_repetition_file, "r") as file:
        
            return json.load(file)

    def save_spaced_repetition(self, schedule):

        # Save the spaced repetition schedule to the file
        with open(self.spaced_repetition_file, "w") as file:
        
            json.dump(schedule, file)

    def setup_dashboard(self):

        self.clear_window()
        
        tk.Label(self.root, image=self.mnlogo).pack(pady=20)
        
        tk.Button(self.root, text="Interactive Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.root, text="View Progress", command=self.view_progress).pack(pady=10)
        tk.Button(self.root, text="Performance Analytics", command=self.performance_analytics).pack(pady=10)
        tk.Button(self.root, text="Spaced Repetition Schedule", command=self.spaced_repetition_schedule).pack(pady=10)
        tk.Button(self.root, text="Watch Animated Videos", command=self.animated_videos).pack(pady=10)
        tk.Button(self.root, text="Chat with AI", command=self.chat_with_ai).pack(pady=10)

    def clear_window(self):

        for widget in self.root.winfo_children():
        
            widget.destroy()

    # Interactive Quiz
    def start_quiz(self):

        self.clear_window()

        tk.Label(self.root, image=self.mnlogo).pack(pady=20)
        
        self.current_question_index = 0
        self.score = 0
        self.start_time = datetime.now()

        # List of questions
        self.questions = [
            {"prompt": "What is 2 + 2?", "answer": "4"},
            {"prompt": "What is the capital of France?", "answer": "Paris"},
            {"prompt": "Who wrote 'Hamlet'?", "answer": "Shakespeare"}
        ]

        # Display the first question
        self.display_question()

    def display_question(self):

        if self.current_question_index < len(self.questions):
            
            question = self.questions[self.current_question_index]

            self.clear_window()

            tk.Label(self.root, image=self.mnlogo).pack(pady=20)

            tk.Label(self.root, text=question["prompt"], font=('Arial', 18)).pack(pady=20)

            # Input field for user's answer
            self.answer_entry = tk.Entry(self.root, font=('Arial', 18))
            self.answer_entry.pack(pady=10)

            tk.Button(self.root, text="Submit", command=self.check_answer).pack(pady=10)
        
        else:

            # If no more questions, show the final score
            self.show_final_score()

    def check_answer(self):

        user_answer = self.answer_entry.get().strip()
        correct_answer = self.questions[self.current_question_index]["answer"]

        # Immediate feedback
        if user_answer.lower() == correct_answer.lower():

            self.score += 1
            feedback = "Correct!"

        else:

            feedback = f"Incorrect. The correct answer was: {correct_answer}"

        # Display feedback and move to the next question
        self.current_question_index += 1
        self.clear_window()
        tk.Label(self.root, text=feedback, font=('Arial', 18)).pack(pady=20)
        tk.Button(self.root, text="Next Question", command=self.display_question).pack(pady=10)

    def show_final_score(self):

        self.clear_window()

        tk.Label(self.root, image=self.mnlogo).pack(pady=20)

        # Calculate time taken for the quiz
        end_time = datetime.now()
        time_taken = (end_time - self.start_time).seconds

        # Load current progress data
        progress = self.load_progress()
        quiz_history = progress.get("quiz_history", [])
        quiz_history.append({"score": self.score, "time_taken": time_taken})

        # Update progress and save
        progress["quiz_history"] = quiz_history
        self.save_progress(progress)

        tk.Label(
            self.root,
            text=f"Quiz Complete! Your score: {self.score}/{len(self.questions)}",
            font=('Arial', 18)
        ).pack(pady=20)

        tk.Label(self.root, text=f"Time Taken: {time_taken} seconds", font=('Arial', 18)).pack(pady=10)

        tk.Button(self.root, text="Back to Dashboard", command=self.setup_dashboard).pack(pady=10)

    # View Progress
    def view_progress(self):

        self.clear_window()

        tk.Label(self.root, image=self.mnlogo).pack(pady=20)

        # Load progress data
        progress = self.load_progress()
        total_quizzes = len(progress.get("quiz_history", []))
        total_score = sum(q["score"] for q in progress.get("quiz_history", []))
        average_score = total_score / total_quizzes if total_quizzes > 0 else 0

        tk.Label(self.root, text="Your Progress", font=('Arial', 24)).pack(pady=20)
        tk.Label(self.root, text=f"Total Quizzes Attempted: {total_quizzes}", font=('Arial', 18)).pack(pady=10)
        tk.Label(self.root, text=f"Total Score: {total_score}", font=('Arial', 18)).pack(pady=10)
        tk.Label(self.root, text=f"Average Score: {average_score:.2f}", font=('Arial', 18)).pack(pady=10)

        tk.Button(self.root, text="Back to Dashboard", command=self.setup_dashboard).pack(pady=10)

    # Performance Analytics
    def performance_analytics(self):

        self.clear_window()

        tk.Label(self.root, image=self.mnlogo).pack(pady=20)

        # Load progress data
        progress = self.load_progress()
        quiz_history = progress.get("quiz_history", [])
        total_quizzes = len(quiz_history)

        if total_quizzes > 0:

            # Calculate average score
            total_score = sum([entry["score"] for entry in quiz_history])
            average_score = total_score / total_quizzes

            # Calculate average time taken per quiz
            total_time = sum([entry["time_taken"] for entry in quiz_history])
            average_time = total_time / total_quizzes

            # Display analytics
            tk.Label(self.root, text="Performance Analytics", font=('Arial', 24)).pack(pady=20)
            tk.Label(self.root, text=f"Total Quizzes: {total_quizzes}", font=('Arial', 18)).pack(pady=10)
            tk.Label(self.root, text=f"Average Score: {average_score:.2f}", font=('Arial', 18)).pack(pady=10)
            tk.Label(self.root, text=f"Average Time Taken: {average_time:.2f} seconds", font=('Arial', 18)).pack(pady=10)

            # Display performance trend
            tk.Label(self.root, text="Score Trend:", font=('Arial', 18)).pack(pady=10)
            for i, entry in enumerate(quiz_history):
                tk.Label(
                    self.root,
                    text=f"Quiz {i + 1}: Score - {entry['score']}, Time - {entry['time_taken']}s",
                    font=('Arial', 14)
                ).pack(pady=5)
        
        else:

            tk.Label(self.root, text="No quiz data available.", font=('Arial', 18)).pack(pady=20)

        tk.Button(self.root, text="Back to Dashboard", command=self.setup_dashboard).pack(pady=10)

    # Spaced Repetition Scheduler
    def spaced_repetition_schedule(self):

        self.clear_window()

        tk.Label(self.root, image=self.mnlogo).pack(pady=20)

        # Load progress and current schedule
        progress = self.load_progress()
        schedule = self.load_spaced_repetition()
        activities = progress.get("activities", {})

        # Generate review dates based on performance
        today = datetime.now().strftime("%Y-%m-%d")

        for activity, data in activities.items():

            avg_score = data.get("average_score", 0)
            last_review_date = schedule.get(activity, {}).get("last_review", today)

            # Calculate the next review date
            if avg_score < 50:

                interval = 1  # Review tomorrow

            elif avg_score < 80:

                interval = 3  # Review in 3 days

            else:

                interval = 7  # Review in a week

            next_review_date = datetime.strptime(last_review_date, "%Y-%m-%d") + timedelta(days=interval)
            schedule[activity] = {
                "last_review": last_review_date,
                "next_review": next_review_date.strftime("%Y-%m-%d")
            }

        # Save and display the schedule
        self.save_spaced_repetition(schedule)
        self.display_spaced_repetition(schedule)

    def display_spaced_repetition(self, schedule):

        self.clear_window()

        tk.Label(self.root, image=self.mnlogo).pack(pady=20)

        tk.Label(self.root, text="Spaced Repetition Schedule", font=('Arial', 24)).pack(pady=20)

        if schedule:

            for activity, dates in schedule.items():

                tk.Label(
                    self.root,
                    text=f"{activity}: Next Review on {dates['next_review']}",
                    font=('Arial', 18)
                ).pack(pady=5)
        
        else:

            tk.Label(self.root, text="No activities scheduled for review.", font=('Arial', 18)).pack(pady=20)

        tk.Button(self.root, text="Back to Dashboard", command=self.setup_dashboard).pack(pady=10)

    # Animated Videos
    def animated_videos(self):

        self.clear_window()

        tk.Label(self.root, image=self.mnlogo).pack(pady=20)

        tk.Label(self.root, text="Animated Videos", font=('Arial', 24)).pack(pady=20)

        # List of available videos
        self.videos = [
            {"title": "Example 1", "file": "videos/ExampleVideo.mp4"},
            {"title": "Example 2", "file": "videos/ExampleVideo.mp4"},
            {"title": "Example 3", "file": "videos/ExampleVideo.mp4"}
        ]

        # Display video options
        for video in self.videos:
            
            tk.Button(self.root, text=video["title"], command=lambda v=video: self.play_video(v)).pack(pady=10)

        tk.Button(self.root, text="Back to Dashboard", command=self.setup_dashboard).pack(pady=10)

    def play_video(self, video):

        self.clear_window()

        tk.Label(self.root, image=self.mnlogo).pack(pady=20)

        tk.Label(self.root, text=video["title"], font=('Arial', 24)).pack(pady=20)

        # Video frame
        video_frame = tk.Label(self.root)
        video_frame.pack()

        # Play the video
        player = tkvideo(video["file"], video_frame, loop=1, size=(800, 450))
        player.play()

        tk.Button(self.root, text="Back to Videos", command=self.animated_videos).pack(pady=10)

    # Chat with AI
    def chat_with_ai(self):

        self.clear_window()

        tk.Label(self.root, image=self.mnlogo).pack(pady=20)

        tk.Label(self.root, text="Chat with AI", font=('Arial', 24)).pack(pady=20)

        # Display chat history
        self.chat_history_text = tk.Text(self.root, font=('Arial', 14), wrap='word', height=15, width=50)
        self.chat_history_text.pack(pady=10)
        self.chat_history_text.insert('1.0', "AI Chat Initialised...\n")
        self.chat_history_text.config(state='disabled')  # Prevent direct editing

        # Input field for the user to ask questions
        self.chat_entry = tk.Entry(self.root, font=('Arial', 18))
        self.chat_entry.pack(pady=10)

        # Send button to process the chat
        tk.Button(self.root, text="Send", command=self.process_chat).pack(pady=10)

        tk.Button(self.root, text="Back to Dashboard", command=self.setup_dashboard).pack(pady=10)

    def process_chat(self):

        user_input = self.chat_entry.get().strip()

        if not user_input:

            return  # Do nothing if input is empty

        # Display user input in chat history
        self.chat_history_text.config(state='normal')
        self.chat_history_text.insert('end', f"User: {user_input}\n")
        self.chat_history_text.config(state='disabled')  # Prevent editing again
        self.chat_history_text.see('end')  # Scroll to the latest message

        # Call the OpenAI API for response
        try:

            response = self.get_ai_response(user_input)
            self.chat_history_text.config(state='normal')
            self.chat_history_text.insert('end', f"AI: {response}\n")
            self.chat_history_text.config(state='disabled')
            self.chat_history_text.see('end')  # Scroll to the latest message

        except Exception as e:

            self.chat_history_text.config(state='normal')
            self.chat_history_text.insert('end', f"Error: {str(e)}\n")
            self.chat_history_text.config(state='disabled')
            self.chat_history_text.see('end')  # Scroll to the latest message

        # Clear the input field after sending
        self.chat_entry.delete(0, 'end')

    def get_ai_response(self, user_input):
        # Context management for multi-turn conversations
        if not hasattr(self, 'conversation_context'):
            self.conversation_context = ""

        # Append user input to context
        self.conversation_context += f"User: {user_input}\n"

        # Call the OpenAI API for response
        response = openai.Completion.create(
            engine="gpt-4",  # Adjust to your preferred engine
            prompt=f"{self.conversation_context}AI:",
            max_tokens=150,  # Adjust as needed
            stop=None
        )

        # Extract and format the response
        ai_response = response['choices'][0]['text'].strip()
        self.conversation_context += f"AI: {ai_response}\n"  # Update context with AI response

        return ai_response

root = tk.Tk()
app = MASTERY(root)
root.mainloop()