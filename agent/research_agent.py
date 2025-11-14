from typing import Dict , List ,TypedDict,Optional
from langgraph.graph import StateGraph ,START,END
from langchain.tools import tool
import os
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langchain_exa import ExaSearchResults
from dotenv import load_dotenv
load_dotenv()


os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["EXA_API_KEY"] = os.getenv("EXA_API")

class CompanyProfile(BaseModel):
    """Detailed profile of a startup company"""
    name: str = Field(description="Official company name")
    founded_year: Optional[str] = Field(default="N/A", description="Year the company was founded")
    founders: Optional[str] = Field(default="N/A", description="Names of the founders")
    website: Optional[str] = Field(default="N/A", description="Company website URL")
    description: str = Field(description="Brief description of what the company does")
    tech_stack: Optional[str] = Field(default="N/A", description="Technologies used by the company")
    funding_info: Optional[str] = Field(default="N/A", description="Funding stage or amount if available")
    yc_batch: Optional[str] = Field(default="N/A", description="Y Combinator batch if applicable")



class CompanyList(BaseModel):
    """List of company profiles extracted from search results"""
    companies: List[CompanyProfile]

class State(TypedDict):
    input: str
    search_query: str
    search_result: str
    companies: Optional[List[CompanyProfile]]
    report: str

@tool
def search_internet(query: str):
    """Search the internet for startup/company information"""
    search = ExaSearchResults(exa_api_key=os.environ["EXA_API_KEY"])
    result = search._run(
        query=query,
        num_results=5,  
        text_contents_options=True,
        highlights=True,
    )
    print("inside in search internet")

    return result


llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider = "google-genai"
)

structured_llm = llm.with_structured_output(CompanyList)

def enhance_query_node(state:State):
    """Refine the user query """
    user_input = state["input"]
    refine_prompt = f"""
        Given this user query about startups: "{user_input}"
        
        Create an optimized search query that will help find:
        - Startup names and their official websites
        - Founder information
        - Company descriptions and what they build
        - Technology stack information
        - Funding and batch information (especially for YC companies)
        
        Return ONLY the optimized search query, nothing else.
        """
    refined_query = llm.invoke(refine_prompt)
    print("enchancing query")
    return {"search_query":refined_query.content}


def search_node(state: State):
    """excute the search engine"""
    query = state.get('search_query',state['input'])
    search_result = search_internet.invoke(query)
    print("search node")
    return {"search_result": search_result}


def extraction_node(state:State):
    """extract structured company information"""
    search_result = state["search_result"]
    original_query = state['input']

    extraction_prompt =  f"""
        Based on the original user query: "{original_query}"
        
        Extract information about startup companies from these search results:
        {search_result}
        
        For EACH distinct company mentioned, create a profile with all available information.
        Use "N/A" for fields where information is not available.
    """
    response = structured_llm.invoke(extraction_prompt)

    print("inside the extraction")
    return {"companies": response.companies}


def report_generation_node(state:State):
    """genrate a formatted report"""
    companies = state['companies']
    original_query = state["input"]
    
    if not companies:
        return {"report":"No companies found matching your query"}
    
    report = f"Query: {original_query}\nCompanies Found: {len(companies)}\n\n"
        
    for i, company in enumerate(companies, 1):
            report += f"{i}. {company.name}\n"
            report += f"   Website: {company.website}\n"
            report += f"   Founded: {company.founded_year}\n"
            report += f"   Founders: {company.founders}\n"
            report += f"   Description: {company.description}\n"
            report += f"   Tech Stack: {company.tech_stack}\n"
            report += f"   Funding: {company.funding_info}\n"
            report += f"   YC Batch: {company.yc_batch}\n\n"
        
    print("inside report making")
    return {"report": report}

graph_builder=StateGraph(State)

graph_builder.add_node("query_refinement",enhance_query_node)
graph_builder.add_node("search",search_node)
graph_builder.add_node("extraction",extraction_node)
graph_builder.add_node("report",report_generation_node)


graph_builder.add_edge(START,"query_refinement")
graph_builder.add_edge("query_refinement","search")
graph_builder.add_edge("search","extraction")
graph_builder.add_edge("extraction","report")
graph_builder.add_edge("report",END)


app = graph_builder.compile()

def research_agent(query : str):
    input_data = {"input":query}
    result = app.invoke(input_data)

    return {
            "query": query,
            "companies": [company.dict() for company in result.get('companies', [])],
            "report": result.get('report', ''),
            "total_companies": len(result.get('companies', []))
        }


