from logger import logger

def query_chain(chain, user_input:str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        result=chain({"query": user_input})

        sources = []
        for doc in result["source_documents"]:
            source_file = (doc.metadata.get("source", "")).split("/")[-1]
            chunk_number = int(doc.metadata.get("chunk", ""))

            sources.append(f"{source_file} (chunk {chunk_number})")
        response={
            "response": result["result"],
            "sources": sources,
        }
        logger.debug(f"Chain response: {response}")
        return response
    except Exception as e:
        logger.exception("Error on query chain")
        raise 