from langchain_experimental.graph_transformers import LLMGraphTransformer
import LLMAccess as access
import DocumentReader as reader
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain.chains import GraphCypherQAChain


# export NEO4J_HOME=/users/ambarishdeshpande/LTIMindtree/Graphs/neo4j-community-5.22.0


NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "Graph@24"
file_path = "data/motor.pdf"
graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)

def create_graph(file_path):
    text = reader.extract_text_with_layout(file_path)
    documents = [Document(page_content=text)]
    gpt4o = access.get_gpt4omni()
    llm_transformer = LLMGraphTransformer(llm=gpt4o)
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    return graph_documents

def graph_exists(label):
    graph.refresh_schema()
    result = graph.query(f"MATCH (n:{label}) RETURN COUNT(n) AS count")
    print(result, type(result))
    count = result[0].get("count")
    return count > 0

def graph_rag(file_path, question):
    if not graph_exists('Policy'):
        print("Graph not Found - creating now")
        graph_documents = create_graph(file_path)
        graph.add_graph_documents(graph_documents, baseEntityLabel=True)
        graph.refresh_schema()
    chain = GraphCypherQAChain.from_llm(graph=graph, llm=access.get_gpt4omni(), verbose=True)
    response = chain.invoke({"query": question})
    return response


answer = graph_rag(file_path=file_path, question="list all from liability section?")
print(answer)

