from fastapi import APIRouter,HTTPException , Depends

from pydantic import BaseModel, Field
from typing import List, Optional
from agent.research_agent import research_agent


router = APIRouter(prefix="/agent",tags=["agent"])

class ResearchRequest(BaseModel):
    query: str = Field(description="search query for the startup")

class CompanyProfileResponse(BaseModel):
    name: str
    founded_year : Optional[str]
    founders: Optional[str]
    website: Optional[str]
    description : Optional[str]
    tech_stack : Optional[str]
    funding_info : Optional[str]
    yc_batch : Optional[str]


class ResearchResponse(BaseModel):
    query: str
    companies : List[CompanyProfileResponse]
    report : str


@router.post("/query",response_model=ResearchResponse)
async def research_startups(request:ResearchRequest):
    result = research_agent(request.query)

    return ResearchResponse(
        query=result["query"],
        companies=result["companies"],
        report=result["report"]
    )

