# app/api/watch_queries.py
from config.database import collection

# Function to monitor MongoDB changes and return updated queries
def watch_queries_stream():
    """
    Generator function that yields latest queries whenever 
    a document is inserted or updated.
    """
    with collection.watch() as stream:
        for change in stream:
            op_type = change["operationType"]

            # Insert operation
            if op_type == "insert":
                latest_doc = change["fullDocument"]
                # Extract all queries from the document
                queries = [q["query"] for q in latest_doc.get("queries", [])]
                yield {"operation": "insert", "queries": queries}

            # Update operation
            elif op_type == "update":
                updated_fields = change["updateDescription"]["updatedFields"]
                # Filter only keys that are queries
                updated_queries = []
                for k, v in updated_fields.items():
                    if k.startswith("queries.") and "query" in v:
                        updated_queries.append(v["query"])
                yield {"operation": "update", "updated_queries": updated_queries}

# Example usage in a while loop (non-blocking usage is recommended)
if __name__ == "__main__":
    for update in watch_queries_stream():
        print("Change detected:", update)
