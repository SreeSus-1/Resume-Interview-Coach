from agents.base_agent import BaseAgent

class BehavioralInterviewAgent(BaseAgent):
    def generate_questions(self, target_role: str, career_goal: str) -> str:
        prompt = f"""
        You are a Behavioral Interview Agent.

        Generate 5 behavioral interview questions for:
        Target Role: {target_role}
        Career Goal: {career_goal}

        Focus on teamwork, leadership, challenges, problem-solving, and communication.
        """
        return self.call_ollama(prompt)

    def review_answer(self, question: str, answer: str, target_role: str) -> str:
        prompt = f"""
        You are a Behavioral Interview Coach.

        Review the following interview answer.

        Target Role: {target_role}
        Question: {question}
        Answer: {answer}

        Provide:
        - strengths
        - weaknesses
        - STAR structure feedback
        - improvement suggestions
        - improved answer tips
        """
        return self.call_ollama(prompt)