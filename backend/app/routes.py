from fastapi import APIRouter, HTTPException
from app.crawler import LinkedInCrawler
from app.credentials import get_credentials

router = APIRouter()

@router.post("/crawl")
def crawl_linkedin(profiles: list[str]):
    try:
        username, password = get_credentials()
        crawler = LinkedInCrawler(username, password)
        results = crawler.crawl_profiles(profiles)
        return {"profiles": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
