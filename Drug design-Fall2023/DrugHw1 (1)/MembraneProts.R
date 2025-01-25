if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install(version = "3.18")
BiocManager::install(c("biomaRt"))
library("biomaRt")

ensembl <- useMart("ensembl", dataset = "hsapiens_gene_ensembl")
filters <- c("go")
attributes <- c("ensembl_gene_id", "external_gene_name", "description", "go_id")

membrane_prots <- getBM(attributes = attributes,
                 filters = filters,
                 values = list(go="GO:0016020"),
                 mart = ensembl)

membrane_prots[50:150,]
