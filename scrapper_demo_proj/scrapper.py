import asyncio
import json
from typing import Any, Optional
import httpx
from bs4 import BeautifulSoup
from aiolimiter import AsyncLimiter
import time
from logger import log_events
from metrics import scrape_requests_total, scrape_duration_seconds, queue_depth


base_url="https://quotes.toscrape.com/"
t_out=10.0
max_retries=3
bkoff=1
total_pg=3
req_sec=2
rl=AsyncLimiter(req_sec,1)

async def fetch_retry(
    client:httpx.AsyncClient,
    url: str)-> str:
    platform="quotes"
    for att in range(max_retries):
        start=time.perf_counter()
        try:
            print(f"Requesting {url}")
            print(f"Attemp {att+1}/{max}")
            async with rl:
                response=await client.get(url)
            
            response.raise_for_status()
            duration = time.perf_counter() - start
            scrape_duration_seconds.observe(duration)
            scrape_requests_total.labels(
                platform=platform,
                status="success"
            ).inc()
            print(f"Sucess {response.status_code}")
            print(f"Scrape duration: {duration:.4f} seconds")
            return response.text
        except httpx.TimeoutException as error:
            scrape_requests_total.labels(
                platform=platform,
                status="failed"
                ).inc()
            print(f"Timeout error: {error}")
        except httpx.HTTPStatusError as error:
            scrape_requests_total.labels(
                platform=platform,
                status="failed"
                ).inc()
            print(f"HTTPS status error: {error}")
        except httpx.RequestError as error:
            scrape_requests_total.labels(
                platform=platform,
                status="failed"
                ).inc()
            print(f"Request error: {error}")
        if att==max-1:
            print("Max attemps achieved.")
            raise error
        t= bkoff *(2**att)
        print(f"retrieve in {t} seconds...")
        await asyncio.sleep(t)
    raise RuntimeError("Error: Failed to get.") 

def parse_quotes(html: str)->list[dict[str,Any]]:
    soup=BeautifulSoup(html,"html.parser",)
    results=[]
    ele=soup.select("div.quote")
    for e in ele:
        txt=e.select_one("span.text")
        a_ele=e.select_one("small.author")
        tag_ele=e.select("a.tag")
        q_txt=(txt.get_text(strip=True)
               if txt
               else "")
        a_name=(a_ele.get_text(strip=True)
                if a_ele
                else "")
        tags=[tag.get_text(strip=True)
              for tag in tag_ele ]
        results.append({
            "quote": q_txt,
            "author": a_name,
            "tags": tags
        })
    return results

async def scrap_page(client: httpx.AsyncClient, pg_no: int,)->list[dict[str,Any]]:
    url=(f"{base_url}page/"f"{pg_no}/")
    html=await fetch_retry(client,url,)
    quotes=parse_quotes(html)
    await log_events(
        "scrape_success",{
            "page": pg_no,
            "quotes": len(quotes)
            })
    print(f"Extracted {len(quotes)} quotes.")
    return quotes

def save_data(data:list[dict[str,Any]], filename: str,)->None:
    with open (filename,"w",encoding="utf-8", )as file:
        json.dump(data,file,indent=4,ensure_ascii=False)
    print(f"Saved {len(data)} records in {filename}")

async def run_scrapper()->None:
    timeout=httpx.Timeout(timeout= t_out)
    async with httpx.AsyncClient(timeout=timeout,headers={
        "User-Agent":("Mozilla/5.0 Scrapper practice/1.0")
    },) as client:
        all_quotes=[]
        queue_depth.set(total_pg)
        for pg_no in range(1, total_pg+1):
            pg_q= await scrap_page(client,pg_no,)
            all_quotes.extend(pg_q)
            queue_depth.dec()
        save_data(all_quotes,"quotes.json",)

if __name__ == "__main__":
    asyncio.run(run_scrapper())




