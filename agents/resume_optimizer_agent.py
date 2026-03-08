from agents.base_agent import BaseAgent

class ResumeOptimizerAgent(BaseAgent):
    def run(self, resume_text: str, career_goal: str, target_role: str) -> str:
        prompt = f"""
        You are a Resume Optimizer Agent.

        Review the following resume and provide improvement suggestions.

        Career Goal: {career_goal}
        Target Role: {target_role}

        Focus on:
        - summary improvement
        - bullet point impact
        - relevant skills
        - keyword alignment
        - clarity and structure
        - missing information

        Resume:
        {resume_text[:5000]}
        """
        return self.call_ollama(prompt)