if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install(version = "3.18")
BiocManager::install(c("biomaRt"))
library("biomaRt")

ensembl <- useMart("ensembl", dataset = "hsapiens_gene_ensembl")
attributes <- c("ensembl_gene_id", "external_gene_name", "gene_biotype", "description", "go_id")
receptors <- getBM(attributes = attributes,
                 values = list(with_ortholog = TRUE, 
                               homolog_ensembl_gene = "receptor"),
                 mart = ensembl)

receptors[50:150, ]
