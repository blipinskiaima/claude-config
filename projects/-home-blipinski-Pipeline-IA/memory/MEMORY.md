# Memory Index

- [project_cohort.md](project_cohort.md) — Cohort composition: 83 cancer + 50 healthy, validated on S3
- [reference_s3_paths.md](reference_s3_paths.md) — S3 bucket paths for cancer/healthy bedMethyl data
- [project_data_stats.md](project_data_stats.md) — Sparse matrix dimensions, sparsity, CpG coverage stats
- [project_model_results.md](project_model_results.md) — LR 1000 features: AUC=1.0, sens=0.988, Transformer skipped
- [project_phase2_results.md](project_phase2_results.md) — cfDNA eval: 79% sens high VAF CGFL, 47% combined
- [feedback_memory_optimization.md](feedback_memory_optimization.md) — Never hstack full genome matrices, process per chromosome
- [feedback_parsing_speed.md](feedback_parsing_speed.md) — Use pandas.read_csv not line-by-line, 16x speedup
