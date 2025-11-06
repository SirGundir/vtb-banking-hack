import tldextract


def get_base_domain(host: str):
    referer_ext = tldextract.extract(host)
    suffix = f".{referer_ext.suffix}" if referer_ext.suffix else ''
    return f"{referer_ext.domain}{suffix}"
