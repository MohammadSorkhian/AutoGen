import asyncio, re, time, aiohttp, json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional, Tuple
from urllib.parse import urlparse, urljoin, urldefrag
from _tools._40_webSearchSerper_tool import web_search_serper
import trafilatura
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup
from readability import Document
import fitz
from _tools._10_SearchResultScoring_tool import SearchResultScoring_tool



@dataclass
class ScrapedDocument:
    url: str
    final_url: Optional[str]
    status: Optional[int]
    title: Optional[str]
    text: Optional[str]
    html: Optional[str]
    content_type: Optional[str]
    fetched_at: Optional[datetime]
    language: Optional[str]
    meta: Dict[str, str]
    error: Optional[str]


@dataclass
class ScraperConfig:
    user_agent: str = "YourBotName/1.0 (+https://yourdomain.example/contact)"
    max_global_concurrency: int = 12
    max_concurrency_per_host: int = 2
    default_host_delay: float = 0.6
    timeout_sec: int = 25
    max_redirects: int = 5
    max_bytes: int = 2_500_000
    include_html: bool = False
    accept_language: str = "en, *;q=0.5"
    html_renderer: Optional[Callable[..., "asyncio.Future[str]"]] = None


def normalize_url(url: str) -> str:
    url, _ = urldefrag(url)
    parsed = urlparse(url)
    scheme = (parsed.scheme or "http").lower()
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"
    out = f"{scheme}://{netloc}{path}"
    if parsed.query:
        out += f"?{parsed.query}"
    return out


def should_skip_url(url: str) -> bool:
    return url.startswith(("mailto:", "javascript:", "tel:", "data:"))


def is_probably_html(content_type: Optional[str], url: str) -> bool:
    if not content_type:
        return not url.lower().endswith(".pdf")
    ct = content_type.lower()
    return ("text/html" in ct) or ("application/xhtml+xml" in ct)


