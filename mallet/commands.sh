# cd /Users/jbakken/Desktop/HMC/2022_Fall/Research/Mallet/mallet_1996
export PATH=$PATH:/Users/jbakken/Mallet/bin/
# this removes problematic alphanumerics but keeps newlines, tabs, etc.
#tr -cd [:alnum:][\ ,.-/-]\\n\\t < ./segmented_documents.txt > ./segmented_documents.txt
mkdir unpruned
cd unpruned
# import currently doesn't include --stoplist-file, nor --token-regex
mallet import-file --input ../segmented_documents.txt --output segmented_docs_unpruned.seq --keep-sequence
# train the topic model
mallet train-topics --input segmented_docs_unpruned.seq --num-topics 50 --optimize-interval 10 --num-iterations 5000 --output-state segmented_docs_unpruned.txt.gz --evaluator-filename segmented_docs_unpruned.evaluator --output-topic-keys segmented_docs_unpruned.keys --num-top-words 50 --diagnostics-file segmented_docs_unpruned_diag.xml --topic-word-weights-file segmented_docs_unpruned.wordweights.txt --output-doc-topics segmented_docs_unpruned.doctopics.txt
cd .. 
mkdir pruned
cd pruned
# repeat, but with pruning
mallet import-file --input ../segmented_documents.txt --output segmented_docs_unpruned.seq --keep-sequence
# can adjust the pruning parameters
mallet prune --input segmented_docs_unpruned.seq --output segmented_docs_pruned.seq --prune-document-freq 5 --prune-count 5 --min-idf 2
mallet train-topics --input segmented_docs_pruned.seq --num-topics 50 --optimize-interval 10 --num-iterations 5000 --output-state segmented_docs_pruned.txt.gz --evaluator-filename segmented_docs_pruned.evaluator --output-topic-keys segmented_docs_pruned.keys --num-top-words 50 --diagnostics-file segmented_docs_pruned_diag.xml --topic-word-weights-file segmented_docs_pruned.wordweights.txt --output-doc-topics segmented_docs_pruned.doctopics.txt



