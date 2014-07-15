# PhD Tools and Data


Tools and data related to my phd.

## trec_medtrack_additional_qrels

Additional Relevance Assessment for TREC Medical Records Track

We are making publicly available a set of additional relevance assessments (qrels) for the TREC Medical Records Track. These are in additional to the officials qrels for this task provided by TREC organisers. The qrels are for the same set TREC query topics but are assessments for an additional 950 documents not previously judged by TREC assessors. As with TREC, the assessments were conducted by medical professionals.

Full details about how the assessments were obtained is available in Chapter 7 of:

B. Koopman. Semantic Search as Inference: Applications in Health Informatics. PhD thesis, Queensland University of Technology, Brisbane, Australia, 2014. http://koopman.id.au/papers/KoopmanPhDThesis-SemanticSearchAsInference.pdf

Or for more analysis of the assessment task see also:

B. Koopman and G. Zuccon. Why assessing relevance in medical IR is demanding. In Proceedings of the SIGIR Workshop on Medical Information Retrieval (MedIR), Gold Coast, Australia, July 2014. http://koopman.id.au/papers/medIR2014-relevance_assessment.pdf

## ir_results_kinematics:
Compare two sets of TREC retrieval results.

	Input: 
		1.results, 2,results, qrel
	Output:
		Both results file annotated with i) '*' to indicate relevance ii) the position of the 
		document as [x,y] where x = pos in 1.results and y = pos in 2.results.
