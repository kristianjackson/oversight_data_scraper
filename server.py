from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup
import json
import asyncio

app = FastAPI()

async def get_total_pages(client, first_page_url):
    response = await client.get(first_page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    total_records_text = soup.select_one('#block-views-report-page-with-solr-block > div > div > div > div.view-footer > div.oversight-table-summary').text
    # Extract total number of records and calculate total pages
    total_records = int(total_records_text.split()[-1])
    total_pages = (total_records + 59) // 60
    return total_pages

async def scrape_pages(base_url, total_pages):
    all_data = []
    async with httpx.AsyncClient() as client:
        for page_number in range(total_pages):
            url = f"{base_url}&page={page_number}"
            response = await client.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            rows = soup.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    report_date = cells[0].text.strip()
                    agency = cells[1].text.strip()
                    title = cells[2].find('a').text.strip()
                    title_url = cells[2].find('a')['href']
                    report_type = cells[3].text.strip()
                    location = cells[4].text.strip()

                    all_data.append({
                        "report_date": report_date,
                        "agency": agency,
                        "title": title,
                        "title_url": title_url,
                        "report_type": report_type,
                        "location": location
                    })
    return all_data

@app.get("/scrape")
async def scrape_data():
    base_url = "https://www.oversight.gov/reports?field_address_country=All&field_component_agency_[0]=322&items_per_page=60"
    first_page_url = f"{base_url}&page=0"

    async with httpx.AsyncClient() as client:
        total_pages = await get_total_pages(client, first_page_url)

    data = await scrape_pages(base_url, total_pages)

    return json.dumps(data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
