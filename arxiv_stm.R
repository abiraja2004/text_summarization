require(magrittr)
require(aRxiv)
require(pdftools)
require(quanteda)
require(stm)

# запрашиваем у arxiv.org тысячу статей из категорий Information Retrieval и Biological Physics

matches <- arxiv_search(query = "cat:cs.AR OR cat:physics.bio-ph", limit = 1000)
texts   <- lapply(matches$link_pdf, . %>% {try(suppressMessages(pdf_text(.)))})

# выкидываем 13 статей, которые не удалось распарсить

invalid <- which(sapply(texts, class) %in% "try-error")
texts   <- texts[-invalid]
matches <- matches[-invalid, ]

# токенизируем тексты и строим тематическую модель

texts %<>% sapply(paste, collapse = " ") %>% 
  dfm(ignoredFeatures = c(stopwords("english"), letters),
      stem = TRUE) %>% 
  trim(minDoc = 2) %>% 
  readCorpus()

model <- texts %$% 
  stm(documents, vocab, K = 10, prevalence = ~primary_category, data = matches)

# Topic 1: model, mutat, popul, rate, time 
# Topic 2: dna, fig, length, energi, forc 
# Topic 3: ω, state, can, eq, α 
# Topic 4: can, τ, function, one, distribut 
# Topic 5: cell, membran, al, model, fig 
# Topic 6: can, quantum, system, state, process 
# Topic 7: energi, protein, structur, simul, model 
# Topic 8: time, neuron, spike, signal, inform 
# Topic 9: system, comput, use, network, node 
# Topic 10: sequenc, gene, use, cluster, structur 

# дальше можно мерить близость текстов KL или JS дивергенцией
