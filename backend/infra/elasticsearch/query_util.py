from typing import List, Any

from infra.elasticsearch.setup import es_client


"""
    For now this file only contains utility functions for Elasticsearch queries as a placeholder (for reference).
    In the future, we will like to abstract these queries into a more structured format, possibly using an ORM-like approach for Elasticsearch.
    We should also be able to chain multiple functions together to build complex queries.
"""

async def wildcard_search(query: str, offset: int = 0, limit: int = 5) -> List[Any]:
    # Performs a wildcard search
    search_body = {
        "query": {
            "wildcard": {
                "name": f"*{query}*"
            }
        },
        "from": offset,
        "size": limit
    }

    es_response = await es_client.search(
        index="organizations",
        body=search_body
    )

    organizations_ids = [hit["_source"]["id"] for hit in es_response["hits"]["hits"]]

    return organizations_ids

async def multi_match_search(fields: List[str], query: str, offset: int = 0, limit: int = 5) -> List[Any]:
    # Performs searching on multiple fields and returns matched values
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields
            }
        },
        "from": offset,
        "size": limit,
        "_source": ["id", "name", "description"] # Only retrieve necessary fields from ES
    }

    es_response = await es_client.search(
        index="organizations",
        body=search_body
    )

    organizations_ids = [hit["_source"]["id"] for hit in es_response["hits"]["hits"]]

    return organizations_ids


async def exact_match_search(field_name: str, query: str, offset: int = 0, limit: int = 5) -> List[Any]:
    # Performs exact searching on a single field
    # If the query is a space separated string, it will search for each word in the fields
    search_body = {
        "query": {
            "match": {
                field_name: query
            }
        },
        "from": offset,
        "size": limit,
    },

    es_response = await es_client.search(
        index="organizations",
        body=search_body
    )

    organizations_ids = [hit["_source"]["id"] for hit in es_response["hits"]["hits"]]

    return organizations_ids

async def prefix_match_search(field_name: str, query: str, offset: int = 0, limit: int = 5) -> List[Any]:
    # Performs exact searching on a single field (which is represented by field_name)
    search_body = {
        "query": {
            "prefix": {
                field_name: query,
                "case_insensitive": True
            }
        },
        "from": offset,
        "size": limit,
    },

    es_response = await es_client.search(
        index="organizations",
        body=search_body
    )

    organizations_ids = [hit["_source"]["id"] for hit in es_response["hits"]["hits"]]

    return organizations_ids

async def range_match_search(field_name: str, gte: int, lte: int, offset: int = 0, limit: int = 5) -> List[Any]:
    # Performs range searching on a single field (which is represented by field_name). It then returns all the values that lie between the lte and gte values.
    search_body = {
        "query": {
            "range": {
                field_name: {
                    "gte": gte,
                    "lte": lte,
                }
            }
        },
        "from": offset,
        "size": limit,
    },

    es_response = await es_client.search(
        index="organizations",
        body=search_body
    )

    organizations_ids = [hit["_source"]["id"] for hit in es_response["hits"]["hits"]]

    return organizations_ids

async def range_match_search(field_name: str, gte: int, lte: int, offset: int = 0, limit: int = 5) -> List[Any]:
    # Returns all documents having non null valies
    search_body = {
        "query": {
            "field": field_name
        },
        "from": offset,
        "size": limit,
    },

    es_response = await es_client.search(
        index="organizations",
        body=search_body
    )

    organizations_ids = [hit["_source"]["id"] for hit in es_response["hits"]["hits"]]

    return organizations_ids