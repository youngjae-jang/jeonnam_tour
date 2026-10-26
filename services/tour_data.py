"""Tour CSV loading and filtering without Streamlit dependencies."""
import pandas as pd

from config import category_label, subcategory_label
from services.validation import map_valid_mask, validate_schema


def load_tours(filepath):
    """Read and normalize the source CSV into fields used by the app."""
    try:
        df = pd.read_csv(filepath, encoding="utf-8-sig", dtype={"contentid": "string", "cat1": "string", "cat2": "string", "cat3": "string"})
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="cp949", dtype={"contentid": "string"})
    validate_schema(df)
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed:")].copy()
    for name in ("cat2", "cat3", "firstimage", "description", "modifiedtime", "createdtime", "contentid"):
        if name not in df.columns:
            df[name] = ""
    df["title"] = df["title"].fillna("").astype(str).str.strip()
    df["addr1"] = df["addr1"].fillna("").astype(str).str.strip()
    df["region"] = df["addr1"].str.extract(r"(?:전남광주통합특별시|전라남도|전남)\s+(\S+?(?:시|군))\b", expand=False).fillna("지역 미상")
    df["category"] = df["cat1"].map(category_label)
    df["subcategory"] = df["cat2"].map(subcategory_label)
    df["latitude"] = pd.to_numeric(df["mapy"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["mapx"], errors="coerce")
    df["firstimage"] = df["firstimage"].fillna("").astype(str).str.strip()
    df.loc[~df["firstimage"].str.startswith(("https://", "http://")), "firstimage"] = ""
    df["contentid"] = df["contentid"].fillna("").astype(str)
    row_ids = pd.Series(df.index, index=df.index).astype(str).radd("row-")
    df["record_id"] = df["contentid"].where(df["contentid"].ne(""), row_ids)
    return df.reset_index(drop=True)


def apply_filters(df, regions=None, categories=None, keyword="", subcategories=None, favorite_ids=None, favorites_only=False, sort_option="기본순"):
    """Apply user-selected filters and sorting to a copy of the source rows."""
    out = df.copy()
    if regions:
        out = out[out["region"].isin(regions)]
    if categories:
        out = out[out["category"].isin(categories)]
    if subcategories:
        out = out[out["subcategory"].isin(subcategories)]
    if keyword.strip():
        query = keyword.strip()
        match = out["title"].str.contains(query, case=False, regex=False, na=False) | out["addr1"].str.contains(query, case=False, regex=False, na=False) | out["region"].str.contains(query, case=False, regex=False, na=False)
        out = out[match]
    if favorites_only:
        out = out[out["record_id"].isin(favorite_ids or [])]
    rules = {"관광지명 오름차순": ("title", True), "관광지명 내림차순": ("title", False), "지역명순": ("region", True), "등록일 최신순": ("createdtime", False)}
    if sort_option in rules:
        column, ascending = rules[sort_option]
        out = out.sort_values(column, ascending=ascending, kind="stable", na_position="last")
    return out


def region_counts(df):
    return df.groupby("region", as_index=False).size().rename(columns={"size": "count"}).sort_values("count", ascending=False)


def valid_map_points(df):
    return df.loc[map_valid_mask(df)].copy()
