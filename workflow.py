from langgraph.graph import StateGraph, END
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from vector_store import get_vector_store

# Đổi model hội thoại
model_id = "facebook/blenderbot-400M-distill"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
hf_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=128)
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# State lưu dữ liệu
class ChatState(dict):
    question: str
    context: str
    answer: str

# Node 1: Tìm thông tin từ ChromaDB
def retrieve_info(state: ChatState):
    if len(state["question"].split()) <= 3:  # Nếu câu hỏi quá ngắn
        state["context"] = ""
        return state
    retriever = get_vector_store().as_retriever(search_kwargs={"k": 1})
    docs = retriever.get_relevant_documents(state["question"])
    state["context"] = "\n".join([d.page_content for d in docs])
    return state

# Node 2: Tạo câu trả lời
def generate_answer(state: ChatState):
    greetings = ["hi", "hello", "hey", "chào", "xin chào"]
    if state["question"].strip().lower() in greetings:
        state["answer"] = "Hello!"
        return state
    # BlenderBot chỉ cần câu hỏi, không cần prompt phức tạp
    answer = llm.invoke(state["question"])
    state["answer"] = answer
    return state

# Tạo workflow
graph = StateGraph(ChatState)
graph.add_node("retrieve", retrieve_info)
graph.add_node("answer", generate_answer)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "answer")
graph.add_edge("answer", END)

workflow = graph.compile()
