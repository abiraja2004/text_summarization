require(magrittr)
require(aRxiv)
require(pdftools)
require(dplyr)
require(parallel)

try_pdf_text <- function(url)
  tryCatch(
    pdf_text(url) %>% paste(collapse = " "),
    error = function(e)
      NA
  )

try_arxiv_search <- function(url, ...)
  tryCatch(
    arxiv_search(url, ...),
    error = function(e)
      data_frame()
  )

# запрашиваем у arxiv.org 127 * limit статей
library(doParallel)
cl <- makeCluster(detectCores())
registerDoParallel(cl)

par.setup <- parLapply(cl, 1:length(cl),
                       function(xx) {
                         require(aRxiv)
                         require(pdftools)
                         require(dplyr)
                       })

metadata <-  paste("cat", arxiv_cats$abbreviation, sep = ":") %>%
  parLapply(cl = cl,
            X = .,
            try_arxiv_search,
            limit = 200) %>%
  bind_rows() %>%
  distinct

docs <- parLapply(cl, metadata$link_pdf, try_pdf_text)

data <- list(metadata = metadata, docs = docs)
stopCluster(cl)

saveRDS(data, "arxiv_data.RDS")
saveRDS(data[1], "arxiv_meta.RDS")
saveRDS(data[2], "arxiv_docs.RDS")