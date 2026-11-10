"""Reuse the index students build in the Components lesson; no implicit LLM."""
import os
from pathlib import Path
from llama_index.core.tools import QueryEngineTool

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(ROOT / ".cache" / "huggingface"))
EMBED_MODEL = "BAAI/bge-small-en-v1.5"


def embedding_model():
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    settings = dict(
        model_name=EMBED_MODEL, device="cpu",
        cache_folder=str(ROOT / ".cache" / "huggingface"),
    )
    try:
        model = HuggingFaceEmbedding(**settings, local_files_only=True)
        print("Loaded the cached CPU embedding model locally; no HF request was needed.")
        return model
    except OSError:
        print("No complete model cache. Downloading public embedding files; no HF token is required.", flush=True)
    try:
        return HuggingFaceEmbedding(**settings, local_files_only=False)
    except OSError:
        raise SystemExit(
            "The embedding model could not finish loading. Check internet access and free disk space, "
            "then rerun the same program to resume the public download. No Groq tokens were used "
            "for this download. See the setup troubleshooting table if it keeps failing."
        ) from None


def get_store():
    import chromadb
    from llama_index.vector_stores.chroma import ChromaVectorStore

    db = chromadb.PersistentClient(path=str(ROOT / "alfred_chroma_db"))
    collection = db.get_or_create_collection("alfred")
    return collection, ChromaVectorStore(chroma_collection=collection)


def open_index():
    from llama_index.core import VectorStoreIndex

    collection, store = get_store()
    if collection.count() == 0:
        raise SystemExit("No indexed personas. Run prepare_personas.py and then my_ingest.py first.")
    return VectorStoreIndex.from_vector_store(store, embed_model=embedding_model())


class EvidenceQueryEngineTool(QueryEngineTool):
    """Keep original passages visible to the agent, separately from generated prose."""

    def with_evidence(self, result):
        sources = getattr(result.raw_output, "source_nodes", [])
        parts = [
            "SEARCH SCOPE: only the retrieved passages below were checked, not every profile. "
            "If they contain no match, say 'No match was found in the retrieved passages.' "
            "Do not claim the entire database has no match.",
            "SOURCE EXCERPTS (verbatim; quote only these and name the file):",
        ]
        for hit in sources[:2]:
            name = hit.node.metadata.get("file_name", "unknown source")
            text = hit.node.get_content()
            excerpt = text[:800]
            parts.append(f"SOURCE: {name}\nEXCERPT:\n{excerpt}")
            if len(text) > 800:
                parts.append("[Excerpt clipped; open the source file for the remaining text.]")
        if not sources:
            parts.append("No original source passages were returned. Mark the evidence missing.")
        parts.append("GENERATED ANSWER (not an original quotation):\n" + result.content[:600])
        result.content = "\n\n".join(parts)
        return result

    async def acall(self, *args, **kwargs):
        return self.with_evidence(await super().acall(*args, **kwargs))

    def call(self, *args, **kwargs):
        return self.with_evidence(super().call(*args, **kwargs))


def persona_tool(llm):

    engine = open_index().as_query_engine(
        llm=llm, similarity_top_k=2, response_mode="compact", use_async=True,
    )
    return EvidenceQueryEngineTool.from_defaults(
        query_engine=engine, name="personas",
        description="Retrieve up to two passages from ten persona descriptions for interests and expertise. This is not an exhaustive review of every profile. A missing match means only that the retrieved passages did not document it. Returns SOURCE/EXCERPT text separately from a GENERATED ANSWER. Quote only the original EXCERPT and cite its SOURCE filename. No real names or contact details; mark missing facts honestly.",
        return_direct=False,
    )
