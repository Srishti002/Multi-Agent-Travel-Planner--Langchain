# Multi-Agent-Travel-Planner-Langchain
This project uses a well defined agent architecture to research destinations,create personlized itineraries,optimize budgets and ensure quality through iterative critique.

### 1. Research Agent: 
- This agent will conduct comprehensive destination research.
- Input : destination,season,interests
- Matches activities to user interests,provides seasonal analysis
- Output: Structured JSON with destination profile, activity recommendations, seasonal insights, and insider tips.

### 2. Planner Agent : 
- Creates detailed day by day itineraries using Reasoning + Action methodology.
- Input: research data, days,budget,pace
- Output:  Complete itinerary with daily themes, activities, timings, costs, reasoning, and backup options.

### 3. Optimizer Agent: 
- Performs cost benefit analysis and budget optimization.
- Calculate costs, identify expensive items, find savings
- Suggest alternatives, identify splurge vs. save opportunities
- Explain cost savings vs. experience impact
- Input: Itinerary,budget,priorities
- Output: Well detailed optimization report with current vs. optimized costs, strategies, and recommendations.

### 4. Critic Agent: 
- Quality assurance through multiple critique.
- input: itinerary,user preferances, research
- Output: Detailed critique with overall score out of 10, strengths, weaknesses, issues by severity, and improvement suggestions.
- Final verdict: Approve/Needs Revision/Major Rework.

### 5. Coordinator Agent: 
- Orchestrates all agents and manages the planning workflow.






