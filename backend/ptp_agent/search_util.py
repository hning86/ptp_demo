import os
import re
from google.cloud import discoveryengine_v1 as discoveryengine

def search_vais(query: str, category: str = None) -> str:
    """
    Search Vertex AI Search Data Store for content.
    
    Args:
        query: The search query string.
        category: Optional category to filter or prioritize.
                  Note: Server-side filtering by category requires the field to be 
                  marked as filterable in the Discovery Engine schema.
                  If not filterable, we fallback to prepending the category to the query
                  to prioritize results.
    """
    client = discoveryengine.SearchServiceClient()
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'ninghai-ccai')
    location = os.environ.get('VAIS_LOCATION', 'global')
    datastore_id = os.environ.get('VAIS_DATASTORE_ID', 'ptp-docs-store')
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{datastore_id}/servingConfigs/default_search"
    print(f"---DEBUG: VAIS Search with query: '{query}', category: '{category}'")
        
    filter_expr = f'category: ANY("{category}")' if category else ""
        
    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=query,
        filter=filter_expr if filter_expr else None,
        page_size=3,
        content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
            extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                max_extractive_segment_count=1
            )
        )
    )
    
    try:
        response = client.search(request=request)
    except Exception as e:
        print(f"---DEBUG: Filter search failed: {e}. Falling back to query prepending.")
        full_query = query
        if category:
            full_query = f"{category} {query}"
            
        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=full_query,
            page_size=3,
            content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
                extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                    max_extractive_segment_count=1
                )
            )
        )
        try:
            response = client.search(request=request)
        except Exception as e2:
            return f"Error searching VAIS: {e2}"

    results = []
    for result in response.results:
        derived = result.document.derived_struct_data
        if derived:
            for seg in derived.get("extractive_segments", []):
                raw_seg = seg.get("content", "")
                # Clean up tags and ellipses
                clean_seg = re.sub(r'</?b>', '', raw_seg)
                clean_seg = clean_seg.replace('...', '').strip()
                if clean_seg:
                    results.append(clean_seg)
        
    if not results:
        return "No specific guidelines found for this query."
        
    # Remove duplicates
    unique_results = list(set(results))
    return "\n\n".join(unique_results)