def is_probably_pdf(content_type: Optional[str], url: str) -> bool:
    if content_type and "application/pdf" in content_type.lower():
        return True
    return url.lower().endswith(".pdf")


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def guess_language(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    sample = text[:3000].lower()
    tokens = [" the ", " and ", " of ", " to ", " in "]
    hits = sum(t in sample for t in tokens)
    return "en" if hits >= 2 else None


def extract_meta_title_canonical(
    html: str, base_url: str
) -> Tuple[Dict[str, str], Optional[str], Optional[str]]:
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    canonical = None
    link_canon = soup.find("link", rel=lambda v: v and "canonical" in v)
    if link_canon and link_canon.get("href"):
        canonical = urljoin(base_url, link_canon["href"].strip())
    desc = None
    meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find(
        "meta", attrs={"property": "og:description"}
    )
    if meta_desc and meta_desc.get("content"):
        desc = meta_desc["content"].strip()
    meta: Dict[str, str] = {}
    if canonical:
        meta["canonical"] = canonical
    if desc:
        meta["description"] = desc
    return meta, title, canonical


def extract_text_from_html(html: str, url: str) -> str:
    if trafilatura:
        try:
            res = trafilatura.extract(
                html,
                url=url,
                favor_precision=True,
                include_comments=False,
                include_tables=False,
            )
            if res and len(res.split()) >= 30:
                return collapse_ws(res)
        except Exception:
            pass
    if Document:
        try:
            doc = Document(html)
            main_html = doc.summary(html_partial=True)
            soup = BeautifulSoup(main_html, "lxml")
            txt = soup.get_text(separator=" ")
            if txt and len(txt.split()) >= 30:
                return collapse_ws(txt)
        except Exception:
            pass
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    txt = soup.get_text(separator=" ")
    return collapse_ws(txt)


def extract_text_from_pdf_bytes(data: bytes) -> Optional[str]:
    if not fitz:
        return None
    try:
        with fitz.open(stream=data, filetype="pdf") as doc:
            parts: List[str] = []
            for page in doc:
                parts.append(page.get_text("text"))
            return collapse_ws("\n".join(parts))
    except Exception:
        return None


class HostRateLimiter:
    def __init__(self, default_delay: float = 0.6, max_concurrency_per_host: int = 2):
        self.default_delay = default_delay
        self.max_concurrency_per_host = max_concurrency_per_host
        self._locks: Dict[str, asyncio.Semaphore] = {}
        self._last_fetch_at: Dict[str, float] = {}

    async def throttle(self, host: str):
        delay = self.default_delay
        now = time.time()
        last = self._last_fetch_at.get(host, 0.0)
        sleep_for = max(0.0, (last + delay) - now)
        if sleep_for > 0:
            await asyncio.sleep(sleep_for)
        self._last_fetch_at[host] = time.time()

    def semaphore(self, host: str) -> asyncio.Semaphore:
        if host not in self._locks:
            self._locks[host] = asyncio.Semaphore(self.max_concurrency_per_host)
        return self._locks[host]


class WebScraper:
    def __init__(self, config: ScraperConfig):
        self.cfg = config

    async def _create_session(self) -> aiohttp.ClientSession:
        connector = aiohttp.TCPConnector(
            limit=self.cfg.max_global_concurrency, ssl=False
        )
        headers = {
            "User-Agent": self.cfg.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
            "Accept-Language": self.cfg.accept_language,
        }
        return aiohttp.ClientSession(connector=connector, headers=headers)

    async def _fetch(
        self, session: aiohttp.ClientSession, limiter: HostRateLimiter, url: str
    ) -> ScrapedDocument:
        url = normalize_url(url)
        if should_skip_url(url):
            return ScrapedDocument(
                url,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                {},
                "Skipped non-http URL",
            )

        host = urlparse(url).netloc
        sem = limiter.semaphore(host)

        async with sem:
            await limiter.throttle(host)
            backoffs = [0, 1.2, 2.5]
            last_err = None

            for backoff in backoffs:
                if backoff:
                    await asyncio.sleep(backoff)
                try:
                    timeout = ClientTimeout(total=self.cfg.timeout_sec)
                    async with session.get(
                        url,
                        timeout=timeout,
                        allow_redirects=True,
                        max_redirects=self.cfg.max_redirects,
                    ) as resp:
                        status = resp.status
                        final_url = str(resp.url)
                        ctype = (resp.headers.get("content-type") or "").lower()
                        data = b""
                        async for chunk in resp.content.iter_chunked(64 * 1024):
                            data += chunk
                            if len(data) >= self.cfg.max_bytes:
                                break

                        if is_probably_pdf(ctype, final_url):
                            text = extract_text_from_pdf_bytes(data)
                            return ScrapedDocument(
                                url=url,
                                final_url=final_url,
                                status=status,
                                title=None,
                                text=text,
                                html=None,
                                content_type=ctype,
                                fetched_at=datetime.now(timezone.utc),
                                language=guess_language(text),
                                meta={"format": "pdf"},
                                error=(
                                    None
                                    if text
                                    else "PDF extraction failed or PyMuPDF missing"
                                ),
                            )

                        if not is_probably_html(ctype, final_url):
                            return ScrapedDocument(
                                url=url,
                                final_url=final_url,
                                status=status,
                                title=None,
                                text=None,
                                html=None,
                                content_type=ctype,
                                fetched_at=datetime.now(timezone.utc),
                                language=None,
                                meta={},
                                error="Non-HTML content",
                            )

                        encoding = resp.charset or "utf-8"
                        html = data.decode(encoding, errors="replace")
                        meta, title, canonical = extract_meta_title_canonical(
                            html, final_url
                        )
                        text = extract_text_from_html(html, final_url)

                        if len(text.split()) < 30 and self.cfg.html_renderer:
                            try:
                                rendered = await self.cfg.html_renderer(
                                    final_url, self.cfg.user_agent
                                )
                                if rendered:
                                    meta, title, canonical = (
                                        extract_meta_title_canonical(
                                            rendered, final_url
                                        )
                                    )
                                    text = extract_text_from_html(rendered, final_url)
                                    if self.cfg.include_html:
                                        html = rendered
                            except Exception:
                                pass

                        return ScrapedDocument(
                            url=url,
                            final_url=final_url,
                            status=status,
                            title=title,
                            text=text,
                            html=html if self.cfg.include_html else None,
                            content_type=ctype,
                            fetched_at=datetime.now(timezone.utc),
                            language=guess_language(text),
                            meta=meta,
                            error=None,
                        )
                except Exception as e:
                    last_err = str(e)

            return ScrapedDocument(
                url=url,
                final_url=None,
                status=None,
                title=None,
                text=None,
                html=None,
                content_type=None,
                fetched_at=datetime.now(timezone.utc),
                language=None,
                meta={},
                error=last_err or "Unknown error",
            )

    async def scrape(self, query: str = "") -> List[ScrapedDocument]:
        webSearchURLList = [x['link'] for x in json.loads(web_search_serper(query=query))['organic']]

        limiter = HostRateLimiter(
            default_delay=self.cfg.default_host_delay,
            max_concurrency_per_host=self.cfg.max_concurrency_per_host,
        )
        async with await self._create_session() as session:
            tasks = [self._fetch(session, limiter, url) for url in webSearchURLList]
            
            result = await asyncio.gather(*tasks)

            result = [r.text for r in result]
            results: List[ScrapedDocument] = await asyncio.gather(*tasks)
            
            return result



            return results
