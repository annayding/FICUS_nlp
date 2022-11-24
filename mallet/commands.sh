export PATH=$PATH:/Users/jbakken/Mallet/bin/

mkdir unpruned; cd unpruned
# importing docs
mallet import-file --input ../segmented_docs.txt --output segmented_docs_unpruned.seq --keep-sequence
# training topic model
mallet train-topics --input segmented_docs_unpruned.seq --num-topics 50 --optimize-interval 10 \
--num-iterations 5000 --output-state segmented_docs_unpruned.txt.gz --evaluator-filename segmented_docs_unpruned.evaluator \
--output-topic-keys segmented_docs_unpruned.keys --num-top-words 50 --diagnostics-file segmented_docs_unpruned_diag.xml \
--topic-word-weights-file segmented_docs_unpruned.wordweights.txt --output-doc-topics segmented_docs_unpruned.doctopics.txt

# repeat process, but with pruning
cd ..; mkdir pruned; cd pruned
mallet import-file --input ../segmented_docs.txt --output segmented_docs_unpruned.seq --keep-sequence
# pruning (we should adjust the parameters)
mallet prune --input segmented_docs_unpruned.seq --output segmented_docs_pruned.seq \
--prune-document-freq 5 --prune-count 5 --min-idf 2
# training topic model
mallet train-topics --input segmented_docs_pruned.seq --num-topics 50 --optimize-interval 10 \
--num-iterations 5000 --output-state segmented_docs_pruned.txt.gz --evaluator-filename segmented_docs_pruned.evaluator \
--output-topic-keys segmented_docs_pruned.keys --num-top-words 50 --diagnostics-file segmented_docs_pruned_diag.xml \
--topic-word-weights-file segmented_docs_pruned.wordweights.txt --output-doc-topics segmented_docs_pruned.doctopics.txt



