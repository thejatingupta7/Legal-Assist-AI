import os
import pickle
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import faiss

# Paths to FAISS index and metadata file
FAISS_INDEX_PATH = "embed_db/index.faiss"
METADATA_PATH = "embed_db/index.pkl"

# Load FAISS index
index = faiss.read_index(FAISS_INDEX_PATH)

# Load metadata if available
metadata = None
if os.path.exists(METADATA_PATH):
    with open(METADATA_PATH, 'rb') as f:
        metadata = pickle.load(f)
        # Check if metadata is loaded correctly
        if isinstance(metadata, tuple):
            # If metadata is a tuple, attempt to unpack
            if len(metadata) > 0 and isinstance(metadata[0], dict):
                metadata = metadata[0]  # Assuming the first item is the dictionary
            else:
                metadata = None  # Unable to unpack tuple as dictionary

# Retrieve embeddings
embeddings = index.reconstruct_n(0, index.ntotal)

# Extract labels if metadata is available
labels = list(metadata.keys()) if metadata else None

# Perform dimensionality reduction using PCA
pca = PCA(n_components=2)
embeddings_pca = pca.fit_transform(embeddings)

# Plotting the embeddings
plt.figure(figsize=(10, 8))
plt.scatter(embeddings_pca[:, 0], embeddings_pca[:, 1], c='b', alpha=0.5)
plt.title('PCA of Embeddings')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')

# Annotate points with labels if available
if labels:
    for i, label in enumerate(labels):
        plt.annotate(label, (embeddings_pca[i, 0], embeddings_pca[i, 1]))

plt.grid(True)
plt.show()
