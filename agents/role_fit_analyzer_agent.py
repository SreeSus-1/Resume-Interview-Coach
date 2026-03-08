from agents.base_agent import BaseAgent

class RoleFitAnalyzerAgent(BaseAgent):
    def run(self, resume_text: str, career_goal: str, target_role: str, job_description: str) -> str:
        prompt = f"""
        You are a Role-Fit Analyzer Agent.

        Analyze how well the following profile fits the target role.

        Career Goal: {career_goal}
        Target Role: {target_role}
        Job Description:
        {job_description[:3000]}

        Resume:
        {resume_text[:4000]}

        Provide:
        - strengths
        - matching qualifications
        - skill gaps
        - readiness assessment
        - recommendations to improve fit
        """
        return self.call_ollama(prompt)