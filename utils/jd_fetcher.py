import re
import requests
from bs4 import BeautifulSoup


def fetch_jd(url: str) -> dict:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Could not fetch URL: {e}", "full_text": ""}

    soup = BeautifulSoup(resp.text, "lxml")

    # Remove non-content elements
    for tag in soup.find_all(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    # Try to extract title
    title = ""
    for selector in ["h1", ".job-title", "[data-automation='job-detail-title']"]:
        el = soup.select_one(selector)
        if el and el.get_text(strip=True):
            title = el.get_text(strip=True)
            break
    if not title:
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)

    # Extract main content area
    main = soup.find("main") or soup.find("article") or soup.find("body")
    if main is None:
        main = soup

    full_text = main.get_text(separator="\n", strip=True)

    # Clean up excessive blank lines
    lines = [line.strip() for line in full_text.splitlines()]
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        if not line:
            if not prev_blank:
                cleaned_lines.append("")
            prev_blank = True
        else:
            cleaned_lines.append(line)
            prev_blank = False
    full_text = "\n".join(cleaned_lines).strip()

    # Try to extract company name from meta or og tags
    company = ""
    og_site = soup.find("meta", property="og:site_name")
    if og_site and og_site.get("content"):
        company = og_site["content"]

    # Extract requirements section heuristically
    requirements = ""
    for heading in soup.find_all(["h2", "h3", "h4", "strong"]):
        text = heading.get_text(strip=True).lower()
        if any(kw in text for kw in ["requirement", "qualification", "what we're looking for",
                                      "what you bring", "your profile", "skills"]):
            sibling_text = []
            for sib in heading.find_next_siblings():
                if sib.name in ["h2", "h3", "h4"]:
                    break
                sib_text = sib.get_text(separator="\n", strip=True)
                if sib_text:
                    sibling_text.append(sib_text)
            if sibling_text:
                requirements = "\n".join(sibling_text)
                break

    # Try to find location
    location = ""
    for heading in soup.find_all(["h2", "h3", "h4", "strong", "span", "div"]):
        text = heading.get_text(strip=True).lower()
        if "location" in text:
            next_el = heading.find_next_sibling()
            if next_el:
                location = next_el.get_text(strip=True)
            break

    # Try to extract contact email
    EXCLUDED_PREFIXES = ("noreply", "no-reply", "donotreply", "do-not-reply", "mailer-daemon")
    contact_email = ""

    # Check mailto: links first
    for a_tag in soup.find_all("a", href=re.compile(r"^mailto:", re.IGNORECASE)):
        candidate = a_tag["href"].replace("mailto:", "").split("?")[0].strip().lower()
        if candidate and not any(candidate.startswith(p) for p in EXCLUDED_PREFIXES):
            contact_email = candidate
            break

    # Fall back to regex on page text
    if not contact_email:
        for match in re.finditer(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_text
        ):
            candidate = match.group(0).lower()
            if not any(candidate.startswith(p) for p in EXCLUDED_PREFIXES):
                contact_email = candidate
                break

    return {
        "title": title,
        "company": company,
        "full_text": full_text[:8000],  # Cap to avoid excessive token use
        "requirements": requirements[:3000],
        "location": location,
        "contact_email": contact_email,
    }
