import random
import subprocess
import json
from typing import List, Optional

import requests
from mcp.server.fastmcp import FastMCP

from tools.nuclei import run_nuclei
from tools.ffuf import run_ffuf
from tools.wfuzz import run_wfuzz
from tools.sqlmap import run_sqlmap
from tools.nmap import run_nmap
from tools.hashcat import run_hashcat
from tools.httpx import run_httpx
from tools.subfinder import run_subfinder
from tools.tlsx import run_tlsx
from tools.xsstrike import run_xsstrike
from tools.ipinfo import run_ipinfo
from tools.amass import amass_wrapper
from tools.dirsearch import dirsearch_wrapper
from tools.gospider import gospider_wrapper, gospider_crawl_with_filter
from tools.arjun import arjun_wrapper, arjun_bulk_scan, arjun_with_custom_payloads

# Create server
mcp = FastMCP(name="secops-mcp",
    version="1.0.0"
)


@mcp.tool()
def nuclei_scan_wrapper(
    target: str,
    templates: Optional[List[str]] = None,
    severity: Optional[str] = None,
    output_format: str = "json",
) -> str:
    """Wrapper for running a Nuclei security scan."""
    return run_nuclei(target, templates, severity, output_format)


@mcp.tool()
def ffuf_wrapper(
    url: str,
    wordlist: str,
    filter_code: Optional[str] = "404",
) -> str:
    """Wrapper for running ffuf fuzzing."""
    return run_ffuf(url, wordlist, filter_code)


@mcp.tool()
def wfuzz_wrapper(
    url: str,
    wordlist: str,
    filter_code: Optional[str] = "404",
) -> str:
    """Wrapper for running wfuzz fuzzing."""
    return run_wfuzz(url, wordlist, filter_code)


@mcp.tool()
def sqlmap_wrapper(
    url: str,
    risk: Optional[int] = 1,
    level: Optional[int] = 1,
) -> str:
    """Wrapper for running SQLMap scan."""
    return run_sqlmap(url, risk, level)


@mcp.tool()
def nmap_wrapper(
    target: str,
    ports: Optional[str] = None,
    scan_type: Optional[str] = "sV",
) -> str:
    """Wrapper for running Nmap scan."""
    return run_nmap(target, ports, scan_type)


@mcp.tool()
def hashcat_wrapper(
    hash_file: str,
    wordlist: str,
    hash_type: str,
) -> str:
    """Wrapper for running Hashcat password cracking."""
    return run_hashcat(hash_file, wordlist, hash_type)


@mcp.tool()
def httpx_wrapper(
    urls: List[str],
    status_codes: Optional[List[int]] = None,
) -> str:
    """Wrapper for running HTTPX scan."""
    return run_httpx(urls, status_codes)


@mcp.tool()
def subfinder_wrapper(
    domain: str,
    recursive: bool = False,
) -> str:
    """Wrapper for running Subfinder subdomain enumeration."""
    return run_subfinder(domain, recursive)


@mcp.tool()
def tlsx_wrapper(
    host: str,
    port: Optional[int] = 443,
) -> str:
    """Wrapper for running TLSX scan."""
    return run_tlsx(host, port)


@mcp.tool()
def xsstrike_wrapper(
    url: str,
    crawl: bool = False,
) -> str:
    """Wrapper for running XSStrike scan."""
    return run_xsstrike(url, crawl)


@mcp.tool()
def ipinfo_wrapper(
    ip: Optional[str] = None,
) -> str:
    """Wrapper for getting IP information using ipinfo.io."""
    return run_ipinfo(ip)


@mcp.tool()
def amass_wrapper(
    domain: str,
    passive: bool = True,
) -> str:
    """Wrapper for running Amass subdomain enumeration."""
    return amass_wrapper(domain, passive)


@mcp.tool()
def dirsearch_wrapper(
    url: str,
    extensions: Optional[List[str]] = None,
    wordlist: Optional[str] = None,
) -> str:
    """Wrapper for running Dirsearch directory brute forcing."""
    return dirsearch_wrapper(url, extensions, wordlist)


@mcp.tool()
def gospider_scan(
    target: str,
    depth: int = 3,
    concurrent: int = 10,
    timeout: int = 10,
    user_agent: Optional[str] = None,
    headers: Optional[List[str]] = None,
    include_subs: bool = False,
    include_other_source: bool = False,
    output_format: str = "json"
) -> str:
    """Wrapper for running Gospider web crawling."""
    result = gospider_wrapper(
        target=target,
        depth=depth,
        concurrent=concurrent,
        timeout=timeout,
        user_agent=user_agent,
        headers=headers,
        include_subs=include_subs,
        include_other_source=include_other_source,
        output_format=output_format
    )
    return json.dumps(result, indent=2)


@mcp.tool()
def gospider_filtered_scan(
    target: str,
    extensions: Optional[List[str]] = None,
    exclude_extensions: Optional[List[str]] = None,
    filter_length: Optional[int] = None,
    depth: int = 3,
    concurrent: int = 10,
    timeout: int = 10,
    include_subs: bool = False
) -> str:
    """Wrapper for running Gospider web crawling with filtering capabilities."""
    result = gospider_crawl_with_filter(
        target=target,
        extensions=extensions,
        exclude_extensions=exclude_extensions,
        filter_length=filter_length,
        depth=depth,
        concurrent=concurrent,
        timeout=timeout,
        include_subs=include_subs
    )
    return json.dumps(result, indent=2)


@mcp.tool()
def arjun_scan(
    url: str,
    method: str = "GET",
    wordlist: Optional[str] = None,
    headers: Optional[List[str]] = None,
    data: Optional[str] = None,
    delay: int = 0,
    timeout: int = 10,
    threads: int = 25,
    stable: bool = False,
    output_format: str = "json"
) -> str:
    """Wrapper for running Arjun HTTP parameter discovery."""
    result = arjun_wrapper(
        url=url,
        method=method,
        wordlist=wordlist,
        headers=headers,
        data=data,
        delay=delay,
        timeout=timeout,
        threads=threads,
        stable=stable,
        output_format=output_format
    )
    return json.dumps(result, indent=2)


@mcp.tool()
def arjun_bulk_parameter_scan(
    urls: List[str],
    method: str = "GET",
    wordlist: Optional[str] = None,
    threads: int = 25,
    stable: bool = False
) -> str:
    """Wrapper for running Arjun parameter discovery on multiple URLs."""
    result = arjun_bulk_scan(
        urls=urls,
        method=method,
        wordlist=wordlist,
        threads=threads,
        stable=stable
    )
    return json.dumps(result, indent=2)


@mcp.tool()
def arjun_custom_parameter_scan(
    url: str,
    method: str = "GET",
    custom_params: Optional[List[str]] = None,
    wordlist: Optional[str] = None,
    timeout: int = 10,
    threads: int = 25,
    stable: bool = False
) -> str:
    """Wrapper for running Arjun with custom parameter testing."""
    result = arjun_with_custom_payloads(
        url=url,
        method=method,
        custom_params=custom_params,
        wordlist=wordlist,
        timeout=timeout,
        threads=threads,
        stable=stable
    )
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")