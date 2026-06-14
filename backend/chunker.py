from langchain_text_splitters import MarkdownHeaderTextSplitter
import re

def clean_markdown_chunk(text):
    """
    Removes Markdown table artifacts, excessive hyphens, 
    and styling characters like pipes and asterisks.
    """
    # 1. Remove Table Pipe characters (|)
    text = text.replace('|', ' ')
    
    # 2. Remove Table Alignment/Divider rows (e.g., |---|---|)
    # This regex looks for 3 or more hyphens or colons inside pipes
    text = re.sub(r'[:\-]{3,}', ' ', text)
    
    # 3. Remove Bold/Italic asterisks (**) and underscores (_)
    text = text.replace('**', '').replace('*', '').replace('_', '').replace('###', '')
    
    # 4. Remove excessive hyphens (keeping single hyphens for words)
    text = re.sub(r'-{2,}', ' ', text)
    
    # 5. Collapse multiple spaces and newlines for a clean string
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def split_markdown_and_prepare_chunks():
    # 1. Load your Knowledge Base File
    with open("knowledge_base/Refund_Knowledge_Base.md", "r") as f:
        full_content = f.read()

    # 2. Define the Hierarchy for Honesty
    # This tells the splitter to look for # (Doc Title) and ## (Specific Policy)
    # It will inject these into the metadata of every chunk.
    headers_to_split_on = [
        ("#", "Document_Title"),
        ("##", "Section"),
        ("###", "Sub_Section"),
    ]

    # 3. Initialize the Splitter
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, 
        strip_headers=False # Keep headers in the text so the LLM sees them too
    )

    # 4. Perform the Split
    # This turns your 10-page doc into many smaller, context-aware chunks
    md_header_splits = markdown_splitter.split_text(full_content)

    # 5. Process Chunks for Pinecone/Vector DB
    processed_chunks = []
    for i, chunk in enumerate(md_header_splits):
        # Construct a clean object for your database
        if len(list(chunk.metadata.values())) == 1:
            continue
        
        payload = {
            "_id": f"chunk_{i}",
            "content": clean_markdown_chunk(chunk.page_content),
            "metadata": list(chunk.metadata.values())
        }
        processed_chunks.append(payload)
    
    return processed_chunks
