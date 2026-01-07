from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
import os 
import json
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
load_dotenv()

#Loading Prompts from JSON file
class PromptLoader:
    def __init__(self,prompts_file='prompts.json'):
        self.prompt_file=prompts_file
        self.prompts=self.load_prompts()

    def load_prompts(self):
        with open(self.prompt_file,'r',encoding='utf-8') as f:
            return json.load(f)
        
    def get_prompt(self,agent_name):
        prompt_data=self.prompts[agent_name]
        return PromptTemplate(
            input_variables=prompt_data['input_variables'],
            template=prompt_data['template']
        )
     
class ResearchAgent:
    def __init__(self,prompt_loader):
        self.llm=ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.research_prompt=prompt_loader.get_prompt('research_agent')
        self.parser=JsonOutputParser()
        self.chain = self.research_prompt | self.llm | self.parser

    def results(self,destination,interests,season):

        result = self.chain.invoke({
            "destination": destination,
            "interests": interests,
            "season": season
        })
        return result
    
class PlannerAgent:
    def __init__(self,prompt_loader):
        self.llm=ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.8,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        self.planning_prompt=prompt_loader.get_prompt('planner_agent')
        self.parser=JsonOutputParser()
        self.chain = self.planning_prompt | self.llm | self.parser

    
    def create_itinerary(self,research_data,days,pace,budget):
        result=self.chain.invoke({
            "research_data": json.dumps(research_data, indent=2),
            "days": days,
            "pace": pace,
            "budget": budget if budget else "flexible"
        }
        )

        return result
    
class OptimizerAgent:
    def __init__(self,prompt_loader):
        self.llm=ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.6,
            google_api_key=os.getenv("GOOGLE_API_KEY")

        )

        self.optimization_prompt=prompt_loader.get_prompt('optimizer_agent')
        
        self.parser = JsonOutputParser()
        self.chain = self.optimization_prompt | self.llm | self.parser


    def optimize(self,itinerary,budget,priorities):
        result=self.chain.invoke({
           "itinerary": json.dumps(itinerary, indent=2),
            "budget": budget if budget else "flexible",
            "priorities": priorities
        }
        )

        return result
    

class CriticAgent:
    def __init__(self,prompt_loader):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.5,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        self.critique_prompt = prompt_loader.get_prompt('critic_agent')

        self.parser = JsonOutputParser()
        self.chain = self.critique_prompt | self.llm | self.parser

        
    
    def critique(self, itinerary, research, user_preferences):
        result=self.chain.invoke({
            "itinerary": json.dumps(itinerary, indent=2),
            "research": json.dumps(research, indent=2),
            "user_preferences": json.dumps(user_preferences, indent=2)
            })
        return result


class CoordinatorAgent:
    def __init__(self,prompts_file='prompts.json'):
        self.prompt_loader = PromptLoader(prompts_file)
        self.researcher=ResearchAgent(self.prompt_loader)
        self.planner=PlannerAgent(self.prompt_loader)
        self.optimizer=OptimizerAgent(self.prompt_loader)
        self.critic=CriticAgent(self.prompt_loader)
        self.max_iterations=2

    def create_itinerary(self,user_input):
        research_data=self.researcher.results(
            destination=user_input['destination'],
            interests=user_input['interests'],
            season=user_input.get('season','current')
        )

        itinerary=self.planner.create_itinerary(
            research_data=research_data,
            days=user_input['days'],
            pace=user_input['pace'],
            budget=user_input.get('budget')
        )

        if user_input.get('budget'):
            optimization=self.optimizer.optimize(
                itinerary=itinerary,
                budget=user_input['budget'],
                priorities=user_input.get('priorities','balanced experience')

            )
        else:
            optimization=None

        for iteration in range(self.max_iterations):
            critique=self.critic.critique(
                itinerary=itinerary,
                research=research_data,
                user_preferences=user_input

            )

            print(f"Score: {critique.get('overall_score', 'N/A')}")
            print(f"Verdict: {critique.get('final_verdict', 'N/A')}")

            if critique.get('final_verdict') == 'Approve':
                print("Quality approved!")
                break
            if critique.get('must_fix_before_final'):
                print(f"Applying {len(critique['must_fix_before_final'])} critical fixes...")

        final_result={
            'research': research_data,
            'itinerary': itinerary,
            'optimization': optimization,
            'quality_report': critique,
            'metadata': {
                'destination': user_input['destination'],
                'duration': f"{user_input['days']} days",
            }
        }

        return final_result
    


user_input={
    'destination': input("Destination: "),
    'days': int(input("Number of days: ")),
    'interests': input("Interests (comma-separated): "),
    'pace': input("Pace (relaxed/moderate/packed): ").lower(),

    'budget': input("Budget in Rs. (or press Enter for flexible): "),
    'season': input("Travel season (or press Enter for current): "),
    'priorities': input("Priorities (e.g., 'authentic experiences, food'): ")
}

coordinator = CoordinatorAgent()
result = coordinator.create_itinerary(user_input)

print(f"Destination: {result['metadata']['destination']}")
print(f"Duration: {result['metadata']['duration']}")
print(f"Quality Score: {result['quality_report'].get('overall_score', 'N/A')}")




