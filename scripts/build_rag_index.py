"""Build/update the local Chroma RAG index; run from project root."""
import argparse
from src.rag.engine import build_index

def main():
    parser=argparse.ArgumentParser(description='Build multilingual policy RAG index')
    parser.add_argument('--force', action='store_true', help='Rebuild index even when unchanged')
    args=parser.parse_args()
    info=build_index(force=args.force)
    print('RAG:',info['status'])
    print('Sections:',info['chunks'])
    print('Embedding model:',info['model'])
    print('Index location:',info['path'])

if __name__=='__main__':main()
